#!/usr/bin/env python3
"""X bot (OAuth 2.0): post the next item from social/queue.txt, rotate to bottom.

Secrets (GitHub): X_CLIENT_ID, X_CLIENT_SECRET, X_STATE_KEY.
Token state lives encrypted in social/x_state.enc (X rotates refresh tokens
on every use, so we must persist them each run). Never stores plaintext
tokens in the repo.
"""
import json
import os
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent.parent
QUEUE = ROOT / "social" / "queue.txt"
STATE = ROOT / "social" / "x_state.enc"
SPEND = ROOT / "data" / "x_posts.json"

# --- Hard spend guardrails (X credits are prepaid; these stop us burning them) ---
MAX_POSTS_PER_MONTH = 31        # 1/day; the money cap is set on X's side (no auto-reload)
MIN_HOURS_BETWEEN_POSTS = 20    # blocks accidental/manual re-runs draining credits


def load_spend():
    import datetime
    if SPEND.exists():
        s = json.loads(SPEND.read_text())
        if s.get("month") == date.today().strftime("%Y-%m"):
            return s
    return {"month": date.today().strftime("%Y-%m"), "posts": 0, "last_post": None}


def main():
    cid = os.environ.get("X_CLIENT_ID")
    csec = os.environ.get("X_CLIENT_SECRET")
    key_hex = os.environ.get("X_STATE_KEY")
    if not all([cid, csec, key_hex]):
        print("X secrets not set — skipping (bot idle until keys added).")
        return
    if not STATE.exists():
        print("social/x_state.enc missing — bot not bootstrapped yet.")
        return

    from nacl.secret import SecretBox
    import requests

    box = SecretBox(bytes.fromhex(key_hex))
    tokens = json.loads(box.decrypt(STATE.read_bytes()).decode())

    # 1. Refresh access token (refresh token rotates — save the new one)
    r = requests.post("https://api.x.com/2/oauth2/token",
                      auth=(cid, csec),
                      data={"grant_type": "refresh_token",
                            "refresh_token": tokens["refresh_token"]},
                      timeout=30)
    if r.status_code != 200:
        print(f"Token refresh failed ({r.status_code}): {r.text[:200]}")
        print("Re-bootstrap needed: re-authorize and reseed x_state.enc.")
        return
    tokens = r.json()
    STATE.write_bytes(box.encrypt(json.dumps({
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"],
    }).encode()))

    # 2. Spend guardrails
    import datetime
    spend = load_spend()
    if spend["posts"] >= MAX_POSTS_PER_MONTH:
        print(f"MONTHLY POST CAP REACHED ({spend['posts']}/{MAX_POSTS_PER_MONTH}). Refusing to post.")
        return
    if spend.get("last_post"):
        last = datetime.datetime.fromisoformat(spend["last_post"])
        hours = (datetime.datetime.now(datetime.timezone.utc) - last).total_seconds() / 3600
        if hours < MIN_HOURS_BETWEEN_POSTS:
            print(f"Too soon since last post ({hours:.1f}h < {MIN_HOURS_BETWEEN_POSTS}h). Skipping.")
            return

    # 3. Post next queued item
    lines = [l.strip() for l in QUEUE.read_text().splitlines() if l.strip()]
    if not lines:
        print("Queue empty.")
        return
    post = lines[0]
    p = requests.post("https://api.x.com/2/tweets",
                      headers={"Authorization": f"Bearer {tokens['access_token']}"},
                      json={"text": post}, timeout=30)
    if p.status_code in (200, 201):
        tid = p.json()["data"]["id"]
        QUEUE.write_text("\n".join(lines[1:] + [lines[0]]) + "\n")
        spend["posts"] += 1
        spend["last_post"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        SPEND.parent.mkdir(parents=True, exist_ok=True)
        SPEND.write_text(json.dumps(spend, indent=2))
        print(f"Posted: https://x.com/aicantseeme/status/{tid}")
        print(f"  text: {post[:70]}...")
        print(f"  month usage: {spend['posts']}/{MAX_POSTS_PER_MONTH} posts")
    else:
        print(f"Post failed ({p.status_code}): {p.text[:200]}")


if __name__ == "__main__":
    main()
