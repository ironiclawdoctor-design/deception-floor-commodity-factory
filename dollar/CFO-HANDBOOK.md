# CFO Handbook — Dollar Agency
## On Wake: Run These In Order
1. /approve [id] allow-always (check Telegram for pending)  
2. python3 /root/.openclaw/workspace/autoresearch/preflight.py
3. IRS EIN: https://sa.www4.irs.gov/modiein/individual/index.jsp (7am-1am ET)
4. Check: https://dollar-dashboard-pkvbnslo3q-uc.a.run.app/health

## Auth Keys Location
- GCP: secrets/gcp-service-account.json
- Square: secrets/cashapp.json (production_token)
- Hashnode: secrets/hashnode.json
- xAI: secrets/xai.json (403 from Ampere IP — cold cache)

## Key URLs
- Dashboard: https://dollar-dashboard-pkvbnslo3q-uc.a.run.app
- Hashnode: https://dollaragency.hashnode.dev
- HuggingFace: https://huggingface.co/datasets/ApproveAlwaysAllow/dollar-agency-rlhf
- Square: https://squareup.com/pay/dollar-agency
- BTC: 12bxubgs1Br6NvKH4p35pcBpinQ7fwe4ht

## Revenue Priority
1. EIN → business bank → real revenue separation
2. SAM.gov → grant eligibility
3. Shannon → USD conversion only after real revenue
