# Agency Skill Integration Guide

## Optimized Skills
1. **clawdocs** - Interactive documentation with structured embeds
2. **telegram-ui** - Enhanced Telegram UI with batch processing

## Integration Points
- Fiesta-agents orchestrator can dispatch to these skills
- Skills accept batch API calls for internal couplings
- Interactive components work with Telegram inline keyboards
- Structured embeds use Telegram's formatting options

## Usage Examples

```bash
# Via orchestrator
./orchestrator.sh --skill clawdocs --task "generate-api-docs"

# Direct API call
curl -X POST http://localhost:9001/api/telegram-ui/execute \
  -H "Content-Type: application/json" \
  -d '{"message": "Test", "buttons": ["Option1", "Option2"]}'
```

## Next Steps
1. Test interactive components with Telegram bot
2. Add batch API methods for internal agency couplings
3. Integrate with autoresearch for skill optimization
4. Add structured embeds to all agency communications
