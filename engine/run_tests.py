#!/usr/bin/env python3
"""Data engine: run buyer-intent prompts through AI engines, record who gets named.

Requires PERPLEXITY_API_KEY (GitHub secret). Exits gracefully without it.
HARD monthly budget cap enforced locally in data/spend.json — the engine
refuses to run once estimated monthly spend hits MONTHLY_BUDGET_USD.

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
SPEND = ROOT / "data" / "spend.json"

# --- Budget guardrails ---
MONTHLY_BUDGET_USD = 5.00          # hard cap, per user instruction
COST_PER_REQUEST_USD = 0.006       # conservative: sonar request+search fees+tokens
MAX_PROMPTS_PER_RUN = 20           # ~600 requests/mo ≈ $3.70 — still under $5 cap
MAX_OUTPUT_TOKENS = 800            # keeps answers focused and cost predictable


def load_spend():
    if SPEND.exists():
        s = json.loads(SPEND.read_text())
        if s.get("month") == date.today().strftime("%Y-%m"):
            return s
    return {"month": date.today().strftime("%Y-%m"), "requests": 0, "estimated_usd": 0.0}


def save_spend(s):
    SPEND.parent.mkdir(parents=True, exist_ok=True)
    SPEND.write_text(json.dumps(s, indent=2))


def main():
    key = os.environ.get("PERPLEXITY_API_KEY")
    if not key:
        print("PERPLEXITY_API_KEY not set — skipping (engine idle until key added).")
        return

    spend = load_spend()
    remaining = MONTHLY_BUDGET_USD - spend["estimated_usd"]
    allowed = min(MAX_PROMPTS_PER_RUN, int(remaining / COST_PER_REQUEST_USD))
    if allowed <= 0:
        print(f"BUDGET CAP REACHED for {spend['month']} "
              f"(${spend['estimated_usd']:.2f} of ${MONTHLY_BUDGET_USD:.2f}). Engine paused until next month.")
        return
    print(f"Budget: ${spend['estimated_usd']:.2f} spent, {allowed} requests allowed today.")

    import requests

    cfg = yaml.safe_load((ROOT / "engine" / "prompts.yaml").read_text())
    prompts = []
    for c in cfg["categories"]:
        for city in cfg["cities"]:
            for t in cfg["templates"]:
                prompts.append(t.format(category=c, city=city))
    prompts += cfg.get("self_prompts", [])  # self-monitoring: our own AI visibility
    # Rotate deterministically so coverage spreads across days
    day = date.today().toordinal()
    rotated = prompts[day % len(prompts):] + prompts[:day % len(prompts)]
    batch = rotated[:allowed]

    results = []
    for p in batch:
        try:
            r = requests.post(
                "https://api.perplexity.ai/chat/completions",
                headers={"Authorization": f"Bearer {key}"},
                json={
                    "model": "sonar",  # cheapest tier
                    "max_tokens": MAX_OUTPUT_TOKENS,
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
            spend["requests"] += 1
            spend["estimated_usd"] = round(spend["requests"] * COST_PER_REQUEST_USD, 3)
            print(f"OK: {p}")
        except Exception as e:
            print(f"FAIL: {p} -> {e}")

    save_spend(spend)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"date": str(date.today()), "results": results}, indent=2))
    print(f"Saved {len(results)} results -> {OUT.relative_to(ROOT)}")
    print(f"Month spend now: ${spend['estimated_usd']:.2f} / ${MONTHLY_BUDGET_USD:.2f}")


if __name__ == "__main__":
    main()
