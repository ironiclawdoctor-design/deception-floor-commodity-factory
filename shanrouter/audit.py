#!/usr/bin/env python3
"""
ShanRouter Cost Audit Tool — the $75 product.
Takes an OpenRouter usage export (JSON) and shows exactly where money was wasted
by routing expensive models at tasks cheaper models handle fine.

Usage:
  python3 audit.py --input usage_export.json [--output report.md]
  python3 audit.py --demo   # Run on synthetic data to show output format
"""

import json, sys, argparse
from pathlib import Path
from datetime import datetime

REFERRAL_LINK = "https://openrouter.ai/?ref=shananon"

# Cost per 1M tokens (input/output) for common models
MODEL_COSTS = {
    # Expensive — often misrouted
    "anthropic/claude-opus-4":          (15.00, 75.00),
    "anthropic/claude-sonnet-4.6":      (3.00,  15.00),
    "anthropic/claude-3.5-sonnet":      (3.00,  15.00),
    "anthropic/claude-3-opus":          (15.00, 75.00),
    "openai/gpt-4o":                    (2.50,  10.00),
    "openai/gpt-4-turbo":               (10.00, 30.00),
    "openai/o3":                        (10.00, 40.00),
    # Cheap alternatives
    "deepseek/deepseek-chat":           (0.14,  0.28),
    "deepseek/deepseek-chat-v3-0324":   (0.27,  1.10),
    "google/gemma-3-27b-it:free":       (0.0,   0.0),
    "qwen/qwen3-coder:free":            (0.0,   0.0),
    "z-ai/glm-4.5-air:free":            (0.0,   0.0),
    "meta-llama/llama-3.3-70b-instruct":(0.10,  0.10),
    "google/gemini-2.0-flash-001":      (0.10,  0.40),
}

# Task classification by prompt length + model tier
# Short prompts on expensive models = high waste signal
WASTE_THRESHOLDS = {
    "short_on_expensive":   {"max_prompt_tokens": 500,  "min_model_cost": 2.0},
    "medium_on_expensive":  {"max_prompt_tokens": 2000, "min_model_cost": 3.0},
    "repetitive_pattern":   {"min_identical": 3},
}

CHEAP_ALTERNATIVES = {
    "anthropic/claude-sonnet-4.6":  "deepseek/deepseek-chat-v3-0324",
    "anthropic/claude-3.5-sonnet":  "deepseek/deepseek-chat-v3-0324",
    "anthropic/claude-opus-4":      "deepseek/deepseek-chat-v3-0324",
    "openai/gpt-4o":                "google/gemini-2.0-flash-001",
    "openai/gpt-4-turbo":           "deepseek/deepseek-chat",
    "openai/o3":                    "deepseek/deepseek-chat-v3-0324",
}

def cost_per_call(model: str, prompt_tokens: int, completion_tokens: int) -> float:
    costs = MODEL_COSTS.get(model)
    if not costs:
        return 0.0
    return (prompt_tokens * costs[0] + completion_tokens * costs[1]) / 1_000_000

def is_expensive(model: str) -> bool:
    costs = MODEL_COSTS.get(model, (0, 0))
    return costs[0] >= 2.0

def analyze(calls: list) -> dict:
    total_spend = 0.0
    waste_calls = []
    model_breakdown = {}
    
    for call in calls:
        model = call.get("model", "unknown")
        prompt_t = call.get("prompt_tokens", call.get("usage", {}).get("prompt_tokens", 0))
        completion_t = call.get("completion_tokens", call.get("usage", {}).get("completion_tokens", 0))
        actual_cost = cost_per_call(model, prompt_t, completion_t)
        total_spend += actual_cost
        
        # Track by model
        if model not in model_breakdown:
            model_breakdown[model] = {"calls": 0, "spend": 0.0, "tokens": 0}
        model_breakdown[model]["calls"] += 1
        model_breakdown[model]["spend"] += actual_cost
        model_breakdown[model]["tokens"] += prompt_t + completion_t
        
        # Flag waste: expensive model, short prompt
        if is_expensive(model) and prompt_t < 1000:
            alt = CHEAP_ALTERNATIVES.get(model, "deepseek/deepseek-chat")
            alt_cost = cost_per_call(alt, prompt_t, completion_t)
            waste_calls.append({
                "model": model,
                "prompt_tokens": prompt_t,
                "completion_tokens": completion_t,
                "actual_cost": actual_cost,
                "alt_model": alt,
                "alt_cost": alt_cost,
                "waste": actual_cost - alt_cost,
            })
    
    total_waste = sum(c["waste"] for c in waste_calls)
    waste_pct = (total_waste / total_spend * 100) if total_spend > 0 else 0
    
    return {
        "total_calls": len(calls),
        "total_spend": total_spend,
        "total_waste": total_waste,
        "waste_pct": waste_pct,
        "waste_calls": sorted(waste_calls, key=lambda x: x["waste"], reverse=True)[:20],
        "model_breakdown": sorted(model_breakdown.items(), key=lambda x: x[1]["spend"], reverse=True),
    }

def format_report(analysis: dict, period: str = "last 30 days") -> str:
    r = analysis
    lines = [
        f"# ShanRouter LLM Cost Audit",
        f"*Period: {period} | Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}*",
        f"",
        f"## Summary",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Total API calls | {r['total_calls']:,} |",
        f"| Total spend | ${r['total_spend']:.2f} |",
        f"| Identifiable waste | ${r['total_waste']:.2f} |",
        f"| Waste percentage | {r['waste_pct']:.1f}% |",
        f"| Projected annual waste | ${r['total_waste'] * 12:.2f} |",
        f"",
        f"## Spend by Model",
        f"| Model | Calls | Spend | % of Total |",
        f"|-------|-------|-------|------------|",
    ]
    
    for model, data in r["model_breakdown"][:10]:
        pct = (data["spend"] / r["total_spend"] * 100) if r["total_spend"] > 0 else 0
        lines.append(f"| `{model}` | {data['calls']:,} | ${data['spend']:.4f} | {pct:.1f}% |")
    
    if r["waste_calls"]:
        lines += [
            f"",
            f"## Top Waste Opportunities",
            f"These calls used expensive models for short prompts — prime candidates for cheaper routing.",
            f"",
            f"| Model Used | Prompt Tokens | Cost | Better Option | Savings |",
            f"|-----------|--------------|------|---------------|---------|",
        ]
        for c in r["waste_calls"][:10]:
            lines.append(
                f"| `{c['model']}` | {c['prompt_tokens']:,} | "
                f"${c['actual_cost']:.5f} | `{c['alt_model']}` | "
                f"${c['waste']:.5f} |"
            )
    
    lines += [
        f"",
        f"## What ShanRouter Would Have Done",
        f"With intelligent tier routing, estimated spend: **${r['total_spend'] - r['total_waste']:.2f}**",
        f"Monthly savings: **${r['total_waste']:.2f}** ({r['waste_pct']:.0f}% reduction)",
        f"Annual savings: **${r['total_waste'] * 12:.2f}**",
        f"",
        f"## Next Steps",
        f"1. Install ShanRouter in your stack (drop-in OpenRouter replacement)",
        f"2. Set routing rules: short prompts (<500 tokens) → DeepSeek tier",
        f"3. Reserve Claude/GPT-4 for complex reasoning, architecture, security",
        f"",
        f"---",
        f"*Audit by ShanRouter — the Dollar Agency's internal LLM router.*",
        f"*If this saved you money, consider signing up for OpenRouter via our referral:*",
        f"*{REFERRAL_LINK}*",
    ]
    
    return "\n".join(lines)

def demo_data() -> list:
    """Generate synthetic usage data that shows realistic waste patterns."""
    import random
    calls = []
    models_weighted = [
        ("anthropic/claude-sonnet-4.6", 40),
        ("openai/gpt-4o", 20),
        ("deepseek/deepseek-chat", 25),
        ("google/gemini-2.0-flash-001", 15),
    ]
    for _ in range(200):
        model = random.choices(
            [m for m, _ in models_weighted],
            weights=[w for _, w in models_weighted]
        )[0]
        # Short prompts are common waste signal
        prompt_t = random.choice([50, 100, 200, 300, 500, 1000, 2000, 4000])
        completion_t = random.randint(50, min(prompt_t, 500))
        calls.append({
            "model": model,
            "prompt_tokens": prompt_t,
            "completion_tokens": completion_t,
        })
    return calls

def main():
    parser = argparse.ArgumentParser(description="ShanRouter Cost Audit")
    parser.add_argument("--input", help="OpenRouter usage export JSON file")
    parser.add_argument("--output", help="Output report file (default: stdout)")
    parser.add_argument("--demo", action="store_true", help="Run on demo data")
    args = parser.parse_args()
    
    if args.demo:
        calls = demo_data()
        period = "demo data (200 synthetic calls)"
    elif args.input:
        with open(args.input) as f:
            data = json.load(f)
        # Handle both list and {data: [...]} formats
        calls = data if isinstance(data, list) else data.get("data", data.get("calls", []))
        period = Path(args.input).stem
    else:
        print("Usage: audit.py --input usage.json OR --demo")
        sys.exit(1)
    
    analysis = analyze(calls)
    report = format_report(analysis, period)
    
    if args.output:
        Path(args.output).write_text(report)
        print(f"Report written to {args.output}")
    else:
        print(report)

if __name__ == "__main__":
    main()
