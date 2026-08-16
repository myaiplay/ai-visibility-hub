#!/usr/bin/env python3
"""Bluesky bot: walk social/queue.txt by index, post one item per run.

Secrets (GitHub): BSKY_HANDLE, BSKY_APP_PASSWORD.
Sessions are created fresh per run (stateless — no token persistence needed).
Pointer tracked in data/bsky_state.json.
"""
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent.parent
QUEUE = ROOT / "social" / "queue.txt"
STATE = ROOT / "data" / "bsky_state.json"

MIN_HOURS_BETWEEN_POSTS = 20


def build_facets(text):
    """Make URLs clickable via richtext facets (byte-indexed)."""
    facets = []
    for m in re.finditer(r"https?://[^\s)>]+", text):
        start = len(text[:m.start()].encode("utf-8"))
        end = start + len(m.group().encode("utf-8"))
        facets.append({
            "index": {"byteStart": start, "byteEnd": end},
            "features": [{"$type": "app.bsky.richtext.facet#link", "uri": m.group()}],
        })
    return facets


def main():
    handle = os.environ.get("BSKY_HANDLE")
    pw = os.environ.get("BSKY_APP_PASSWORD")
    if not all([handle, pw]):
        print("Bluesky secrets not set — skipping.")
        return

    import requests

    # Rate guard
    state = json.loads(STATE.read_text()) if STATE.exists() else {"index": 0, "last_post": None}
    if state.get("last_post"):
        hours = (datetime.now(timezone.utc) - datetime.fromisoformat(state["last_post"])).total_seconds() / 3600
        if hours < MIN_HOURS_BETWEEN_POSTS:
            print(f"Too soon since last post ({hours:.1f}h). Skipping.")
            return

    lines = [l.strip() for l in QUEUE.read_text().splitlines() if l.strip()]
    if not lines:
        print("Queue empty.")
        return
    text = lines[state["index"] % len(lines)]
    if len(text) > 299:
        text = text[:296] + "..."

    # Session
    s = requests.post("https://bsky.social/xrpc/com.atproto.server.createSession",
                      json={"identifier": handle, "password": pw}, timeout=30)
    if s.status_code != 200 and "." not in handle:
        # retry with default domain
        s = requests.post("https://bsky.social/xrpc/com.atproto.server.createSession",
                          json={"identifier": f"{handle}.bsky.social", "password": pw}, timeout=30)
    if s.status_code != 200:
        print(f"Session failed ({s.status_code}): {s.text[:200]}")
        return
    sess = s.json()

    record = {
        "$type": "app.bsky.feed.post",
        "text": text,
        "createdAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "langs": ["en"],
        "facets": build_facets(text),
    }
    r = requests.post("https://bsky.social/xrpc/com.atproto.repo.createRecord",
                      headers={"Authorization": f"Bearer {sess['accessJwt']}"},
                      json={"repo": sess["did"], "collection": "app.bsky.feed.post",
                            "record": record}, timeout=30)
    if r.status_code == 200:
        rkey = r.json()["uri"].split("/")[-1]
        state["index"] = (state["index"] + 1) % len(lines)
        state["last_post"] = datetime.now(timezone.utc).isoformat()
        STATE.parent.mkdir(parents=True, exist_ok=True)
        STATE.write_text(json.dumps(state, indent=2))
        h = handle if "." in handle else f"{handle}.bsky.social"
        print(f"Posted: https://bsky.app/profile/{h}/post/{rkey}")
        print(f"  text: {text[:70]}...")
    else:
        print(f"Post failed ({r.status_code}): {r.text[:200]}")


if __name__ == "__main__":
    main()
