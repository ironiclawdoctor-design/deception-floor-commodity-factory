# ProjectX Gateway API — Surface Map
**Discovered:** 2026-03-29 via Lucid Trading chatbot → IS-007 white-label reveal
**Base URL:** https://api.topstepx.com
**Swagger:** https://api.topstepx.com/swagger/v1/swagger.json
**Status:** Healthy (confirmed)
**Auth:** API key via POST /api/Auth/loginKey — key obtained from Settings > API inside platform
**Cost:** $29/month ProjectX add-on (key generation only — docs are FREE)

## Confirmed Endpoints
- POST /api/Auth/loginApp — app credentials auth
- POST /api/Auth/loginKey — API key auth ← agency path
- POST /api/Auth/logout
- POST /api/Auth/validate
- POST /api/Account/search — account data
- POST /api/Contract/search — instrument lookup (MNQ, MES etc.)

## Agency Build Plan (zero cost until funded)
1. Build auth wrapper: POST /api/Auth/loginKey with API key → get session token
2. Build account poller: POST /api/Account/search → pull balance, DLL status
3. Build trade logger: POST /api/Contract/search → map instrument → log to lucid_sessions
4. DLL monitor: poll balance every 5min during session → alert if within $300 of limit
5. Consistency tracker: running ratio of largest_day_pnl / total_cycle_pnl → alert if >15%

## Phase 0 Integration (on fund)
- Day 1: Subscribe to $29/month API add-on
- Day 1: Extract API key from Settings > API
- Day 1: Run auth → confirm session token
- Day 1: All trades auto-log to dollar.db lucid_sessions table
- Agency monitors DLL + consistency ratio in real time

*The chatbot said docs are locked. The Swagger is public. The investigation is ongoing.*
