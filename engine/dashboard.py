#!/usr/bin/env python3
"""Generate content/dashboard.md — live status page for the automation machine.

Reads the state files the bots already maintain. Runs inside the nightly
workflow so the public dashboard is never more than ~24h stale.
"""
import json
import os
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).parent.parent
OUT = ROOT / "content" / "dashboard.md"

CRONS = [
    ("Data engine (12 AI tests)", 3, 17, "daily"),
    ("Bluesky post", 13, 37, "daily"),
    ("X post", 21, 43, "daily"),
    ("Dev.to catch-up", 5, 11, "mon"),
    ("Weekly data article", 6, 7, "mon"),
    ("Weekly report", 18, 22, "sun"),
]


def load(p, default=None):
    f = ROOT / p
    return json.loads(f.read_text()) if f.exists() else default


def next_run(h, m, dow):
    now = datetime.now(timezone.utc)
    d = now.replace(hour=h, minute=m, second=0, microsecond=0)
    target = {"mon": 0, "sun": 6}.get(dow)
    while d <= now or (target is not None and d.weekday() != target):
        d += timedelta(days=1)
    return d


def traffic_section():
    """Pull traffic signals from free APIs we already have keys for."""
    import requests
    rows = []

    # Dev.to article stats
    dkey = os.environ.get("DEVTO_API_KEY")
    if dkey:
        try:
            r = requests.get("https://dev.to/api/articles/me/published?per_page=100",
                             headers={"api-key": dkey}, timeout=30)
            if r.status_code == 200:
                arts = r.json()
                rows.append(("Dev.to article views", str(sum(a.get("page_views_count", 0) for a in arts))))
                rows.append(("Dev.to reactions", str(sum(a.get("public_reactions_count", 0) for a in arts))))
        except Exception:
            pass

    # Bluesky followers (authenticated read)
    bh, bp = os.environ.get("BSKY_HANDLE"), os.environ.get("BSKY_APP_PASSWORD")
    if bh and bp:
        try:
            s = requests.post("https://bsky.social/xrpc/com.atproto.server.createSession",
                              json={"identifier": bh, "password": bp}, timeout=30)
            if s.status_code == 200:
                tok = s.json()["accessJwt"]
                r = requests.get("https://bsky.social/xrpc/app.bsky.actor.getProfile",
                                 headers={"Authorization": f"Bearer {tok}"},
                                 params={"actor": bh}, timeout=30)
                if r.status_code == 200:
                    d = r.json()
                    rows.append(("Bluesky followers", str(d.get("followersCount", 0))))
        except Exception:
            pass

    # GitHub repo traffic (last 14 days) via built-in Actions token
    ght = os.environ.get("GITHUB_TOKEN")
    if ght:
        try:
            r = requests.get("https://api.github.com/repos/myaiplay/ai-visibility-hub/traffic/views",
                             headers={"Authorization": f"Bearer {ght}"}, timeout=30)
            if r.status_code == 200:
                d = r.json()
                rows.append(("Repo views (14d)", f"{d.get('count', 0)} ({d.get('uniques', 0)} unique)"))
        except Exception:
            pass

    if not rows:
        return "_Traffic APIs not reachable from this environment._"
    body = "\n".join(f"| {k} | {v} |" for k, v in rows)
    return f"| Signal | Value |\n|---|---|\n{body}\n\n_Hub pageview analytics: add GoatCounter (see README) for per-page views + referrers._"


def main():
    spend = load("data/spend.json", {"estimated_usd": 0})
    xposts = load("data/x_posts.json", {"posts": 0})
    bsky = load("data/bsky_state.json", {})
    synd = load("data/syndicated.json", {})
    index = load("data/index.json", {"pairs": []})
    runs_dir = ROOT / "data" / "runs"
    run_days = len(list(runs_dir.glob("*.json"))) if runs_dir.exists() else 0
    prompts = 0
    if runs_dir.exists():
        for f in runs_dir.glob("*.json"):
            prompts += len(json.loads(f.read_text()).get("results", []))

    # health: engine ran within last 2 days?
    latest = max((f.stem for f in runs_dir.glob("*.json")), default=None) if runs_dir.exists() else None
    healthy = latest and (date.today() - date.fromisoformat(latest)).days <= 2
    status = "🟢 All systems running" if healthy else "🟡 Engine quiet >48h — check Actions tab"

    rows = "\n".join(
        f"| {name} | {next_run(h, m, d).astimezone().strftime('%a %d %b, %H:%M')} local |"
        for name, h, m, d in CRONS
    )

    bsky_last = bsky.get("last_post", "—")
    if bsky_last != "—":
        bsky_last = datetime.fromisoformat(bsky_last).strftime("%d %b, %H:%M UTC")

    OUT.write_text(f"""---
title: Automation dashboard
description: Live status of the AI Visibility Index automation machine — data engine, social bots, syndication, spend.
type: page
date: {date.today().isoformat()}
---

# Automation dashboard

<p class="lede">{status}</p>
<p class="meta">Last updated: {datetime.now(timezone.utc).strftime('%d %B %Y, %H:%M')} UTC · rebuilds nightly</p>

## Spend (hard-capped)

| Channel | Used | Cap |
|---|---|---|
| Data engine (Perplexity) | ${spend.get('estimated_usd', 0):.2f} | $5.00/mo |
| X posts | {xposts.get('posts', 0)} | 31/mo |
| Bluesky, Dev.to, hosting | $0 | free |

## Coverage

| Metric | Value |
|---|---|
| Test days recorded | {run_days} |
| Buyer prompts tested | {prompts} |
| Stat pages live | {len(index.get('pairs', []))} |
| Articles syndicated to Dev.to | {len(synd)} |
| Bluesky posts made | {bsky.get('index', 0)} (last: {bsky_last}) |

## Traffic

{traffic_section()}

## Next scheduled runs

| Job | Next run |
|---|---|
{rows}

## Data

- [Open dataset (index.json)](https://github.com/myaiplay/ai-visibility-hub/blob/main/data/index.json) — who AI is naming, by category and city
- [Weekly reports archive](https://github.com/myaiplay/ai-visibility-hub/tree/main/reports)
- [Raw test runs](https://github.com/myaiplay/ai-visibility-hub/tree/main/data/runs)

*This page is generated by `engine/dashboard.py` from the bots' own state files. The machine reports on itself.*
""")
    print("dashboard ->", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
