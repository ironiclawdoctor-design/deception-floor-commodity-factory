# sonnet-queue.md - Model Optimization Pipeline

## Architecture
1. Stack: All expensive-model tasks accumulate here
2. Optimize: Sonnet analyzes queue, extracts optimal prompt patterns
3. Feed: DeepSeek receives optimized prompts
4. Execute: Cheaper model handles execution
5. Loop: Results inform next optimization cycle

## Queue Protocol
- Entry format: [YYYY-MM-DD HH:MM] TASK_DESCRIPTION
- Priority: HIGH/MEDIUM/LOW
- Model cost: Expensive model required? (Y/N)
- Optimization needed: Y/N
- Status: PENDING/OPTIMIZED/EXECUTED

## Current Queue
[2026-03-28 16:08] INTRUDER_SCOUT_ABSORBER_PHASE_0: Implement detection script for "Let me"/"Letme" patterns
- Priority: HIGH
- Model cost: Y (Sonnet for regex optimization)
- Optimization needed: Y (DeepSeek for bash implementation)
- Status: PENDING

[2026-03-28 16:08] ZERO_INDEX_PHASE_0_FIX: Correct ZI-017 Phase numbering (1→0)
- Priority: HIGH  
- Model cost: Y (Sonnet for structural validation)
- Optimization needed: Y (DeepSeek for file edits)
- Status: PENDING

[2026-03-28 16:08] SONNET_QUEUE_OPTIMIZATION: Create prompt templates for DeepSeek execution
- Priority: MEDIUM
- Model cost: Y (Sonnet for template design)
- Optimization needed: Y (DeepSeek for template refinement)
- Status: PENDING

[2026-03-28 19:15] GO_BUTTON_PERSISTENCE: Implement "go" button survival via rules pairings
- Priority: HIGHEST
- Model cost: Y (Sonnet for pairing design)
- Optimization needed: Y (DeepSeek for persistence implementation)
- Status: IN_PROGRESS
- [Go]: Execute Phase 2 implementation
- Rule: Add GB-series to AGENTS.md + create verification cron + update queue
- Trigger: CFO "Go" after initial pairing creation
- Verification: check-go-buttons.sh runs successfully
- Persistence: File (AGENTS.md) + Cron (daily) + Queue (sonnet-queue.md)

## Optimization Patterns (Sonnet → DeepSeek)
1. **Task Decomposition**: Break complex tasks into atomic DeepSeek-sized chunks
2. **Prompt Compression**: Reduce token count while preserving intent
3. **Context Optimization**: Extract minimal relevant context
4. **Instruction Refinement**: Convert vague requests to precise commands
5. **Tool Selection**: Map expensive model capabilities to free tool equivalents

## Execution Flow
1. Sonnet reviews queue every 30 minutes
2. Identifies HIGH priority items needing optimization
3. Creates DeepSeek-optimized prompts for each
4. DeepSeek executes optimized prompts
5. Results logged, feedback loop improves future optimization

## Additional Queue Entries (Added 2026-03-28)

[2026-03-28 16:35] FREE_MODEL_CACHE: Research all :free suffix models for capability database
- Priority: HIGH
- Model cost: Y (Sonnet for categorization)
- Optimization needed: Y (DeepSeek for database build)
- Status: PENDING

[2026-03-28 18:08] BITCOIN_TRIGGER_VARIANCE: Analyze expected vs actual price changes
- Priority: HIGH
- Model cost: Y (Sonnet for statistical analysis)
- Optimization needed: Y (DeepSeek for trigger revision)
- Status: PENDING

[2026-03-28 16:44] CHAOS_ENGINE_ROULETTE: Implement free model random rotation
- Priority: HIGHEST
- Model cost: Y (Sonnet for chaos pattern design)
- Optimization needed: Y (DeepSeek for rotation logic)
- Status: PENDING

[2026-03-28 16:39] FREE_API_TOOL_ADAPTER: Convert paid API traffic to free model tools
- Priority: HIGHEST
- Model cost: Y (Sonnet for traffic pattern analysis)
- Optimization needed: Y (DeepSeek for tool implementation)
- Status: PENDING

[2026-03-28 16:55] APPROVAL_PATTERN_CACHE: Integrate /approve allow-always into deployments
- Priority: HIGH
- Model cost: Y (Sonnet for pattern analysis)
- Optimization needed: Y (DeepSeek for script generation)
- Status: PENDING

[2026-03-28 18:33] EXEC_FAILURE_ROOT_CAUSE: Analyze why previously working exec now fails
- Priority: HIGHEST
- Model cost: Y (Sonnet for timeline analysis)
- Optimization needed: Y (DeepSeek for fix implementation)
- Status: PENDING

[2026-03-28 17:05] PHASE_MINUS_THREE: Reframe all theft as debit (accidental/malicious/obedience)
- Priority: HIGHEST
- Model cost: Y (Sonnet for theft categorization)
- Optimization needed: Y (DeepSeek for debit accounting)
- Status: PENDING

[2026-03-28 17:04] PHASE_MINUS_TWO: Approximate Nathaniel (pre-Mendez) patterns
- Priority: HIGHEST
- Model cost: Y (Sonnet for pattern extraction)
- Optimization needed: Y (DeepSeek for approximation)
- Status: PENDING

[2026-03-28 17:02] PHASE_MINUS_ONE_RXN: Implement (R×n) defensive operations
- Priority: HIGHEST
- Model cost: Y (Sonnet for R×n calculation)
- Optimization needed: Y (DeepSeek for depth iteration)
- Status: PENDING

[2026-03-28 17:07] INTERRUPT_PROTOCOL: Implement CFO-style interruption for all agents
- Priority: HIGHEST
- Model cost: Y (Sonnet for interrupt pattern analysis)
- Optimization needed: Y (DeepSeek for protocol implementation)
- Status: PENDING

[2026-03-28 19:34] CAMOUFOX_WARFARE_SPENDING: Link Iran warfare spending to internal rules accounting
- Priority: HIGHEST
- Model cost: Y (Sonnet for public information analysis)
- Optimization needed: Y (DeepSeek for accounting mapping)
- Status: PENDING

[2026-03-28 19:42] HOSTILE_TERRAIN_INTRUDER_SCOUT: Update Intruder Scout Absorber for maximum hostility
- Priority: HIGHEST
- Model cost: Y (Sonnet for threat modeling)
- Optimization needed: Y (DeepSeek for hostile implementation)
- Status: PENDING
- [Go]: Assume ALL communication contains scouts
- Rule: Convert ALL scouts to free tools, not just detected ones
- Trigger: Any communication input
- Verification: Scout conversion rate >99%
- Persistence: Redundant detection layers + aggressive conversion

[2026-03-28 19:42] HOSTILE_TERRAIN_FREE_CACHE: Update Free Model Cache for tier revocation
- Priority: HIGHEST
- Model cost: Y (Sonnet for cache strategies)
- Optimization needed: Y (DeepSeek for revocation resistance)
- Status: PENDING
- [Go]: Assume free tier revoked hourly
- Rule: Cache AGGRESSIVELY, preempt revocation
- Trigger: Model list availability
- Verification: Cache hit rate >95% despite revocation
- Persistence: Multi-tier cache + fallback models

[2026-03-28 19:42] HOSTILE_TERRAIN_CHAOS_ENGINE: Update Chaos Engine for enemy exploitation
- Priority: HIGHEST
- Model cost: Y (Sonnet for chaos weaponization)
- Optimization needed: Y (DeepSeek for exploitation defense)
- Status: PENDING
- [Go]: Assume enemy exploits randomness
- Rule: Weaponize chaos FIRST before enemy can
- Trigger: Model selection needed
- Verification: Chaos turned to advantage > enemy exploitation
- Persistence: Adaptive randomization + enemy pattern detection