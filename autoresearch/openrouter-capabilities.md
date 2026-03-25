# OpenRouter Capabilities — Autoresearch
*Generated 2026-03-25*

## LLM API Features
*(What we already use — model routing, free tier, etc.)*

### Core API
- **Unified OpenAI-compatible API** at `https://openrouter.ai/api/v1/chat/completions`
- Supports OpenAI SDK, Anthropic SDK, direct fetch — drop-in compatible
- `Authorization: Bearer <key>` header auth

### Model Routing
- **Default load balancing**: price-weighted inverse-square selection across stable providers
- **Provider object**: fine-grained routing control per request
  - `order`: explicit provider priority list (e.g. `["anthropic", "openai"]`)
  - `allow_fallbacks`: true/false (default: true)
  - `require_parameters`: only use providers supporting all params
  - `data_collection`: "allow" | "deny"
  - `only` / `ignore`: allowlist or denylist specific providers
  - `quantizations`: filter by model quantization level (int4, int8, etc.)
  - `sort`: "price" | "throughput" | "latency"
  - `preferred_min_throughput`, `preferred_max_latency`: SLA hints (soft)
  - `max_price`: hard cap — request fails if no provider is within budget

### Model Variants (Suffixes)
| Variant | Effect |
|---------|--------|
| `:free` | Access free model tier (lower rate limits) |
| `:nitro` | Sort providers by throughput (fastest) |
| `:floor` | Sort providers by lowest price |
| `:online` | Add real-time web search to any model |
| `:extended` | Extended context window |
| `:thinking` | Extended reasoning (chain-of-thought) |
| `:exacto` | Quality-first for tool-calling reliability |

### Multi-Model Fallbacks
- `models` array: ordered priority list; if model 1 errors → auto-try model 2, etc.
- Triggers: outages, rate limiting, content moderation refusals, context length errors
- Billed at the model actually used

### Auto Router
- `openrouter/auto`: NotDiamond-powered — selects best model for your prompt automatically
- Free Models Router: dedicated router for zero-cost inference

### Tool / Function Calling
- OpenAI-format `tools` and `tool_calls` standardized across all providers
- `:exacto` variant optimizes provider selection for tool-calling quality
- Auto Exacto: automatically optimizes provider ordering for tool calls
- Filter tool-capable models at `openrouter.ai/models?supported_parameters=tools`

### Streaming
- SSE streaming supported (`stream: true`)
- Usage data included per-chunk when streaming

### Structured Outputs
- `response_format.type: "json_schema"` with `strict: true`
- Supported on: OpenAI GPT-4o+, Google Gemini, Anthropic (Sonnet 4.5+, Opus 4.1+), most open-source, Fireworks
- `require_parameters: true` ensures routing only to compliant providers

### Multimodal
- **Image inputs**: vision models via standard message format
- **Image generation**: image output models
- **PDF inputs**: send PDFs to any model
- **Audio**: TTS and speech-to-text capable models
- **Video inputs**: video-capable models

### Web Search Plugin
- Append `:online` to any model or use `plugins: [{id: "web"}]`
- **Engines**: native (Anthropic/OpenAI/Perplexity/xAI), Exa, Firecrawl, Parallel
- `max_results`, `search_prompt`, `include_domains`, `exclude_domains` customizable
- xAI models get both web search + X/Twitter search
- **Costs extra even on free models**

### Response Healing Plugin
- Auto-validates and repairs malformed JSON responses
- Ensures schema compliance even with imperfect model outputs

### Prompt Caching
- **Automatic caching**: OpenAI, DeepSeek, Gemini, Grok, Groq, Moonshot AI
- **Explicit caching**: Anthropic via `cache_control` breakpoints (up to 4)
- Cache TTLs: 5 min (default) or 1 hour for Anthropic
- **Provider sticky routing**: after cache hit, subsequent requests routed to same provider to maximize cache reuse
- Sticky routing tracked per-account, per-model, per-conversation (by hashing first messages)
- OpenAI cache reads: 0.25–0.50x base price; cache writes: free
- Anthropic cache writes: 1.25x base (5min) or 2x (1hr); cache reads: 0.1x base

### Reasoning Tokens
- Supported for thinking-capable models; usage tracked in response
- Deducted from credits

---

## Infrastructure Features (NEW)
*(Anything beyond simple LLM calls)*

### Programmatic API Key Management
- **Management API Keys**: dedicated admin keys for CRUD operations on child keys
- Endpoints under `/api/v1/keys`
- Create keys with: credit limits, limit-reset periods (daily/weekly/monthly), disable flags
- Per-key usage tracking: daily, weekly, monthly (both OpenRouter credits and BYOK usage)
- **Agency pattern**: generate unique keys per customer/agent — full SaaS key distribution

### Organization Management
- Organizations with shared credit pool (max 10 members currently)
- Role-based access: Admin (full) vs Member (limited)
- Per-member and per-key **Guardrails** (spending caps, model/provider allowlists, ZDR)
- Centralized billing, usage analytics, activity feed
- EU in-region routing available for enterprise customers

### Guardrails System
- Spending caps (daily/weekly/monthly) per key or per member
- Model allowlists and provider allowlists
- Zero Data Retention (ZDR) enforcement
- Guardrail hierarchy: intersection logic for providers/models; OR logic for ZDR
- Per-key AND per-member budgets enforced independently (stricter wins)
- Guardrails API for programmatic management

### BYOK (Bring Your Own Keys)
- Attach your own Anthropic/OpenAI/Google/AWS Bedrock/Azure keys to your account
- BYOK endpoints prioritized over shared capacity automatically
- Fallback to shared capacity on key exhaustion (configurable)
- First N BYOK requests/month: free; beyond that: small % fee of standard pricing
- Multiple keys per provider supported (routing order not guaranteed)
- Azure: JSON config per model deployment; AWS Bedrock: API key or IAM credentials

### Observability — Broadcast
- Auto-forward all request traces to external platforms (zero app code changes)
- Supported destinations:
  - Langfuse, LangSmith, Braintrust, Datadog, Grafana Cloud, New Relic
  - Arize AI, Comet Opik, ClickHouse, Snowflake, S3/S3-compatible
  - PostHog, Sentry, OpenTelemetry Collector, W&B Weave, Webhook (any HTTP endpoint)
- Trace data includes: request/response, token counts, cost, latency, model, tool usage
- Optional: `user` field (user ID) and `session_id` for grouping agent workflows

### Activity Export
- Export usage as CSV or PDF, grouped by API key, model, or org member
- Usage accounting endpoint: `/api/v1/generation` for per-request cost/token details

### Zero Data Retention (ZDR)
- Restrict routing to ZDR-compatible provider endpoints only
- Admin-controlled at org level or per guardrail

### Crypto Payment API
- Purchase credits via cryptocurrency (Coinbase integration)
- Supported chains available via Coinbase Commerce

### Claude Code Integration
- OpenRouter as drop-in Anthropic API replacement for Claude Code
- Set `ANTHROPIC_BASE_URL=https://openrouter.ai/api` — no proxy needed
- Enables: multi-provider failover, org budget controls, usage visibility
- **Sub-agent model routing**: `CLAUDE_CODE_SUBAGENT_MODEL` env var routes Claude Code sub-agents through specific models

### Anthropic Agent SDK Support
- The Anthropic Agent SDK (Python/TypeScript) works via same env vars as Claude Code
- Full agent framework routing through OpenRouter

### Automatic Code Review Agent (Stop Hook pattern)
- OpenRouter supports background reviewer agents triggered by Claude Code stop hooks
- Pattern: `claude → stop hook → background reviewer via OpenRouter API`

---

## Free Tier Limits

**No direct RPM/TPM numbers published in docs** — the rate limit page URL (`/docs/rate-limits`) returned 404. From FAQ:

### Free Model Rate Limits (`:free` variant)
- **With credits purchased**: higher daily limit (exact number rendered client-side as `FREE_MODEL_HAS_CREDITS_RPD`)
- **Without credits**: lower daily limit (exact number rendered client-side as `FREE_MODEL_NO_CREDITS_RPD`)
- Rate limits are "determined by the credits you have purchased"
- Having *any* credits unlocks the higher free tier RPD

### Practical Notes
- Free model limits are **per-day** (RPD), not per-minute
- Paid requests are rate-limited by provider capacity (no hard OR-level cap disclosed)
- Using BYOK bypasses OpenRouter's shared rate limits entirely (your own provider limits apply)
- `:free:online` works (web search on free models) but web search incurs extra cost regardless

**To get exact RPD numbers**: check `https://openrouter.ai/docs/api-reference/limits` or the FAQ page (values are JavaScript-rendered template variables).

---

## Agent Spawning Capabilities

**OpenRouter cannot spawn or host agents.** It is purely an LLM inference routing layer.

However, it provides key building blocks for agent infrastructure:

| Capability | Status |
|-----------|--------|
| Host/run agent workers | ❌ Not available |
| Provision compute/VMs | ❌ Not available |
| Persistent agent state | ❌ Not available |
| Spawn sub-agents | ❌ Not directly |
| Route LLM calls for agents | ✅ Core feature |
| Per-agent API keys (via Management API) | ✅ Yes |
| Per-agent spending limits (Guardrails) | ✅ Yes |
| Sub-agent model routing (Claude Code) | ✅ Via env vars |
| Agent observability (Broadcast) | ✅ Via session_id |
| Tool calling support | ✅ Yes |
| Failover between models for agents | ✅ Model fallbacks |
| Structured output for agent responses | ✅ JSON schema |

**Pattern for agent orchestration via OpenRouter:**
- Each spawned agent gets a management-API-created key with a credit limit
- `session_id` field groups all agent sub-calls into one observable trace
- `user` field tags which agent is making calls
- Guardrails restrict agent to approved models only
- Model fallbacks ensure agents don't hard-fail on provider outages

---

## Provider Network

### Major Providers (partial list from routing docs)
- **Anthropic** (1P, Amazon Bedrock, Google Vertex AI)
- **OpenAI** (1P, Azure)
- **Google** (Gemini, Vertex AI)
- **Meta** (Llama via multiple hosts)
- **Mistral AI**
- **xAI** (Grok)
- **Perplexity**
- **Groq**
- **Fireworks AI**
- **Together AI**
- **DeepSeek**
- **Moonshot AI**
- **AWS Bedrock** (via BYOK or shared)
- **Azure AI Services** (via BYOK)

### Bare Metal / Custom Providers
- OpenRouter allows inference providers to list themselves via their provider program
- No dedicated bare metal offering from OpenRouter itself
- "For providers" page describes listing requirements
- EU in-region routing for enterprise (prompts stay in EU)

### Provider Quantization Filtering
- Filter by quantization level: `int4`, `int8`, `fp8`, `fp16`, `bf16`, etc.
- Useful for cost/quality tradeoffs on open-source models

---

## Pricing Model

### Credits System
- Pre-purchase credits in USD (deposit model)
- Credits deducted per request at provider's listed price
- **No markup on inference** — pass-through pricing
- Fee only charged on credit purchase (% of deposit amount via Stripe or crypto)

### Credit Purchase
- Stripe: standard fee applies (% shown at checkout, varies)
- Crypto (Coinbase): separate fee rate
- Crypto payment supported chains via Coinbase Commerce

### Per-Token Pricing
- Prompt tokens and completion tokens priced separately
- Reasoning tokens billed separately for thinking models
- Image generation: per-image pricing
- Request-based pricing for some models

### Caching Discounts
- OpenAI cache reads: 0.25–0.50x input price (auto, no write cost)
- Anthropic cache reads: ~0.1x input price; write cost 1.25–2x (offset by read savings)
- `cache_discount` field in response shows net savings per request

### Web Search Plugin Cost
- Extra cost on top of inference, even with free models
- Engine choice (native vs Exa vs Firecrawl) affects cost

### BYOK Fee Structure
- First N BYOK requests/month: free
- Beyond that: small % fee (displayed as template var in docs, ~1% or less)

### Zero Completion Insurance
- No charge for failed or empty completions
- Credits refunded for non-delivering responses

---

## Agency-Relevant Opportunities

### 🔑 Management API Keys — Agent Key Distribution
**Currently unused, high value.** Create per-agent or per-client sub-keys programmatically:
- Set per-key credit limits (prevents runaway spend)
- Daily/weekly/monthly limit resets
- Revoke keys programmatically when agent tasks complete
- Track each agent's exact spend independently

### 📊 Guardrails — Agent Budget Control
**Currently unused.** Lock down which models agents can use and how much they can spend per day.

### 📡 Broadcast / Observability Integration
**Currently unused.** Pipe all OpenRouter traces to Langfuse, Datadog, S3, etc.:
- `session_id` per agent run = full agentic trace in one place
- `user` field = per-agent attribution
- Zero code changes needed — configure in dashboard

### 🔀 Model Fallbacks for Agent Resilience
**Likely underused.** Provide fallback model chains for critical agent tasks:
```json
{"models": ["anthropic/claude-sonnet-4.6", "openai/gpt-4o", "google/gemini-2.0-flash"]}
```
Eliminates hard failures from provider outages.

### 🌐 Web Search `:online` for Research Agents
Grounded web search on any model for free with just `:online` suffix. Domain filtering available.

### 📦 Prompt Caching for High-Volume Agents
For agents with large system prompts (RAG data, character cards, instructions):
- Anthropic `cache_control` on system prompt = 90% cost reduction after first hit
- Sticky routing ensures cache hits across multi-turn agent conversations

### 💰 BYOK for Rate Limit Management
When agents hit OpenRouter shared rate limits, BYOK lets the agency use its own provider keys to bypass them — critical for high-throughput parallel agents.

### 🤖 Claude Code + OpenRouter
Route Claude Code (and Anthropic Agent SDK) through OpenRouter for:
- Failover between Anthropic providers
- Sub-agent model routing via env vars
- Cost visibility per coding session

### 🏗️ Organization Structure for Client Isolation
Create org + guardrails to isolate per-client agent spend and model access.

---

## What OpenRouter Cannot Do

| Limitation | Notes |
|-----------|-------|
| **Host agents or workers** | No execution environment; LLM routing only |
| **Provision compute / VMs** | Not a cloud provider; use Ampere, GCP, etc. |
| **Persistent agent memory** | No state storage; implement externally |
| **Spawn agents on trigger** | No cron / webhook → agent runner |
| **Execute code** | No code interpreter; models can suggest, not execute |
| **Persistent websocket connections** | SSE streaming per-request only; no long-lived connections |
| **More than 10 org members** | Current org limit (contact support for more) |
| **Guarantee throughput SLAs** | `preferred_min_throughput` is a hint, not a guarantee |
| **EU in-region without enterprise plan** | EU data residency is enterprise-only |
| **Bare metal / GPU provisioning** | Not in scope; that's the provider's infrastructure |
| **Async/batch inference** | No async job queue; all requests are synchronous or streaming |
| **Fine-tuning** | Routes to providers that support it, but no fine-tuning UI/API of its own |
| **Custom model hosting** | Cannot host custom/proprietary models; must use listed providers |

---

## Sources
- https://openrouter.ai/docs (index)
- https://openrouter.ai/docs/guides/routing/provider-selection
- https://openrouter.ai/docs/guides/features/tool-calling
- https://openrouter.ai/docs/guides/best-practices/prompt-caching
- https://openrouter.ai/docs/guides/features/plugins/web-search
- https://openrouter.ai/docs/guides/routing/model-variants/free
- https://openrouter.ai/docs/guides/administration/organization-management
- https://openrouter.ai/docs/guides/overview/auth/management-api-keys
- https://openrouter.ai/docs/guides/features/guardrails
- https://openrouter.ai/docs/guides/coding-agents/claude-code-integration
- https://openrouter.ai/docs/faq
- https://openrouter.ai/docs/guides/overview/auth/byok
- https://openrouter.ai/docs/guides/features/structured-outputs
- https://openrouter.ai/docs/guides/routing/model-fallbacks
- https://openrouter.ai/docs/guides/features/broadcast/overview
