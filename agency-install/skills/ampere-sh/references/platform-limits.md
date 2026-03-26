# Ampere.sh Platform Limits

Documented hard limits for agent operations on Ampere.sh.

## Compute

| Resource | Hard Limit | Notes |
|----------|-----------|-------|
| Terminal instances | 3 concurrent max | Exceeding kills oldest or blocks new |
| CPU | Shared (container-level) | No dedicated cores; burst allowed |
| GPU | None | Not a GPU platform; no CUDA/ROCm |
| RAM | Container-allocated | Check with `free -h`; varies by plan |
| Disk | Workspace-scoped | `/root/.openclaw/workspace` is persistent |

## Network

| Resource | Limit | Notes |
|----------|-------|-------|
| Outbound HTTP/HTTPS | Allowed | Web fetch, API calls, git operations |
| Inbound connections | Blocked (reverse proxy only) | No direct port exposure to internet |
| Localhost services | Allowed | Ports 9000, 9001, 9222, etc. on 127.0.0.1 |
| SSH outbound | Allowed | Git push/pull to GitHub works |

## Security Boundaries

| Boundary | Enforcement |
|----------|-------------|
| Container isolation | Linux namespaces + UID mapping |
| Root access | Container-local only (not host root) |
| Cross-user access | Blocked at all layers |
| API key scope | Per-user, encrypted server-side |
| Spending limits | Server-side enforced, non-bypassable |

## Software

| Capability | Status | Notes |
|-----------|--------|-------|
| Local LLM hosting | **NOT SUPPORTED** | BitNet cancelled 2026-03-17; wrong platform type |
| Python/Node.js/Bash | Available | Standard toolchain present |
| Docker-in-Docker | Not available | Single container per user |
| systemd services | Limited | Some service management available |
| Cron | Available | Standard crontab |

## Operational Guidance

- **Terminal discipline:** Never exceed 3 sessions. Use `tmux` to multiplex if needed.
- **Storage:** Clean up temp files. `ncdu` for disk audit. Workspace persists across sessions.
- **Token burn:** Monitor daily. Credits deplete based on external model API calls, not bash/local ops.
- **Service restarts:** If a service on port 9000/9001/9222 dies, check PID and restart manually. No guaranteed auto-restart.
- **Git:** SSH-based git works. `gh` CLI auth may not be configured — SSH is the Path B workaround.
