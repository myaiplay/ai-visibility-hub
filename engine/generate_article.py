#!/usr/bin/env python3
"""Weekly data-article generator.

Turns recorded engine data into an editorial article via Perplexity.
ANTI-HALLUCINATION GATE: every number in the generated article must appear
in the source stats — otherwise the article is discarded, not published.

Requires PERPLEXITY_API_KEY and at least one aggregated category/city pair.
Respects the same $5/mo budget tracked in data/spend.json.
"""
import json
import os
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent.parent
INDEX = ROOT / "data" / "index.json"
SPEND = ROOT / "data" / "spend.json"
OUT_DIR = ROOT / "content" / "articles"

BUDGET_USD = 5.00
COST_PER_REQUEST_USD = 0.006


def budget_ok():
    if SPEND.exists():
        s = json.loads(SPEND.read_text())
        if s.get("month") == date.today().strftime("%Y-%m"):
            return s.get("estimated_usd", 0) + COST_PER_REQUEST_USD <= BUDGET_USD, s
    return True, {"month": date.today().strftime("%Y-%m"), "requests": 0, "estimated_usd": 0.0}


def main():
    key = os.environ.get("PERPLEXITY_API_KEY")
    if not key:
        print("PERPLEXITY_API_KEY not set — skipping.")
        return
    if not INDEX.exists():
        print("No aggregated data yet — nothing data-backed to write. Skipping.")
        return

    index = json.loads(INDEX.read_text())
    pairs = index.get("pairs", [])
    if not pairs:
        print("No category/city pairs past the variance threshold yet. Skipping.")
        return

    ok, spend = budget_ok()
    if not ok:
        print("Monthly budget cap reached — article generation paused.")
        return

    # Build the stats brief (only pairs with most runs, keep prompt small)
    pairs = sorted(pairs, key=lambda p: -p["runs"])[:6]
    brief = {f"{p['category']} in {p['city']}": {
        "test_runs": p["runs"],
        "most_named": [{"business": t["name"],
                        "named_in_pct_of_answers": round(t["mention_rate"] * 100)}
                       for t in p["top"][:5]],
    } for p in pairs}

    import requests
    prompt = f"""You are a careful data journalist. Write a 700-900 word article for a blog called "AI Visibility Index" about which local businesses AI search engines currently recommend.

VERIFIED DATA (from recorded test runs — your ONLY allowed source of numbers):
{json.dumps(brief, indent=2)}

STRICT RULES:
- Every statistic or percentage you state MUST appear in the verified data above. Never invent numbers.
- Do not claim causation (don't say WHY a business is named unless framed as a hypothesis).
- Structure: start with a 2-3 sentence direct-answer summary of the key finding. Then "What the data shows" section with specifics per category/city. Then a short "What this means if you're a local business" section with practical framing (crawler access, entity signals, citable answers — no numbers needed here). End with a short FAQ (2 questions, each answer 1-2 sentences).
- Tone: plain, confident, no hype. No emojis. No word "delve".
- Output markdown body only — no H1 title, no frontmatter. Use ## for sections."""

    r = requests.post(
        "https://api.perplexity.ai/chat/completions",
        headers={"Authorization": f"Bearer {key}"},
        json={"model": "sonar", "max_tokens": 1800,
              "messages": [{"role": "user", "content": prompt}]},
        timeout=90,
    )
    r.raise_for_status()
    body = r.json()["choices"][0]["message"]["content"]

    # --- ANTI-HALLUCINATION GATE ---
    allowed_numbers = set(re.findall(r"\d+", json.dumps(brief)))
    used_numbers = set(re.findall(r"\d+", body))
    # allow structural numbers (list indexes etc. small ints) only if in data
    bad = {n for n in used_numbers - allowed_numbers if int(n) > 1}
    if bad:
        print(f"REJECTED: article contained numbers not in source data: {sorted(bad)}")
        return
    if len(body.split()) < 400:
        print("REJECTED: article too short (<400 words).")
        return

    # Record spend
    spend["requests"] = spend.get("requests", 0) + 1
    spend["estimated_usd"] = round(spend["requests"] * COST_PER_REQUEST_USD, 3)
    SPEND.write_text(json.dumps(spend, indent=2))

    slug = f"what-ai-recommends-{date.today().isoformat()}"
    total_runs = sum(p["runs"] for p in pairs)
    (OUT_DIR / f"{slug}.md").write_text(f"""---
title: "What AI search recommended this week ({date.today():%d %B %Y})"
description: "Recorded data from {total_runs} AI search tests: which local businesses ChatGPT-style engines actually named this week, by category and city."
type: article
date: {date.today().isoformat()}
utm: weekly_data
---

# What AI search recommended this week

<p class="meta">{date.today():%d %B %Y} · Based on {total_runs} recorded test runs · AI Visibility Index</p>

{body}

---

*All numbers above come from recorded test runs published in our [open data index](/). Want your business tested? [One-time diagnostic, no subscription](https://aicantfindme.com?utm_source=hub&utm_medium=weekly_data&utm_campaign=hub_cta).*
""")
    print(f"PUBLISHED: content/articles/{slug}.md "
      f"(spend: ${spend['estimated_usd']:.2f}/${BUDGET_USD:.2f})")


if __name__ == "__main__":
    main()
