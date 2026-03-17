# Agency Protocol Filters

**Script:** `agency-protocol-filters.sh`  
**Cost:** $0.00 (Tier 0 bash only)  
**Status:** Ready to use

## Overview

This script provides 7 callable functions that create `tcpdump` filters for all agency protocols. Instead of reading documentation, tcpdump learns by observing actual packets on the network.

## The 7 Protocols

| # | Protocol | Port(s) | Source | Function |
|---|----------|---------|--------|----------|
| 1 | HTTP/HTTPS | 80, 443 | External APIs, web services | `capture_http()` |
| 2 | SSH | 22 | Git, repos, remote execution | `capture_ssh()` |
| 3 | DNS | 53 | Domain resolution, service discovery | `capture_dns()` |
| 4 | TCP/UDP | varies | Internal services, control plane | `capture_tcp_udp_internal()` |
| 5 | SQLite | N/A (file I/O) | Local database, state persistence | `capture_sqlite()` |
| 6 | JSON-RPC | 5000+ | BitNet inference, local reasoning | `capture_bitnet()` |
| 7 | Cron | N/A (syslog) | Scheduled tasks, async operations | `capture_cron_metadata()` |

## Quick Start

```bash
# Source the script
source /root/.openclaw/workspace/agency-protocol-filters.sh

# Show HTTP/HTTPS capture command (informational)
capture_http

# Capture DNS to file
capture_dns any /tmp/agency-pcaps

# Monitor all protocols
capture_all_protocols /tmp/agency-pcaps

# Check SQLite activity
capture_sqlite /root/.openclaw/workspace

# View cron execution patterns
capture_cron_metadata
```

## Recursive Learning Mechanism

Each function is designed to **learn from actual traffic**, not from documentation:

- **HTTP:** Pipelined requests, chunked encoding, redirects, response codes
- **SSH:** Handshake, authentication methods, channel multiplex, command frames
- **DNS:** Recursive queries, zone transfers, EDNS extensions, caching
- **TCP/UDP:** Service discovery, internal APIs, heartbeats, control messages
- **SQLite:** File locks, transaction patterns, WAL mode behavior
- **JSON-RPC:** Streaming responses, rate limits, token accounting, error handling
- **Cron:** Task triggers, environment variables, exit codes, scheduling patterns

## Protocol Details

### 1. capture_http()
```bash
capture_http [interface] [output_dir]

# Example:
capture_http any /tmp/agency-pcaps
```
- Watches ports 80 (HTTP) and 443 (HTTPS)
- Learns: request/response patterns, pipelined requests, TLS handshakes
- Use case: Monitor API calls, external integrations

### 2. capture_ssh()
```bash
capture_ssh [interface] [output_dir]

# Example:
capture_ssh any /tmp/agency-pcaps
```
- Watches port 22 (SSH)
- Learns: authentication methods, banner exchange, key exchange, channels
- Use case: Git operations, remote command execution

### 3. capture_dns()
```bash
capture_dns [interface] [output_dir]

# Example:
capture_dns any /tmp/agency-pcaps
```
- Watches port 53 (UDP and TCP)
- Learns: query types (A, AAAA, MX, CNAME), response TTL, DNSSEC
- Use case: Service discovery, domain resolution patterns

### 4. capture_tcp_udp_internal()
```bash
capture_tcp_udp_internal [interface] [dir] [subnet]

# Example:
capture_tcp_udp_internal any /tmp/agency-pcaps 192.168.0.0/16
```
- Watches all TCP/UDP except HTTP/HTTPS/SSH/DNS
- Learns: service discovery, heartbeats, internal control plane
- Use case: Monitor internal APIs, agent communication

### 5. capture_sqlite()
```bash
capture_sqlite [db_path] [process_pattern]

# Example:
capture_sqlite /root/.openclaw/workspace
```
- Uses `lsof` and `strace` instead of tcpdump (local file I/O)
- Learns: file locks, transaction patterns, WAL mode behavior
- Use case: Monitor database I/O, detect lock contention

### 6. capture_bitnet()
```bash
capture_bitnet [interface] [dir] [port]

# Example:
capture_bitnet any /tmp/agency-pcaps 5000
```
- Watches local JSON-RPC port (default 5000)
- Learns: RPC method calls, params, responses, streaming, token usage
- Use case: Monitor local inference, debug BitNet communication

### 7. capture_cron_metadata()
```bash
capture_cron_metadata [log_file] [minutes]

# Example:
capture_cron_metadata /var/log/syslog 60
```
- Uses syslog, process monitoring (no network packets)
- Learns: task triggers, environment, exit codes, scheduling patterns
- Use case: Monitor scheduled operations, debug cron failures

## Helper Function

### capture_all_protocols()
Runs all 7 captures informational output (doesn't block):

```bash
capture_all_protocols /tmp/agency-pcaps
```

## Integration with Agency Architecture

This script supports:

- **Tier 0 bash discipline:** No external calls, pure system utilities
- **Recursive learning:** tcpdump patterns emerge from real traffic
- **Cost tracking:** $0.00 (bash only, no tokens)
- **Operational transparency:** All protocols visible at packet level

## Typical Usage Workflow

1. **During normal operations:** Run `capture_all_protocols /tmp/agency-pcaps` once per day
2. **Debugging issues:** Use specific protocol capture (e.g., `capture_ssh`, `capture_dns`)
3. **Performance analysis:** Compare SQLite patterns with cron timing
4. **Security monitoring:** Watch for unexpected ports, unusual patterns

## Files Generated

- `http-capture.pcap` — HTTP/HTTPS traffic
- `ssh-capture.pcap` — SSH traffic
- `dns-capture.pcap` — DNS queries/responses
- `tcp-udp-internal-capture.pcap` — Internal TCP/UDP
- `bitnet-capture.pcap` — JSON-RPC traffic

(SQLite and cron use text output, not PCAP files)

## Advanced Usage

### Continuous Monitoring
```bash
# Monitor HTTP in real-time (Ctrl+C to stop)
capture_http any | grep -i "GET\|POST"
```

### Filter by Host
```bash
# Modify the capture function or run tcpdump directly:
tcpdump -i any 'tcp port 443 and dst host api.example.com' -A
```

### Correlate Multiple Protocols
```bash
# Run all captures to /tmp, then analyze:
capture_all_protocols /tmp/agency-pcaps
ls -lh /tmp/agency-pcaps/*.pcap
wireshark /tmp/agency-pcaps/http-capture.pcap  # if wireshark available
```

## Cost Analysis

| Component | Cost | Notes |
|-----------|------|-------|
| tcpdump | $0.00 | System utility, no tokens |
| lsof | $0.00 | System utility, no tokens |
| strace | $0.00 | System utility, no tokens |
| syslog | $0.00 | System logs, no tokens |
| **Total** | **$0.00** | Pure Tier 0 bash |

## Notes

- tcpdump may require `sudo` privileges for network capture
- SQLite and cron functions don't use network, so tcpdump is irrelevant for those
- All functions are exported as shell functions for easy reuse
- Script is idempotent and non-destructive
- Packet captures (PCAP files) can grow large; rotate periodically

---

**Created:** 2026-03-15  
**Status:** Ready for testing in terminal  
**Maintainer:** Agency Operations (Fiesta)
