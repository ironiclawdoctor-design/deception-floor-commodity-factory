# Telegram↔Bash Bridge (Functional)

## Components

### handler.py
- Validates commands (whitelist mode, forbids special chars)
- Executes bash with 5s timeout
- Rate-limits: 10 req/min per user
- Returns: `{"status": "ok|error", "result": {"exit_code": N, "stdout": "...", "stderr": "..."}}`

### bot.py
- Python-telegram-bot wrapper
- Polls for messages, invokes handler, replies with output
- Requires: `TELEGRAM_BOT_TOKEN` env var

### security-model.sh
- Bash firewall: rejects pipes, redirects, special chars
- Rate-limit enforcement via JSON file
- Timeout: 5s per command
- Assume breach model: bash is the only firewall

### context-serializer.sh
- Outputs compacted format: `timestamp|user_id|command|exit_code|base64(stdout)`
- Stderr logged separately
- No explanatory text, bash-only format

### telegram-cli.sh
- CLI wrapper: `./telegram-cli.sh <user_id> <command>`
- Combines handler + serializer
- Returns compacted context or error JSON

## Usage

### Test Suite
```bash
bash test.sh
```
Runs 10 integration tests. All passing.

### Direct CLI
```bash
./telegram-cli.sh user123 "pwd"
./telegram-cli.sh user456 "ls -la /tmp"
```

### Bot (requires token)
```bash
export TELEGRAM_BOT_TOKEN="your_token"
python3 bot.py
```

### Python API
```python
from handler import handle_telegram_message
result = handle_telegram_message("user123", "echo hello")
```

## Security

- **Whitelist mode:** Only alphanumeric, spaces, dash, underscore, dot, slash
- **Timeout:** 5 seconds (exit code 124)
- **Rate limit:** 10 commands/min per user (persistent, restarts ignored)
- **Breach model:** Assume telegram token leaked. Bash is firewall. No shell metacharacters allowed.

## Test Results

```
=== HANDLER TESTS ===
Test 1 (valid command): ✓ PASS
Test 2 (rate limit): ✓ PASS (10 ok, 2 blocked)
Test 3 (forbidden chars): ✓ PASS
Test 4 (exit code): ✓ PASS
Test 5 (timeout): ✓ PASS

=== SECURITY MODEL TESTS ===
Test 6 (valid cmd): ✓ PASS
Test 7 (reject semicolon): ✓ PASS
Test 8 (bash execution): ✓ PASS

=== CONTEXT SERIALIZER TESTS ===
Test 9 (serializer format): ✓ PASS

=== INTEGRATION TEST ===
Test 10 (handler + serializer): ✓ PASS
```

## Cost

- Tier 0-2 only: All code is bash/python local execution
- Zero API calls (except Telegram polling)
- Build cost: <$0.50 (tokens for handler.py only, no external reasoning)
- Runtime: Python interpreter + bash, no external services

## Files

- `handler.py` - Core command handler (2.5KB)
- `bot.py` - Telegram bot wrapper (1.8KB)
- `security-model.sh` - Bash firewall (1.8KB)
- `context-serializer.sh` - Compacted output format (0.7KB)
- `telegram-cli.sh` - CLI wrapper (0.7KB)
- `test.sh` - Integration tests (2.6KB)
- `README.md` - This file

Total: ~11KB working code.
