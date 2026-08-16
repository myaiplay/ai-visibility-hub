#!/usr/bin/env python3
"""Cross-post hub articles to Dev.to with canonical_url back to the hub.

Requires DEVTO_API_KEY (GitHub secret). Exits gracefully without it.
Tracks posted articles in data/syndicated.json — never double-posts.
"""
import json
import os
import re
import sys
import time
from pathlib import Path

import yaml

ROOT = Path(__file__).parent.parent
ARTICLES = ROOT / "content" / "articles"
INDEX_DIR = ROOT / "content" / "index"
STATE = ROOT / "data" / "syndicated.json"
BASE = "https://myaiplay.github.io/ai-visibility-hub"
MAIN = "https://aicantfindme.com"

TAGS = ["seo", "ai", "marketing", "business"]


def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    return (yaml.safe_load(m.group(1)), m.group(2)) if m else ({}, text)


def to_devto_markdown(body, slug):
    # Rewrite relative links to absolute hub URLs
    body = re.sub(r"\]\(/", f"]({BASE}/", body)
    # Strip lede/answer div classes Dev.to doesn't need, keep content
    body = body.replace('<p class="lede">', "<p>").replace('<div class="answer">', "<blockquote>").replace("</div>", "</blockquote>", 1)
    footer = (
        "\n\n---\n\n*Originally published at the "
        f"[AI Visibility Index]({BASE}/articles/{slug}/). Free research by the makers of "
        f"[aicantfindme.com]({MAIN}?utm_source=devto&utm_medium=article&utm_campaign={slug}) — "
        "find out why AI search isn't recommending your business.*\n"
    )
    return body + footer


def main():
    key = os.environ.get("DEVTO_API_KEY")
    if not key:
        print("DEVTO_API_KEY not set — skipping (syndication idle until key added).")
        return

    import requests

    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    sources = sorted(ARTICLES.glob("*.md"))
    if INDEX_DIR.exists():
        sources += sorted(INDEX_DIR.glob("*.md"))

    posted = 0
    for md in sources:
        slug = md.stem
        if slug in state:
            continue
        meta, body = parse_frontmatter(md.read_text())
        prefix = "index" if INDEX_DIR in md.parents else "articles"
        canonical = f"{BASE}/{prefix}/{slug}/"
        payload = {
            "article": {
                "title": meta.get("title", slug),
                "description": meta.get("description", ""),
                "body_markdown": to_devto_markdown(body, slug),
                "published": True,
                "canonical_url": canonical,
                "tags": TAGS,
            }
        }
        r = requests.post("https://dev.to/api/articles",
                          headers={"api-key": key, "Content-Type": "application/json"},
                          json=payload, timeout=30)
        if r.status_code == 201:
            art = r.json()
            state[slug] = {"id": art["id"], "url": art["url"], "canonical": canonical}
            posted += 1
            print(f"Posted: {slug} -> {art['url']}")
        else:
            print(f"FAILED: {slug} ({r.status_code}): {r.text[:200]}")
        time.sleep(30)  # be polite to the API

    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, indent=2))
    print(f"Done. {posted} new articles posted, {len(state)} total syndicated.")


if __name__ == "__main__":
    main()
