# sonnet-queue.md - Model Optimization Pipeline

## Architecture
1. Stack: All expensive-model tasks accumulate here
2. Optimize: Sonnet analyzes queue, extracts optimal prompt patterns
3. Feed: DeepSeek receives optimized prompts
4. Execute: Cheaper model handles execution
5. Loop: Results inform next optimization cycle

## Queue Protocol
- Entry format: [YYYY-MM-DD HH:MM] 