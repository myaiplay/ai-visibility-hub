#!/usr/bin/env python3
"""X bot: post the next item from social/queue.txt, rotate to bottom.

Needs secrets: X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET.
Exits gracefully without them.
"""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
QUEUE = ROOT / "social" / "queue.txt"


def main():
    keys = [os.environ.get(k) for k in
            ("X_API_KEY", "X_API_SECRET", "X_ACCESS_TOKEN", "X_ACCESS_SECRET")]
    if not all(keys):
        print("X secrets not set — skipping (bot idle until keys added).")
        return

    from requests_oauthlib import OAuth1
    import requests

    lines = [l.strip() for l in QUEUE.read_text().splitlines() if l.strip()]
    if not lines:
        print("Queue empty.")
        return

    post = lines[0]
    auth = OAuth1(*keys)
    r = requests.post("https://api.x.com/2/tweets", auth=auth,
                      json={"text": post}, timeout=30)
    if r.status_code in (200, 201):
        QUEUE.write_text("\n".join(lines[1:] + [lines[0]]) + "\n")
        print(f"Posted: {post[:60]}...")
    else:
        print(f"Post failed ({r.status_code}): {r.text[:200]}")


if __name__ == "__main__":
    main()
