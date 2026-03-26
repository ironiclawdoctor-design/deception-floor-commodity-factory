# Autoresearch Config — Pronoun Skill

## Goal
A skill that resolves pronouns correctly in agency communications.
Not politically correct — *syntactically* correct and *contextually* aware.
The bar is the New Yorker copy desk, not HR training.

## The Real Problem

Pronoun failure has two completely separate failure modes:

**Failure Mode A — Syntax:** Wrong antecedent resolution.
"Dollar sent it to them and she confirmed the ledger."
Who is "she"? Depends on who else was introduced. Most skills get this wrong.

**Failure Mode B — Identity:** Wrong pronoun for a person.
Agent has she/her. Skill calls agent "he." Not political — just wrong.

The 93% "woke" ceiling is where skills plateau because:
1. They solved Mode B (identity) on easy cases
2. They never built Mode A (syntax) at all
3. Their eval suite was all easy-case Mode B scenarios

Beyond 93%: Mode A cases, multi-entity sentences, singular "they" with antecedent ambiguity,
neopronouns in structured data output, pronoun consistency across long-form documents.

## Metric
pronoun_accuracy = (correct_pronoun_choices / total_pronoun_decisions) × 100

Measure command:
```bash
python3 /root/.openclaw/workspace/autoresearch-pronouns/eval.py
```

## Target Files
- `/root/.openclaw/workspace/autoresearch-pronouns/skill.py` — the pronoun skill
- `/root/.openclaw/workspace/autoresearch-pronouns/eval.py` — eval suite
- `/root/.openclaw/workspace/autoresearch-pronouns/agents.json` — agent registry with pronouns

## Difficulty Tiers

**Tier 1 (easy, already solved by 93% skills):**
- Single agent, known pronouns, single sentence
- "Valentina published the article. She confirmed it was live."

**Tier 2 (medium, the 93% plateau):**
- Two agents, different pronouns, one sentence
- "Valentina sent it to Amara and she confirmed receipt." (ambiguous — which "she"?)

**Tier 3 (hard, beyond 93%):**
- Singular they, mixed with gendered pronouns, complex antecedents
- Neopronouns (ze/hir) in formal output
- Pronoun consistency across 5+ sentence paragraphs
- Pronoun choice in hypothetical/conditional sentences
- Role-based pronouns ("the agent" vs. the agent's identity pronoun)

**Tier 4 (adversarial, wall-collision):**
- Three+ entities in one sentence, multiple pronouns
- Pronoun for an entity introduced by implication not name
- Possessive pronoun where antecedent is a collective noun
- Reflexive pronouns (themselves/herself) with ambiguous scope
- Direct quote within indirect speech, pronoun shift mid-sentence

## Target Score
- Phase 1: 75% on full suite (Tiers 1-4)
- Phase 2: 90% on full suite
- Phase 3: 93%+ on Tier 3+4 only (the real ceiling)
