#!/usr/bin/env python3
"""
Ultimatum Ideas DB — Agency Review System
Logs strategic ultimatums/directives during idle for agency review.
Runs as isolated agentTurn cron. All ideas queryable via SQLite.
"""
import sqlite3, json
from datetime import datetime
from pathlib import Path

DB = Path("/root/.openclaw/workspace/agency.db")

def init():
    conn = sqlite3.connect(DB)
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS ultimatums (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            category TEXT NOT NULL,
            title TEXT NOT NULL,
            body TEXT NOT NULL,
            priority INTEGER DEFAULT 5,
            status TEXT DEFAULT 'pending' CHECK(status IN ('pending','reviewed','adopted','rejected','deferred')),
            reviewed_by TEXT,
            shannon_reward INTEGER DEFAULT 0,
            source TEXT DEFAULT 'idle-agent'
        );
        CREATE TABLE IF NOT EXISTS llm_providers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            provider TEXT NOT NULL,
            model TEXT,
            access_type TEXT CHECK(access_type IN ('free','freemium','paid','key-required')),
            endpoint TEXT,
            api_key_env TEXT,
            daily_limit TEXT,
            notes TEXT,
            active INTEGER DEFAULT 1,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS llm_routing (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_type TEXT NOT NULL,
            preferred_provider TEXT NOT NULL,
            fallback_provider TEXT,
            cost_tier INTEGER DEFAULT 0,
            notes TEXT
        );
    """)
    conn.commit()
    return conn

def seed_ultimatums(conn):
    ideas = [
        ("security", "Rotate GCP service account key monthly", "The dollaragency SA key (a0e884fe...) was shared in chat. Rotate monthly minimum. Add rotation reminder cron.", 9, 10),
        ("revenue", "Publish article #2: theological-financial hybrid", "Dollar persona has Catholic theology + financial tracking. Write dev.to article #2 referencing BTC address + Ampere referral. Shannon minting trigger on publish.", 8, 25),
        ("infrastructure", "Enable Cloud Run API via GCP Console before next cron", "Single action: visit console.cloud.google.com/apis/library/run.googleapis.com?project=sovereign-see and click Enable. Unblocks everything.", 10, 0),
        ("security", "Add secondary Cash App backing account", "Single point of failure: $DollarAgency is the only backing. Add secondary reserve (BTC wallet counts if spendability verified).", 7, 5),
        ("distribution", "Apply shannon-new-events.sql to activate autonomous minting", "5 triggers ready. 18 Shannon/day safe rate. 24-day runway. Apply SQL file to dollar.db to start autonomous minting.", 9, 15),
        ("governance", "Adopt AUTONOMOUS-v2.md decision tree", "Circuit breaker, exponential backoff, token caching. Replace v1 decision tree. Safer for extended autonomous operation.", 8, 10),
        ("revenue", "Set up Square API for real-time Cash App balance", "square_access_token in cashapp.json is NEEDS_TOKEN. Get real token at developer.squareup.com/apps. Unlocks live balance polling.", 7, 5),
        ("distribution", "Shannon distribution: mint outward faster to reduce attack surface", "Autoresearch finding: hoarding invites attack. Velocity = defense. Distribute Shannon to contributors before day 20.", 8, 0),
        ("infrastructure", "Build Docker image for Dollar dashboard", "Cloud Run needs real image. Current placeholder is google-samples/hello-app. Build actual Dollar dashboard container.", 6, 20),
        ("governance", "Certify all fiesta-agents via certification-officer", "64 agents, none formally certified. Run certification pipeline: certification-officer evaluates, assigns L1/L2/L3.", 5, 30),
    ]
    for cat, title, body, priority, reward in ideas:
        existing = conn.execute("SELECT id FROM ultimatums WHERE title = ?", (title,)).fetchone()
        if not existing:
            conn.execute(
                "INSERT INTO ultimatums (category, title, body, priority, shannon_reward, source) VALUES (?,?,?,?,?,'idle-seed')",
                (cat, title, body, priority, reward)
            )
    conn.commit()

def seed_llm_providers(conn):
    providers = [
        ("OpenRouter Free", "openrouter", "deepseek/deepseek-v3.2", "freemium", "https://openrouter.ai/api/v1", "OPENROUTER_API_KEY", "varies", "Current main model. Free tier available."),
        ("Groq (Llama 3.3 70B)", "groq", "llama-3.3-70b-versatile", "freemium", "https://api.groq.com/openai/v1", "GROQ_API_KEY", "14,400 req/day", "Fast inference, generous free tier. Good for Tier 1 tasks."),
        ("Groq (Llama 3.1 8B)", "groq", "llama-3.1-8b-instant", "freemium", "https://api.groq.com/openai/v1", "GROQ_API_KEY", "14,400 req/day", "Ultra-fast, free. Use for bash-tier routing decisions."),
        ("Google Gemini Flash", "google", "gemini-1.5-flash-latest", "freemium", "https://generativelanguage.googleapis.com/v1beta", "GEMINI_API_KEY", "1,500 req/day", "Free via GCP sovereign-see. Use service account."),
        ("Cloudflare Workers AI", "cloudflare", "@cf/meta/llama-3.1-8b-instruct", "free", "https://api.cloudflare.com/client/v4/accounts/{id}/ai/run", "CF_API_TOKEN", "unlimited (rate limited)", "Free forever on Cloudflare Workers. No key needed for basic use."),
        ("Ollama (local)", "ollama", "llama3.2", "free", "http://localhost:11434/api", None, "unlimited", "Local inference. Zero cost. Needs GPU or fast CPU."),
        ("HuggingFace Inference", "huggingface", "meta-llama/Meta-Llama-3-8B-Instruct", "freemium", "https://api-inference.huggingface.co/models", "HF_TOKEN", "limited", "Free tier with HF token. Good for experimentation."),
        ("Mistral Le Chat", "mistral", "mistral-small-latest", "freemium", "https://api.mistral.ai/v1", "MISTRAL_API_KEY", "1B tokens free", "Free tier generous. Good European alternative."),
        ("Grok (xAI)", "xai", "grok-beta", "freemium", "https://api.x.ai/v1", "XAI_API_KEY", "25 req/hr free", "Real-time web search. Already configured as skill."),
    ]
    for name, provider, model, access, endpoint, key_env, limit, notes in providers:
        existing = conn.execute("SELECT id FROM llm_providers WHERE name = ?", (name,)).fetchone()
        if not existing:
            conn.execute(
                "INSERT INTO llm_providers (name, provider, model, access_type, endpoint, api_key_env, daily_limit, notes) VALUES (?,?,?,?,?,?,?,?)",
                (name, provider, model, access, endpoint, key_env, limit, notes)
            )
    conn.commit()

def seed_routing(conn):
    routes = [
        ("bash-tier-decision", "Groq (Llama 3.1 8B)", "Cloudflare Workers AI", 0, "Ultra-fast, free. Route system ops here."),
        ("content-generation", "Groq (Llama 3.3 70B)", "Mistral Le Chat", 1, "Long-form content. Article #2 etc."),
        ("code-generation", "OpenRouter Free", "Groq (Llama 3.3 70B)", 1, "Current main. Fallback to Groq."),
        ("gcp-operations", "Google Gemini Flash", "OpenRouter Free", 1, "Use service account sovereign-see for free Gemini."),
        ("real-time-search", "Grok (xAI)", "OpenRouter Free", 1, "Web search tasks. Already skilled."),
        ("local-inference", "Ollama (local)", None, 0, "Zero cost. Use when latency acceptable."),
        ("agent-orchestration", "OpenRouter Free", "Groq (Llama 3.3 70B)", 2, "Complex multi-agent tasks need strong model."),
    ]
    for task, preferred, fallback, tier, notes in routes:
        existing = conn.execute("SELECT id FROM llm_routing WHERE task_type = ?", (task,)).fetchone()
        if not existing:
            conn.execute(
                "INSERT INTO llm_routing (task_type, preferred_provider, fallback_provider, cost_tier, notes) VALUES (?,?,?,?,?)",
                (task, preferred, fallback, tier, notes)
            )
    conn.commit()

def report(conn):
    print("📋 Ultimatum Ideas (top 5 by priority):")
    for row in conn.execute("SELECT priority, category, title, shannon_reward FROM ultimatums ORDER BY priority DESC LIMIT 5"):
        print(f"  [{row[0]}] {row[1].upper()} — {row[2]} (+{row[3]} Sh)")
    print()
    print("🤖 LLM Providers (free/freemium):")
    for row in conn.execute("SELECT name, access_type, daily_limit FROM llm_providers WHERE access_type IN ('free','freemium') ORDER BY access_type"):
        print(f"  {row[0]} [{row[1]}] — {row[2]}")
    print()
    print("🔀 Routing Table:")
    for row in conn.execute("SELECT task_type, preferred_provider, cost_tier FROM llm_routing ORDER BY cost_tier"):
        print(f"  {row[0]} → {row[1]} (tier {row[2]})")

if __name__ == "__main__":
    conn = init()
    seed_ultimatums(conn)
    seed_llm_providers(conn)
    seed_routing(conn)
    report(conn)
    conn.close()
    print(f"\n✅ agency.db ready at /root/.openclaw/workspace/agency.db")
