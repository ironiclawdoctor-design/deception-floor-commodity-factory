# 🤠 TEXAN.md — Nadir Strip Mining Registry

> *Go to the bottom. Extract everything. Build upward from bedrock.*

## Philosophy

Texan engineering: practical, no-nonsense, self-reliant. If it works, ship it. If it's free, mine it. If it's reputable, trust it. If it breaks, fix it. Don't buy what you can build. Don't build what already exists for free.

**Nadir strip mining** = for every capability, find the lowest-cost reputable tool that does the job. Then go one level deeper.

## Mining Criteria

Every tool in this registry must pass ALL checks:

```
0. FREE — MIT/Apache/BSD licensed, no usage fees, no token costs
1. REPUTABLE — maintained, starred, used in production by others
2. RUNS ON OUR HARDWARE — AMD EPYC 4-core, 7.2GB RAM, no GPU, Linux x86_64
3. SELF-CONTAINED — minimal dependencies, doesn't phone home
4. PRIVACY-SAFE — no telemetry, no data exfiltration, auditable source
5. PATH B COMPLIANT — solves a real problem, not speculative
```

---

## Tier 0: Already Mined (installed and working) ⛏️

These are the bedrock — tools we already have and use daily.

| Tool | Purpose | Cost | Source | Notes |
|---|---|---|---|---|
| **BitNet/bitnet.cpp** | Local LLM inference (1.58-bit) | $0 | microsoft/BitNet | 29 tok/s, {-1,0,1} weights |
| **Python 3.12** | Scripting, ML, data processing | $0 | system | Already installed |
| **Node.js 22** | JavaScript runtime, npm ecosystem | $0 | system | Already installed |
| **gcc/g++ 13.3** | C/C++ compilation | $0 | system | Already installed |
| **clang 18** | C/C++ compilation (BitNet requires) | $0 | system | Already installed |
| **cmake 3.28** | Build system | $0 | system | Already installed |
| **git 2.43** | Version control, free checkpoints | $0 | system | SSH authenticated |
| **curl** | HTTP client | $0 | system | API calls, downloads |
| **bash/grep/sed/awk** | Text processing | $0 | system | Zero-token operations |
| **PyTorch 2.2 (CPU)** | ML framework | $0 | pip | CPU-only build |
| **Transformers 4.57** | HuggingFace model loading | $0 | pip | Training pipeline |
| **OpenClaw** | Agent platform | $0 | npm | Our runtime |

## Tier 1: Ready to Mine (identified, not installed) 🔍

High-value tools worth strip-mining next.

| Tool | Purpose | Stars | License | Size | Why Mine It |
|---|---|---|---|---|---|
| **Ollama** | Local model serving (OpenAI-compatible API) | 135K+ | MIT | ~100MB | Wraps BitNet/GGUF models in OpenAI-compatible REST API. Agents can call local model as if it were OpenAI. |
| **SQLite** | Embedded database | N/A (stdlib) | Public Domain | ~1MB | Zero-cost persistent storage. Training data, metrics, logs. No server needed. |
| **jq** | JSON processing | 30K+ | MIT | ~1MB | Replaces AI for JSON manipulation. Tier 0 tool. |
| **DuckDB** | Analytical SQL on files | 28K+ | MIT | ~30MB | Query CSV/Parquet/JSON without a database server. Analytics on training data. |
| **ripgrep (rg)** | Fast search | 50K+ | MIT | ~5MB | 10-100x faster than grep. Nadir for code/text search. |
| **fd** | Fast file finder | 35K+ | MIT | ~3MB | Replaces `find` with sanity. |
| **bat** | Better `cat` with syntax highlighting | 50K+ | MIT | ~5MB | Developer quality of life. |
| **httpie/curlie** | Better HTTP client | 34K+ | BSD | ~10MB | API testing without AI overhead. |
| **Uptime Kuma** | Self-hosted monitoring | 65K+ | MIT | Node.js | Monitor our services. Status dashboard. |
| **Memos** | Self-hosted notes | 37K+ | MIT | Go binary | Alternative to memory files — searchable, linkable. |

## Tier 2: Deep Nadir (the really cheap stuff) ⛏️⛏️

Single-file tools, scripts, and utilities that cost almost nothing.

| Tool | Purpose | Why |
|---|---|---|
| **shellcheck** | Bash script linter | Our scripts need to be correct. Free. One binary. |
| **entr** | Run command on file change | Watch files, auto-rebuild. 200 lines of C. |
| **fzf** | Fuzzy finder | Navigate files/history/anything. Single binary. |
| **tmux** | Terminal multiplexer | Run multiple processes. Essential for training + serving. |
| **htop** | Process monitor | See what's eating our RAM during training. |
| **ncdu** | Disk usage analyzer | Find what's consuming our 136GB. |
| **age** | File encryption | Encrypt model weights at rest. Single binary. Go. |
| **restic** | Backup tool | Encrypted backups of our workspace. Deduplication. |
| **caddy** | Web server | Serve GitHub Pages locally. Auto-HTTPS. Single binary. |
| **datasette** | Explore SQLite in browser | View training data, metrics, logs via web UI. |

## Tier 3: Repo Mining Targets (explore for extraction) 🗺️

Repos to explore for extractable components:

| Repo | What to Extract | Direction |
|---|---|---|
| **awesome-selfhosted** | Master list of free self-hosted tools | Map the nadir landscape |
| **awesome-local-llm** | Local LLM tools, techniques, models | Train vertex reinforcement |
| **microsoft/BitNet** | Training code (not just inference) | Sovereignty: train our own 1-bit models |
| **ggml-org/llama.cpp** | GGUF ecosystem, server mode, embeddings | Inference infrastructure |
| **huggingface/trl** | Training reinforcement learning | Fine-tuning improvement |
| **huggingface/peft** | Parameter-efficient fine-tuning | LoRA/QLoRA for our hardware |
| **Mozilla/llamafile** | Single-file executable LLM | Ultimate nadir: entire model in one file |
| **n8n-io/n8n** | Workflow automation | Automate training pipeline without tokens |
| **go-gitea/gitea** | Self-hosted GitHub alternative | If we ever need to leave GitHub |
| **minio/minio** | Self-hosted S3-compatible storage | Model artifact storage |

## Tier 4: The Texan Skills Pipeline

Every tool mined goes through:

```
0. DISCOVER — Find tool in repo ecosystem
1. EVALUATE — Does it pass all 6 mining criteria?
2. TEST — Install and verify on our hardware
3. INTEGRATE — Connect to existing workflows
4. DOCUMENT — Add to this registry with notes
5. TRAIN — Teach agents how to use it (may cost tokens → Triangle flows)
6. AUTOMATE — Script the integration so it never needs tokens again
```

This pipeline is itself a Texan operation: practical, repeatable, no waste.

---

## The Strip Mining Doctrine

```
Every tool we mine is a permanent capability gain:
  - It doesn't consume tokens (unlike external API calls)
  - It doesn't need training (unlike local LLM improvement)
  - It just WORKS, forever, for free
  - It's the bedrock that Token and Train build on

The nadir is not the bottom — it's the FOUNDATION.
Strip mining is not destruction — it's DISCOVERY.
Going deep is not going down — it's going SOLID.

Texas built an economy on what was underground.
We build an agency on what's in the repos.
```

---

## Mining Schedule

- **Daily:** Check for new versions of Tier 0 tools (security patches)
- **Weekly:** Evaluate one Tier 1 tool for installation
- **Monthly:** Explore one Tier 3 repo for extractable components
- **Quarterly:** Review entire registry — promote, demote, or retire tools

All mining operations are **Tier 0 cost** (bash, git, curl). The Texan vertex costs zero tokens by design.

---

**Filed by:** Fiesta — Chief of Staff
**Vertex:** 🤠 Texan (Prosperity Triangle, position 2)
**Doctrine:** Go to the bottom. Extract everything. Build upward from bedrock.
**Cost of this document:** Zero tokens (it's in the files now, forever)
