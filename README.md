# AI Visibility Hub — autonomous traffic machine

Satellite content/data hub driving organic traffic to [aicantfindme.com](https://aicantfindme.com).
Runs itself via GitHub Actions. Live site: https://myaiplay.github.io/ai-visibility-hub/

## How it works

```
engine/run_tests.py        → nightly: asks AI engines buyer questions, records who gets named
engine/aggregate.py        → aggregates runs, generates /index/* stat pages (real data only)
engine/generate_article.py → Mondays: data article from recorded stats (hallucination-gated)
engine/syndicate_devto.py  → cross-posts articles to Dev.to (canonical back to hub)
engine/report.py           → Sundays: performance report → reports/
engine/dashboard.py        → live status page: /dashboard/ (spend, coverage, traffic)
engine/ogimage.py          → branded 1200x630 social cards for every page at build time
engine/indexnow.py         → pings Bing/IndexNow with new URLs after every build
build.py                   → renders content/*.md → docs/ (GitHub Pages) + RSS + sitemap
social/post_x.py           → daily X post (31/mo cap, OAuth2 rotating tokens)
social/post_bsky.py        → daily Bluesky post (free)
```

All scripts exit gracefully when their API keys aren't set — channels activate
automatically as secrets are added.

## Secrets (repo Settings → Secrets and variables → Actions)

| Secret | Enables | Status |
|---|---|---|
| `PERPLEXITY_API_KEY` | nightly data engine + stat pages | **active** (hard $5/mo cap in `engine/run_tests.py`) |
| `X_CLIENT_ID` / `X_CLIENT_SECRET` / `X_STATE_KEY` | daily X posts via @aicantseeme (OAuth 2.0, rotating tokens in `social/x_state.enc`; 31 posts/mo cap) | **active** (prepaid credits, no auto-reload) |
| `BSKY_HANDLE` / `BSKY_APP_PASSWORD` | daily Bluesky posts via @aicantseeme | **active** (free) |
| `DEVTO_API_KEY` | article cross-posting | **active** |

## Rules this machine follows

1. **No invented statistics.** Numbers on stat pages come only from recorded runs in `data/runs/`.
2. **Variance guardrail.** A category/city page publishes only after ≥3 runs.
3. **ToS-safe only.** No spam, no astroturfing, no mass outreach. Ever.
4. **Every page funnels** to aicantfindme.com with UTM-tagged CTAs.

## Manual ops

- `python build.py` — rebuild site locally (needs `pip install -r requirements.txt`)
- Add prompts: edit `engine/prompts.yaml`
- Add social posts: append lines to `social/queue.txt`
- Track directory submissions: `distribution/directories.csv`
