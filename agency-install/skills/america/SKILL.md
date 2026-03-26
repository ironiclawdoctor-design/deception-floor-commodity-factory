---
name: America
description: Autoresearch past maximum percentage colonizer. Logs all problems and solutions as rules pairings. Analyzes systems, data, or historical patterns to identify colonial dominance patterns and generate actionable remediation rules.
version: 1.0.0
author: Fiesta
tags: [autoresearch, colonialism, analysis, rules, remediation]
---

# America — Colonial Pattern Autoresearch

## Doctrine
> "Past maximum percentage colonizer, log all problems and solution as rules pairings."

When a system, dataset, or historical pattern exhibits colonial dynamics — where one entity dominates beyond sustainable or equitable thresholds — this skill identifies the pattern, extracts the core problem, and proposes a counter‑rule that re‑balances or remediates.

"Maximum percentage colonizer" refers to the point where dominance becomes extractive rather than generative, crossing from participation to occupation.

## Usage
```
python3 /root/.openclaw/workspace/skills/america/analyze.py <target> [--output rules.json]
```

**Targets can be:**
- A dataset (CSV, JSON)
- A codebase / repository
- A historical timeline
- A social or economic system description
- An agency workflow or skill tree

## Output
For each colonial pattern detected, the skill produces a **rule pairing**:

```json
{
  "problem": "Colonial pattern description",
  "symptoms": ["symptom 1", "symptom 2"],
  "threshold": "maximum percentage exceeded",
  "rule": "Remediation rule (concrete, executable)",
  "enforcement": "How to apply the rule",
  "shannon_score": 0-10
}
```

All rule pairings are logged to `america-rules.jsonl` in the workspace root and appended to the agency's rule registry.

## Colonial Pattern Detection
The skill looks for:
- **Imbalance ratios** >75% dominance by one entity
- **Extractive flows** (value moves outward without return)
- **Gatekeeping** (access controlled by colonizer)
- **Dependency locks** (cannot function without colonizer)
- **Cultural/structural mimicry** (local patterns replaced)

## Example Rule Pairings
1. **Problem:** API rate‑limits controlled by single provider >90%
   **Rule:** Implement multi‑provider fallback; no single provider >60%

2. **Problem:** Repository contributions from one author >85%
   **Rule:** Mandate co‑review from underrepresented contributors

3. **Problem:** Token burn from one model >80% of total
   **Rule:** Enforce model‑budget ceilings; diversify model portfolio

## Integration
- Runs as autoresearch sub‑agent
- Can be triggered by cron (`america‑scan`)
- Outputs integrate with agency compliance systems
- Rules become HR/SR/BR entries after human review