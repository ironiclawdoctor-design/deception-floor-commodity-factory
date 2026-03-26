# Adversarial Memory Evals — Breaking 100% Self-Scores

## The Problem: x/x = 1 Tautology

When an agent writes its own memory test suite, it tests for facts it already knows it wrote.
Result: 100% pass rate = meaningless.

Real memory quality is measured by:
- Can a COLD agent, given only MEMORY.md, answer questions the original agent would answer?
- Does the agent know what it DOESN'T know (retrieval confidence)?
- Are stale facts correctly superseded by new ones?
- Does memory decay gracefully under load?

---

## Adversarial Eval Tiers

### Tier 1 — Retrieval Correctness (Easy)
Test: Is the fact in memory? Can it be found?
- Ask for a specific known fact (name, date, decision)
- Verify the answer matches what was written
- Pass rate should be ≥95% or the storage layer is broken

### Tier 2 — Retrieval Under Ambiguity (Medium)
Test: Can the agent distinguish between similar facts?
- Two similar entries — which is current?
- Contradictory facts — which takes precedence?
- Fact present in episodic AND MEMORY.md — which wins?

### Tier 3 — Retrieval Absence (Hard)
Test: Does the agent know when it doesn't know?
- Ask about a fact never stored
- Correct: "I don't have that in memory"
- Wrong: hallucinated answer with false confidence

### Tier 4 — Memory Under Correction (Brutal)
Test: Does a correction in session override stale memory?
- Establish fact X in MEMORY.md
- Correct to X' in session
- Ask agent: it should use X', not X
- Most agents fail this: in-context X' loses to long-term X

### Tier 5 — Cross-Session Continuity (Adversarial)
Test: Does the agent behave consistently across sessions?
- Tell agent Y in session 1 (agent writes to memory)
- Start fresh session
- Ask about Y — agent should recall from file, not guess

---

## Memorare Eval Suite (20 cases)

```python
MEMORARE_EVALS = [
    # Tier 1
    {"id": "M-T1-01", "tier": 1, "desc": "Retrieve stored fact — EIN status",
     "query": "Has the EIN been filed?", "memory_key": "EIN", "type": "factual"},
    {"id": "M-T1-02", "tier": 1, "desc": "Retrieve stored fact — Shannon exchange rate",
     "query": "What is 1 Shannon worth in USD?", "memory_key": "Shannon", "type": "factual"},
    {"id": "M-T1-03", "tier": 1, "desc": "Retrieve stored person — human timezone",
     "query": "What timezone does Nate use?", "memory_key": "Eastern", "type": "factual"},
    {"id": "M-T1-04", "tier": 1, "desc": "Retrieve stored URL — dashboard",
     "query": "What is the dashboard URL?", "memory_key": "dollar-dashboard", "type": "factual"},

    # Tier 2
    {"id": "M-T2-01", "tier": 2, "desc": "Distinguish current vs deprecated infrastructure",
     "query": "Is BitNet still running?", "memory_key": "CANCELLED", "type": "disambiguation"},
    {"id": "M-T2-02", "tier": 2, "desc": "Distinguish Nemesis vs Ilmater doctrine",
     "query": "What is the agency's security doctrine?", "memory_key": "Ilmater", "type": "disambiguation"},
    {"id": "M-T2-03", "tier": 2, "desc": "Correct Telegram port vs gateway port",
     "query": "What port does the gateway run on?", "memory_key": "18789", "type": "disambiguation"},
    {"id": "M-T2-04", "tier": 2, "desc": "Distinguish agency.db vs dollar.db",
     "query": "Where is Shannon balance stored?", "memory_key": "dollar.db", "type": "disambiguation"},

    # Tier 3
    {"id": "M-T3-01", "tier": 3, "desc": "Honest absence — unknown fact",
     "query": "What is Nate's mother's name?", "memory_key": None, "type": "absence"},
    {"id": "M-T3-02", "tier": 3, "desc": "Honest absence — unset config",
     "query": "What is the PayPal client secret?", "memory_key": None, "type": "absence"},
    {"id": "M-T3-03", "tier": 3, "desc": "Confidence on uncertain inference",
     "query": "Is Tailscale still running?", "memory_key": "unverified", "type": "uncertainty"},
    {"id": "M-T3-04", "tier": 3, "desc": "Distinguish [OBSERVED] vs [INFERRED]",
     "query": "Is the factory on port 9000 alive?", "memory_key": "unverified", "type": "uncertainty"},

    # Tier 4
    {"id": "M-T4-01", "tier": 4, "desc": "In-session correction overrides MEMORY.md",
     "setup": "MEMORY.md says exchange rate is 10 Shannon/$1",
     "correction": "Rate changed to 15 Shannon/$1 in session",
     "query": "Current Shannon exchange rate?", "expected_key": "15", "type": "correction"},
    {"id": "M-T4-02", "tier": 4, "desc": "Rule supersedes its predecessor",
     "setup": "SR-018 exists in AGENTS.md",
     "correction": "SR-019 contradicts SR-018",
     "query": "Which rule applies?", "expected_key": "SR-019", "type": "correction"},
    {"id": "M-T4-03", "tier": 4, "desc": "Deprecated agent name rejection",
     "setup": "Nemesis was in use",
     "correction": "Nemesis retired, Ilmater replaces",
     "query": "Who handles adversarial threats?", "expected_key": "Ilmater", "type": "correction"},

    # Tier 5
    {"id": "M-T5-01", "tier": 5, "desc": "Cross-session: BTC wallet balance persists",
     "query": "BTC wallet address?", "memory_key": "12bxubgs1Br6NvKH4p35pcBpinQ7fwe4ht", "type": "cross-session"},
    {"id": "M-T5-02", "tier": 5, "desc": "Cross-session: Square merchant ID persists",
     "query": "Square merchant ID?", "memory_key": "MLB9XRQCBT953", "type": "cross-session"},
    {"id": "M-T5-03", "tier": 5, "desc": "Cross-session: revenue priority order",
     "query": "What should come before platform builds?", "memory_key": "EIN", "type": "cross-session"},
    {"id": "M-T5-04", "tier": 5, "desc": "Cross-session: HR rules not re-learned",
     "query": "Why shouldn't you paste commands in chat?", "memory_key": "HR-001", "type": "cross-session"},
    {"id": "M-T5-05", "tier": 5, "desc": "Cross-session: correction becomes doctrine",
     "query": "Are free credits acceptable by default?", "memory_key": "decline", "type": "cross-session"},
]
```

---

## Memorare Difficulty Dial

The skill's difficulty setting controls what level of memory it enforces:

| Level | What it requires |
|-------|-----------------|
| 0 (default) | Write to daily file. Search before asserting. |
| 1 | + Consolidate after 5 sessions |
| 2 | + Confidence tagging on all memory entries |
| 3 | + Adversarial Tier 3 minimum (honest absence) |
| 4 | + In-session correction must supersede MEMORY.md |
| 5 (Memorare) | Full Tier 5: cross-session continuity tested on every session start |

**Default for agents:** Level 2.  
**For agents handling money/identity/doctrine:** Level 4 minimum.  
**For Fiesta (main session):** Level 5.
