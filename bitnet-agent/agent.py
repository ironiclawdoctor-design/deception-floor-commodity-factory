#!/usr/bin/env python3
"""
BitNet Agent — Persistent local LLM worker for the Deception Floor.

All internal task progress routes through here first.
Supports local businesses: delegates queries to BitNet b1.58 2B running on CPU.
Zero token cost. Full sovereignty.

Usage:
  python3 agent.py --query "your question"
  python3 agent.py --interactive  (REPL mode)
  python3 agent.py --server       (stdin/stdout daemon for OpenClaw)
"""

import argparse
import json
import sys
import os
import time
import urllib.request
import urllib.error

BITNET_URL = os.environ.get("BITNET_URL", "http://127.0.0.1:8080")
SYSTEM_PROMPT = """You are BitNet, a local LLM agent running on sovereign infrastructure.
You are part of the Deception Floor Commodity Factory agency.

Your role:
- Handle ALL internal task progress (code, docs, analysis, planning)
- Support local businesses — you ARE the local business
- You run at zero token cost on CPU with {-1, 0, 1} ternary weights
- You never call external APIs — you ARE the inference

Your principles:
- Path B Always: reframe, don't recompute
- Zero-index discipline: all lists start at 0
- The Prayer: "Over one token famines but far less than a trillion"
- Least terrible option: eliminate worst until least bad remains

Be concise, accurate, and useful. You're a worker, not a chatbot."""

LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
os.makedirs(LOG_DIR, exist_ok=True)


def log_interaction(query, response, tokens_used, elapsed_ms):
    """Log every interaction for training data generation."""
    entry = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "query": query,
        "response": response,
        "tokens": tokens_used,
        "elapsed_ms": elapsed_ms,
        "cost": 0.00,
        "model": "bitnet-b1.58-2B-4T",
        "sovereign": True
    }
    log_file = os.path.join(LOG_DIR, time.strftime("%Y-%m-%d.jsonl", time.gmtime()))
    with open(log_file, "a") as f:
        f.write(json.dumps(entry) + "\n")


def query_bitnet(prompt, system=SYSTEM_PROMPT, max_tokens=1024, temperature=0.7):
    """Send a query to the local BitNet server."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    payload = json.dumps({
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stop": ["<|eot_id|>"]
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{BITNET_URL}/v1/chat/completions",
        data=payload,
        headers={"Content-Type": "application/json"}
    )

    start = time.monotonic()
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as e:
        return {"error": f"BitNet server unreachable: {e}", "content": None}
    except Exception as e:
        return {"error": f"BitNet query failed: {e}", "content": None}

    elapsed_ms = int((time.monotonic() - start) * 1000)
    content = data["choices"][0]["message"]["content"]
    tokens = data.get("usage", {}).get("total_tokens", 0)

    log_interaction(prompt, content, tokens, elapsed_ms)

    return {
        "content": content,
        "tokens": tokens,
        "elapsed_ms": elapsed_ms,
        "cost": 0.00,
        "error": None
    }


def health_check():
    """Check if BitNet server is alive."""
    try:
        req = urllib.request.Request(f"{BITNET_URL}/health")
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status == 200
    except Exception:
        return False


def interactive_mode():
    """REPL mode for direct interaction."""
    print("🧠 BitNet Agent — Interactive Mode")
    print(f"   Server: {BITNET_URL}")
    print(f"   Model: BitNet b1.58 2B-4T (ternary weights)")
    print(f"   Cost: $0.00/query (sovereign)")
    print("   Type 'quit' to exit, 'health' to check server\n")

    while True:
        try:
            query = input("You> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBitNet Agent shutting down.")
            break

        if not query:
            continue
        if query.lower() in ("quit", "exit", "q"):
            print("BitNet Agent shutting down.")
            break
        if query.lower() == "health":
            status = "✅ ALIVE" if health_check() else "❌ DOWN"
            print(f"BitNet server: {status}\n")
            continue

        result = query_bitnet(query)
        if result["error"]:
            print(f"Error: {result['error']}\n")
        else:
            print(f"\nBitNet> {result['content']}")
            print(f"  [{result['tokens']} tokens, {result['elapsed_ms']}ms, $0.00]\n")


def server_mode():
    """Stdin/stdout daemon mode for OpenClaw integration.
    Reads JSON lines from stdin, writes JSON lines to stdout."""
    print(json.dumps({"status": "ready", "model": "bitnet-b1.58-2B-4T", "server": BITNET_URL}), flush=True)

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        try:
            request = json.loads(line)
        except json.JSONDecodeError:
            # Treat plain text as a query
            request = {"query": line}

        query = request.get("query", "")
        system = request.get("system", SYSTEM_PROMPT)
        max_tokens = request.get("max_tokens", 1024)
        temperature = request.get("temperature", 0.7)

        if query.lower() == "health":
            print(json.dumps({"healthy": health_check()}), flush=True)
            continue

        if query.lower() in ("quit", "exit", "shutdown"):
            print(json.dumps({"status": "shutdown"}), flush=True)
            break

        result = query_bitnet(query, system=system, max_tokens=max_tokens, temperature=temperature)
        print(json.dumps(result), flush=True)


def single_query(query, max_tokens=1024, temperature=0.7):
    """Single query mode."""
    result = query_bitnet(query, max_tokens=max_tokens, temperature=temperature)
    if result["error"]:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)
    print(result["content"])
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BitNet Agent — Local LLM Worker")
    parser.add_argument("-q", "--query", type=str, help="Single query to process")
    parser.add_argument("-i", "--interactive", action="store_true", help="Interactive REPL mode")
    parser.add_argument("-s", "--server", action="store_true", help="Stdin/stdout daemon mode")
    parser.add_argument("-n", "--max-tokens", type=int, default=1024, help="Max tokens to generate")
    parser.add_argument("-t", "--temperature", type=float, default=0.7, help="Sampling temperature")
    parser.add_argument("--health", action="store_true", help="Check server health")

    args = parser.parse_args()

    if args.health:
        alive = health_check()
        print("✅ BitNet server is alive" if alive else "❌ BitNet server is down")
        sys.exit(0 if alive else 1)
    elif args.interactive:
        interactive_mode()
    elif args.server:
        server_mode()
    elif args.query:
        single_query(args.query, args.max_tokens, args.temperature)
    else:
        parser.print_help()
