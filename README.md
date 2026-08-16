# AI Visibility Hub — autonomous traffic machine

Satellite content/data hub driving organic traffic to [aicantfindme.com](https://aicantfindme.com).
Runs itself via GitHub Actions. Live site: https://myaiplay.github.io/ai-visibility-hub/

## How it works

```
engine/run_tests.py   → nightly: asks AI engines buyer questions, records who gets named
engine/aggregate.py   → aggregates runs, generates /index/* stat pages (real data only)
build.py              → renders content/*.md → docs/ (GitHub Pages)
social/post_x.py      → daily: posts next item from social/queue.txt, rotates
```

All scripts exit gracefully when their API keys aren't set — channels activate
automatically as secrets are added.

## Secrets (repo Settings → Secrets and variables → Actions)

| Secret | Enables | Status |
|---|---|---|
| `PERPLEXITY_API_KEY` | nightly data engine + stat pages | pending |
| `X_API_KEY` / `X_API_SECRET` / `X_ACCESS_TOKEN` / `X_ACCESS_SECRET` | daily X posts | pending |
| `DEVTO_API_KEY` | article cross-posting | pending |

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
