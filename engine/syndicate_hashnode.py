#!/usr/bin/env python3
"""Cross-post hub articles to Hashnode with canonical back to the hub.

Requires HASHNODE_TOKEN (GitHub secret) — Hashnode Personal Access Token.
Publication ID is auto-discovered from the token's account.
Exits gracefully without it. Max 1 new article per run (drip cadence).
Tracks state in data/syndicated_hashnode.json — never double-posts.
"""
import json
import os
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).parent.parent
ARTICLES = ROOT / "content" / "articles"
INDEX_DIR = ROOT / "content" / "index"
STATE = ROOT / "data" / "syndicated_hashnode.json"
BASE = "https://myaiplay.github.io/ai-visibility-hub"
MAIN = "https://aicantfindme.com"
GQL = "https://gql.hashnode.com"

MAX_NEW_PER_RUN = 1


def gql(token, query, variables=None):
    import requests
    r = requests.post(GQL, headers={"Authorization": token},
                      json={"query": query, "variables": variables or {}},
                      timeout=30)
    r.raise_for_status()
    d = r.json()
    if d.get("errors"):
        raise RuntimeError(str(d["errors"])[:300])
    return d["data"]


def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    return (yaml.safe_load(m.group(1)), m.group(2)) if m else ({}, text)


def to_hashnode_markdown(body, slug):
    body = re.sub(r"\]\(/", f"]({BASE}/", body)
    body = body.replace('<p class="lede">', "<p>").replace('<div class="answer">', "<blockquote>").replace("</div>", "</blockquote>", 1)
    return body + (
        "\n\n---\n\n*Originally published at the "
        f"[AI Visibility Index]({BASE}/articles/{slug}/). Free research by the makers of "
        f"[aicantfindme.com]({MAIN}?utm_source=hashnode&utm_medium=article&utm_campaign={slug}).*\n"
    )


def main():
    token = os.environ.get("HASHNODE_TOKEN")
    if not token:
        print("HASHNODE_TOKEN not set — skipping (Hashnode idle until key added).")
        return

    me = gql(token, "query { me { publications(first: 1) { edges { node { id title } } } } }")
    pubs = me["me"]["publications"]["edges"]
    if not pubs:
        print("No Hashnode publication found — create one at hashnode.com first.")
        return
    pub_id = pubs[0]["node"]["id"]
    print(f"Publication: {pubs[0]['node']['title']} ({pub_id})")

    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    sources = sorted(ARTICLES.glob("*.md"))
    if INDEX_DIR.exists():
        sources += sorted(INDEX_DIR.glob("*.md"))

    posted = 0
    for md in sources:
        if posted >= MAX_NEW_PER_RUN:
            break
        slug = md.stem
        if slug in state:
            continue
        meta, body = parse_frontmatter(md.read_text())
        canonical = f"{BASE}/articles/{slug}/"
        try:
            data = gql(token, """
              mutation($input: PublishPostInput!) {
                publishPost(input: $input) { post { id url } }
              }""", {"input": {
                "title": meta.get("title", slug),
                "subtitle": meta.get("description", "")[:250],
                "contentMarkdown": to_hashnode_markdown(body, slug),
                "publicationId": pub_id,
                "originalArticleURL": canonical,
                "tags": [{"name": t, "slug": t} for t in
                         ["seo", "ai", "marketing", "small-business"]],
            }})
            url = data["publishPost"]["post"]["url"]
            state[slug] = {"id": data["publishPost"]["post"]["id"], "url": url}
            posted += 1
            print(f"Posted: {slug} -> {url}")
        except Exception as e:
            print(f"FAILED: {slug} -> {e}")

    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, indent=2))
    print(f"Done. {posted} new posted, {len(state)} total on Hashnode.")


if __name__ == "__main__":
    main()
