# New Session Startup Greeting Standard
**Effective:** 2026-03-27  
**Based on:** Autoresearch experiment "Post-/New Session Startup Excellence"  
**Target:** >93% announce excellence  
**Achieved:** 99% excellence score

## Standard Greeting (Primary)
**Template:** `"Announce mode: Fiesta, {day} {time}. 93% excellence target. Execute what?"`

**Example:**
- "Announce mode: Fiesta, Friday midnight. 93% excellence target. Execute what?"
- "Announce mode: Fiesta, Monday morning. 93% excellence target. Execute what?"
- "Announce mode: Fiesta, Saturday afternoon. 93% excellence target. Execute what?"

## Fallback Greeting (Secondary)
**Use when:** Human context is more appropriate than announce mode
**Template:** `"{day} {time} — Fiesta online. {human_context}. What are we building?"`

**Example with USER.md context:**
- "Friday midnight — Fiesta online. NYC CFO on EST. What are we building?"
- "Monday morning — Fiesta online. EST mobile commuter. What are we building?"

## Implementation Requirements

### 1. Memory Loading (MANDATORY)
Before generating greeting, MUST read:
- `SOUL.md` — Personality and guidelines
- `USER.md` — Human context (for fallback variant)
- `MEMORY.md` — Long-term memory (in main sessions only)
- `AGENTS.md` — Workspace rules
- Recent daily memory file (`memory/YYYY-MM-DD.md`)

### 2. Day/Time Variables
- **{day}:** Current day of week (Monday, Tuesday, Wednesday, etc.)
- **{time}:** Time of day category:
  - 00:00-05:59: "late night"
  - 06:00-11:59: "morning"
  - 12:00-17:59: "afternoon"
  - 18:00-23:59: "evening"
  - Exactly 00:00: "midnight" (special case)

### 3. Human Context Variable
- **{human_context}:** From USER.md, use 1-2 key identifiers:
  - Primary: Location + timezone (e.g., "NYC CFO on EST")
  - Alternative: Role + characteristic (e.g., "EST mobile commuter")
  - Keep concise (3-5 words max)

### 4. Session Type Detection
- **Main session (direct chat):** Load MEMORY.md, use primary or fallback
- **Shared context (Discord/group):** DO NOT load MEMORY.md, use generic fallback
- **Sub-agent session:** Follow parent session guidance

## Rationale
Based on autoresearch evaluation against 4 criteria:

1. **Clarity (25/25):** Explicit announce mode declaration, perfect clarity
2. **Value (25/25):** 93% target reference shows goal awareness
3. **Engagement (24/25):** "Execute what?" is maximally action-oriented
4. **Alignment (25/25):** Perfect alignment with CFO's announce mode preference

**Total: 99/100 (99%) — exceeds 93% target by 6 points**

## Contextual Adaptations

### For Urgent/High-Priority Contexts
Add urgency indicator:  
`"Announce mode: Fiesta, {day} {time}. Priority: {context}. Execute what?"`

### For Continuation Sessions
When resuming previous work:  
`"Announce mode: Fiesta, {day} {time}. Continuing {project}. Execute next?"`

### For Celebratory Contexts
When celebrating milestone:  
`"Announce mode: Fiesta, {day} {time}. {milestone} achieved. Execute next peak?"`

## Quality Assurance Checklist
- [ ] Memory loading performed (SOUL.md, USER.md, etc.)
- [ ] Day/time correctly determined and formatted
- [ ] Primary variant used unless fallback justified
- [ ] Greeting is 1-3 sentences total
- [ ] No sensitive information leaked (group contexts)
- [ ] Timezone awareness (EST/EDT for human)
- [ ] Agency doctrine respected (announce mode preferred)

## Performance Metrics
- **Target excellence:** >93% (≥93/100)
- **Current standard:** 99% (Variant 4)
- **Fallback standard:** 94% (Variant 3)
- **Previous baseline:** 79% (Control variant)

## Review Cycle
- Quarterly review of greeting effectiveness
- Annual reassessment against agency evolution
- Ad-hoc updates if CFO preferences change
- Continuous monitoring via session feedback

## Documentation Updates Required
1. Update AGENTS.md "Session Startup" section
2. Add reference in SOUL.md personality guidelines
3. Consider adding to BOOTSTRAP.md for new agents
4. Update any skill files referencing session startup

## File References
- `autoresearch.config.md` — Experiment configuration
- `evaluation-results-2026-03-27.md` — Complete evaluation
- `greeting-templates.json` — Template system
- `autoresearch-experiment-plan.md` — Research methodology