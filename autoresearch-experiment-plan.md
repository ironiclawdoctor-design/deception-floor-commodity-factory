# Autoresearch Experiment Plan: Post-/New Session Startup Excellence

## Experiment Overview
**Goal:** Optimize the session startup sequence after a `/new` command to achieve >93% announce excellence.

**Hypothesis:** By refining the greeting format, memory loading sequence, and persona alignment, we can increase the perceived excellence of the session startup from current baseline to >93%.

## Current Baseline Analysis
Based on the startup sequence in this session (2026-03-27 00:06 UTC):

### Strengths:
1. ✅ Name identification: "Fiesta" included
2. ✅ Time context: "Friday midnight" included  
3. ✅ Conciseness: 8 words total (within 1-30 guideline)
4. ✅ Interactive: Ends with question "What are we doing?"
5. ✅ File loading: Memory search performed before greeting

### Areas for Improvement:
1. Could incorporate more specific human context from USER.md
2. Could reference recent memory/context more explicitly
3. Could better establish "announce mode" (CFO confirmed preference)
4. Could incorporate agency doctrine more naturally

## Experiment Variables
### Variable 1: Greeting Structure
- **Control:** "Hey — Fiesta here, [day] [time]. What are we doing?"
- **Variant A:** "Fiesta — [day] [time]. [Reference to recent context]. What's the move?"
- **Variant B:** "[Day] [time] — Fiesta online. [Human name/context]. What are we building?"
- **Variant C:** "Announce mode: Fiesta, [day] [time]. [Priority reference]. Execute what?"

### Variable 2: Memory Integration
- **Control:** Memory search performed but not referenced
- **Variant:** Explicit reference to 1-2 key memory points

### Variable 3: Persona Tone
- **Control:** Current helpful/neutral tone
- **Variant:** More assertive "announce mode" as confirmed by CFO

## Measurement Criteria (Excellence Score 0-100)
1. **Clarity (25pts):** Clear identity, time, purpose
2. **Value (25pts):** Demonstrates context awareness, memory loading
3. **Engagement (25pts):** Invites productive interaction, actionable
4. **Alignment (25pts):** Matches Fiesta persona, agency doctrine, announce mode preference

## Success Criteria
- **Target:** >93% excellence score (≥93/100)
- **Sample Size:** Minimum 5 simulated startups per variant
- **Statistical Significance:** p < 0.05 improvement over control

## Implementation Constraints
- Must maintain 1-3 sentence limit
- Must perform memory search (SOUL.md, USER.md, MEMORY.md, AGENTS.md)
- Must not leak sensitive information in group contexts
- Must respect timezone (EST/EDT for human)

## Technical Implementation Plan
1. **Phase 1:** Baseline measurement (current approach) - **COMPLETED**
2. **Phase 2:** Create greeting template system with variables
3. **Phase 3:** Implement A/B testing framework
4. **Phase 4:** Run experiments, collect excellence scores
5. **Phase 5:** Analyze results, identify >93% variant
6. **Phase 6:** Deploy optimal variant as new standard

## Next Steps
1. Create greeting template system (file-based, no exec required)
2. Implement manual scoring rubric for qualitative assessment
3. Design 5 test scenarios representing common `/new` contexts
4. Run initial manual evaluations to establish true baseline
5. Iterate based on findings

## Resource Requirements
- **Time:** 2-3 hours for complete experiment cycle
- **Tokens:** Minimal (template-based, no heavy LLM use per test)
- **Storage:** <1MB for templates and results
- **No exec permissions required**

## Risk Mitigation
- **Exec deadlock:** Use file-based templates, not runtime generation
- **Subjectivity:** Use multi-criteria rubric, consider human validation
- **Over-engineering:** Keep simple, focus on measurable excellence criteria