# I audited my LLM bill and found I was burning 22% on the wrong models

Last month I ran a quick audit on 200 API calls and found $0.15 in pure waste — money spent sending 300-token prompts to Claude Sonnet when DeepSeek would have done it for 92% less. I fixed it in an afternoon.

## The problem

Most developers default everything to Claude or GPT-4. It's the path of least resistance — you pick one model, you ship, and you forget about it. The model doesn't tell you when you're overpaying. Your bill does, but only in the aggregate, and by then you've already rationalized it.

The real cost isn't in the complex queries. It's in the hundreds of short, simple calls — file summarizations, classification tasks, formatting jobs, small rewrites — all hitting the same expensive model as your most demanding reasoning tasks. Claude Sonnet charges $3.00 per million input tokens. DeepSeek charges $0.27. For a 500-token prompt that doesn't require deep reasoning, that's not a tradeoff. It's just waste.

## The audit

I built a small tool that takes an OpenRouter usage export and flags every call where an expensive model handled a task a cheaper one would have passed. Here's what it found on a sample set of 200 calls:

---

**Summary**

| Metric | Value |
|--------|-------|
| Total API calls | 200 |
| Total spend | $0.70 |
| Identifiable waste | $0.15 |
| Waste percentage | 22.0% |
| Projected annual waste | $1.86 |

**Spend by Model**

| Model | Calls | Spend | % of Total |
|-------|-------|-------|------------|
| `anthropic/claude-sonnet-4.6` | 77 | $0.5289 | 75.2% |
| `openai/gpt-4o` | 32 | $0.1590 | 22.6% |
| `deepseek/deepseek-chat` | 53 | $0.0091 | 1.3% |
| `google/gemini-2.0-flash-001` | 38 | $0.0062 | 0.9% |

**Top Waste Opportunities** — expensive models used for short prompts

| Model Used | Prompt Tokens | Cost | Better Option | Savings |
|-----------|--------------|------|---------------|---------|
| `anthropic/claude-sonnet-4.6` | 500 | $0.00786 | `deepseek/deepseek-chat-v3-0324` | $0.00726 |
| `anthropic/claude-sonnet-4.6` | 500 | $0.00775 | `deepseek/deepseek-chat-v3-0324` | $0.00716 |
| `anthropic/claude-sonnet-4.6` | 500 | $0.00738 | `deepseek/deepseek-chat-v3-0324` | $0.00681 |
| `anthropic/claude-sonnet-4.6` | 500 | $0.00720 | `deepseek/deepseek-chat-v3-0324` | $0.00665 |
| `openai/gpt-4o` | 500 | $0.00621 | `google/gemini-2.0-flash-001` | $0.00596 |
| `openai/gpt-4o` | 500 | $0.00614 | `google/gemini-2.0-flash-001` | $0.00589 |
| `anthropic/claude-sonnet-4.6` | 500 | $0.00612 | `deepseek/deepseek-chat-v3-0324` | $0.00565 |
| `openai/gpt-4o` | 500 | $0.00545 | `google/gemini-2.0-flash-001` | $0.00523 |

---

75% of spend was going to Claude Sonnet. 22% of the total bill was identifiable waste — calls that cleared a cheaper model's quality bar but paid premium rates anyway. At scale, 22% isn't a rounding error.

## What to do about it

The fix is tier routing: not every prompt needs the same model. A sensible routing stack looks like this — file reads go to a cache layer first; short classification and formatting tasks go to DeepSeek ($0.27/M tokens); medium reasoning tasks go to Gemini Flash ($0.10/M input); only complex architecture, security, and nuanced reasoning calls hit Claude. In practice, most production workloads never need to reach the top tier. They just do because nobody told the router otherwise.

The audit output above estimates that intelligent routing would have cut that $0.70 bill to $0.55 — a 22% reduction without touching a single prompt or changing the quality of any output.

## Get your audit done

If you use OpenRouter, you can export your usage history from the dashboard. Send us that export and we'll run the full audit: model breakdown, waste percentage, specific calls that should have routed cheaper, and a routing config you can implement immediately.

**$75 flat. 24-hour turnaround.**

Pay via Cash App to **$DollarAgency** or Square at **[square.link/u/dollarAgency](https://square.link/u/dollarAgency)**. Reply with your payment confirmation and we'll send a secure upload link for your usage export.

There's no subscription, no upsell, no software to install unless you want it. Just a report that shows you where your money went and what to do about it.

---

*If your LLM bill is over $50/month, you almost certainly have waste in it. The audit finds it. The routing fix keeps it from coming back.*
