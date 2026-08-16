#!/usr/bin/env python3
"""Aggregate raw engine runs into data/index.json + generate programmatic stat pages.

Only publishes numbers backed by recorded runs. Pages appear once a
category+city pair has data from >= 3 runs (variance guardrail).
"""
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).parent.parent
RUNS = ROOT / "data" / "runs"
MIN_RUNS = 3


def extract_names(answer: str):
    """Naive extraction of capitalised business-like names from answers."""
    names = re.findall(r"\*\*([A-Z][A-Za-z0-9 &'.,-]{2,50})\*\*", answer)
    return [n.strip() for n in names][:10]


def main():
    if not RUNS.exists() or not any(RUNS.glob("*.json")):
        print("No runs yet — nothing to aggregate.")
        return

    pair_results = defaultdict(list)
    for f in sorted(RUNS.glob("*.json")):
        data = json.loads(f.read_text())
        for r in data.get("results", []):
            m = re.match(r"(?:best|who should I hire for) (.+?)(?: services)? (?:in|near) (.+)$", r["prompt"])
            if m:
                pair_results[(m.group(1), m.group(2))].append(r)

    index = {"pairs": []}
    pages_dir = ROOT / "content" / "index"
    pages_dir.mkdir(parents=True, exist_ok=True)

    for (category, city), results in sorted(pair_results.items()):
        if len(results) < MIN_RUNS:
            continue
        counts = defaultdict(int)
        total = len(results)
        for r in results:
            for n in set(extract_names(r["answer"])):
                counts[n] += 1
        ranked = sorted(counts.items(), key=lambda kv: -kv[1])[:10]
        slug = f"{category.replace(' ', '-')}-in-{city.lower().replace(', ', '-').replace(' ', '-')}"
        index["pairs"].append({
            "category": category, "city": city, "runs": total,
            "slug": slug,
            "top": [{"name": n, "mention_rate": round(c / total, 2)} for n, c in ranked],
        })

        rows = "\n".join(
            f"| {i+1} | {n} | {round(c/total*100)}% |"
            for i, (n, c) in enumerate(ranked)
        )
        (pages_dir / f"{slug}.md").write_text(f"""---
title: "Who does AI recommend for {category} in {city}?"
description: "We ran {total} recorded AI search tests for {category} in {city}. These businesses get named most often."
type: article
date: 2026-08-16
utm: index_page
---

# Who does AI recommend when asked for a {category} in {city}?

<div class="answer">
<strong>Method:</strong> we asked AI search engines real buyer questions ("best {category} in {city}", "who should I hire for {category} services near {city}?") across {total} recorded test runs. Below: which businesses were named, and how often.
</div>

| Rank | Business | Named in % of answers |
|---|---|---|
{rows}

*Based on {total} recorded runs. AI answers vary between runs — treat as directional, not a ranking.*

## Is your business on this list?

If you're a {category} in {city} and you're not named above, there's a reason — and it's findable. The usual causes: AI crawlers blocked, weak entity signals, or no citable answer on your site. Start with our [five-minute self-check](/articles/why-chatgpt-doesnt-recommend-your-business/), or get the [full one-time diagnostic](https://aicantfindme.com?utm_source=hub&utm_medium=index_page&utm_campaign=hub_cta) with your top 3 blockers and a 12-step fix plan.
""")

    (ROOT / "data" / "index.json").write_text(json.dumps(index, indent=2))
    print(f"Aggregated {len(index['pairs'])} category/city pairs")


if __name__ == "__main__":
    main()
