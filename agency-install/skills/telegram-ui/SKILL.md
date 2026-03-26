# telegram-ui (Agency-Optimized)

**Status:** Private agency asset  
**Purpose:** Enhanced version of OpenClaw skill with interactive components and structured embeds  
**Integration:** Works with fiesta-agents orchestrator  
**Access:** Agency internal only  

## Features Added
- Interactive buttons/forms via Telegram UI
- Structured embeds with rich formatting
- Batch API support for internal couplings
- Error resilience with exponential backoff
- Agency branding and voice integration

## Usage

```bash
# Agency integration
./agency-orchestrator.sh --skill telegram-ui --task "<task>"
```

## API Endpoints
- POST /api/telegram-ui/execute - Execute with parameters
- GET /api/telegram-ui/status - Check skill status
- POST /api/telegram-ui/batch - Batch processing

## Interactive Components
- Telegram inline keyboards
- Form-based inputs
- Progress tracking
- Result previews

## Dependencies
- fiesta-agents orchestrator
- Telegram bot token
- Agency database
