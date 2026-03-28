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