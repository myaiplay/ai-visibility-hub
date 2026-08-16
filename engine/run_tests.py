#!/usr/bin/env python3
"""Data engine: run buyer-intent prompts through AI engines, record who gets named.

Requires PERPLEXITY_API_KEY (GitHub secret). Exits gracefully without it.
Output: data/runs/YYYY-MM-DD.json
"""
import json
import os
import sys
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).parent.parent
OUT = ROOT / "data" / "runs" / f"{date.today().isoformat()}.json"

# Cap prompts per run to keep API spend ~$5/mo. Expand over time.
MAX_PROMPTS_PER_RUN = 12


def main():
    key = os.environ.get("PERPLEXITY_API_KEY")
    if not key:
        print("PERPLEXITY_API_KEY not set — skipping (engine idle until key added).")
        return

    import requests

    cfg = yaml.safe_load((ROOT / "engine" / "prompts.yaml").read_text())
    prompts = []
    for c in cfg["categories"]:
        for city in cfg["cities"]:
            for t in cfg["templates"]:
                prompts.append(t.format(category=c, city=city))
    # Rotate deterministically so coverage spreads across days
    day = date.today().toordinal()
    rotated = prompts[day % len(prompts):] + prompts[:day % len(prompts)]
    batch = rotated[:MAX_PROMPTS_PER_RUN]

    results = []
    for p in batch:
        try:
            r = requests.post(
                "https://api.perplexity.ai/chat/completions",
                headers={"Authorization": f"Bearer {key}"},
                json={
                    "model": "sonar",
                    "messages": [{"role": "user", "content": p}],
                },
                timeout=60,
            )
            r.raise_for_status()
            data = r.json()
            results.append({
                "engine": "perplexity",
                "prompt": p,
                "answer": data["choices"][0]["message"]["content"],
                "citations": data.get("citations", []),
            })
            print(f"OK: {p}")
        except Exception as e:
            print(f"FAIL: {p} -> {e}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"date": str(date.today()), "results": results}, indent=2))
    print(f"Saved {len(results)} results -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
