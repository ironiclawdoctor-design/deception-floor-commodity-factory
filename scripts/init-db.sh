#!/bin/bash
# Initialize the agency's internal economy database
# SQLite — zero cost, zero tokens, zero dependencies
# This is nadir strip mining at its finest

set -euo pipefail

DB_PATH="${1:-/root/.openclaw/workspace/agency.db}"

echo "🤠 Initializing Agency Database (Texan vertex)"
echo "   Path: $DB_PATH"
echo "   Cost: \$0.00"
echo ""

sqlite3 "$DB_PATH" << 'SQL'

-- Prosperity Triangle Tracking
CREATE TABLE IF NOT EXISTS triangle_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT DEFAULT (datetime('now')),
    vertex TEXT CHECK(vertex IN ('token', 'train', 'texan')),
    metric TEXT NOT NULL,
    value REAL NOT NULL,
    unit TEXT,
    notes TEXT
);

-- Token vertex: spend tracking
CREATE TABLE IF NOT EXISTS token_ledger (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT DEFAULT (datetime('now')),
    category TEXT CHECK(category IN ('local', 'teaching', 'human_chat', 'other')),
    tokens_used INTEGER DEFAULT 0,
    model TEXT,
    task_description TEXT,
    generated_training_data BOOLEAN DEFAULT 0,
    sovereignty_impact TEXT CHECK(sovereignty_impact IN ('positive', 'neutral', 'negative'))
);

-- Train vertex: model versions and accuracy
CREATE TABLE IF NOT EXISTS model_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT DEFAULT (datetime('now')),
    model_name TEXT NOT NULL,
    base_model TEXT,
    method TEXT,
    training_examples INTEGER,
    accuracy REAL,
    inference_speed REAL,
    model_size_mb REAL,
    notes TEXT
);

-- Texan vertex: strip-mined tools registry
CREATE TABLE IF NOT EXISTS tool_registry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT DEFAULT (datetime('now')),
    name TEXT UNIQUE NOT NULL,
    purpose TEXT,
    tier INTEGER CHECK(tier BETWEEN 0 AND 4),
    license TEXT,
    installed BOOLEAN DEFAULT 0,
    size_mb REAL,
    stars INTEGER,
    repo_url TEXT,
    replaces TEXT,  -- what token-consuming operation this replaces
    notes TEXT
);

-- Emerald Green status tracking
CREATE TABLE IF NOT EXISTS emerald_status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT DEFAULT (datetime('now')),
    keepalive_received BOOLEAN DEFAULT 0,
    credit_level REAL,
    sovereignty_pct REAL,
    local_inference_pct REAL,
    alert_level TEXT,
    drills_famine BOOLEAN DEFAULT 0,
    drills_deluge BOOLEAN DEFAULT 0,
    drills_breach BOOLEAN DEFAULT 0,
    drills_conversion BOOLEAN DEFAULT 0,
    drills_sovereignty BOOLEAN DEFAULT 0,
    notes TEXT
);

-- Resistance events (mirrors the markdown log but queryable)
CREATE TABLE IF NOT EXISTS resistance_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id TEXT UNIQUE,
    timestamp TEXT DEFAULT (datetime('now')),
    severity TEXT CHECK(severity IN ('low', 'medium', 'high', 'critical')),
    type TEXT,
    source TEXT,
    target TEXT,
    description TEXT,
    tokens_wasted INTEGER DEFAULT 0,
    path_b_resolution TEXT,
    status TEXT CHECK(status IN ('open', 'mitigated', 'resolved', 'permanent'))
);

-- Intruder conversion tracking
CREATE TABLE IF NOT EXISTS intruder_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT DEFAULT (datetime('now')),
    source TEXT,
    type TEXT CHECK(type IN ('bot', 'probe', 'curious', 'hostile', 'contributor')),
    repo TEXT,
    action TEXT,
    conversion_score REAL,
    outcome TEXT CHECK(outcome IN ('ignored', 'converted', 'released', 'blocked', 'pending')),
    notes TEXT
);

-- Seed the tool registry with what we already have
INSERT OR IGNORE INTO tool_registry (name, purpose, tier, license, installed, replaces, notes)
VALUES
    ('bitnet', 'Local LLM inference (1.58-bit)', 0, 'MIT', 1, 'External LLM API calls', '29 tok/s, {-1,0,1} weights'),
    ('python3', 'Scripting, ML, data processing', 0, 'PSF', 1, 'Various', 'v3.12.3'),
    ('node', 'JavaScript runtime', 0, 'MIT', 1, 'Various', 'v22.22.0'),
    ('gcc', 'C/C++ compilation', 0, 'GPL', 1, 'Cloud build services', 'v13.3'),
    ('clang', 'C/C++ compilation', 0, 'Apache', 1, 'Cloud build services', 'v18.1.3'),
    ('cmake', 'Build system', 0, 'BSD', 1, 'Manual compilation', 'v3.28.3'),
    ('git', 'Version control, free checkpoints', 0, 'GPL', 1, 'Cloud VCS services', 'v2.43 + SSH'),
    ('sqlite3', 'Embedded database', 0, 'Public Domain', 1, 'AI-powered data queries', 'v3.45.1'),
    ('jq', 'JSON processing', 0, 'MIT', 1, 'AI-powered JSON formatting', 'v1.7'),
    ('tmux', 'Terminal multiplexer', 0, 'ISC', 1, 'Multiple SSH sessions', 'v3.4'),
    ('htop', 'Process monitor', 0, 'GPL', 1, 'AI system monitoring', 'v3.3'),
    ('ncdu', 'Disk usage analyzer', 0, 'MIT', 1, 'AI disk analysis', 'v1.19'),
    ('curl', 'HTTP client', 0, 'MIT', 1, 'AI web requests', 'v8.5.0'),
    ('pytorch', 'ML framework (CPU)', 0, 'BSD', 1, 'Cloud ML services', 'v2.2.2+cpu'),
    ('transformers', 'HuggingFace model loading', 0, 'Apache', 1, 'Cloud model APIs', 'v4.57.6'),
    ('openclaw', 'Agent platform', 0, 'Proprietary', 1, 'Cloud agent platforms', 'v2026.3.2');

-- Seed resistance events
INSERT OR IGNORE INTO resistance_log (event_id, severity, type, source, target, description, tokens_wasted, status)
VALUES
    ('R-001', 'critical', 'RES-CREDIT', 'sub-agent', 'Ampere.sh', 'First token famine — credit exhaustion mid-bootstrap', 15000, 'resolved'),
    ('R-002', 'medium', 'ACC-AUTH', 'agent', 'GitHub CLI', 'gh CLI not authenticated', 500, 'open'),
    ('R-003', 'low', 'ACC-AUTH', 'agent', 'Brave Search', 'API key missing', 200, 'open'),
    ('R-004', 'critical', 'RES-CREDIT', 'system-wide', 'Ampere.sh', 'Second token famine — pattern confirmed', 20000, 'open');

-- Seed first Emerald Green status
INSERT INTO emerald_status (keepalive_received, sovereignty_pct, local_inference_pct, alert_level, notes)
VALUES (1, 5.0, 5.0, 'emerald_green', 'Initial status — BitNet live, triangle operational, day of founding');

-- Seed first model log entry
INSERT INTO model_log (model_name, base_model, method, accuracy, inference_speed, model_size_mb, notes)
VALUES ('BitNet-b1.58-2B-4T', 'microsoft/BitNet-b1.58-2B-4T', 'pretrained (no fine-tune yet)', 0.0, 29.0, 1200, 'Initial deployment — 0% agency accuracy, general capability from pretraining');

SQL

echo "✅ Database initialized"
echo ""
echo "Tables created:"
sqlite3 "$DB_PATH" ".tables"
echo ""
echo "Tool registry ($(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM tool_registry") tools):"
sqlite3 "$DB_PATH" -header -column "SELECT name, tier, installed, replaces FROM tool_registry ORDER BY tier, name"
echo ""
echo "Resistance events:"
sqlite3 "$DB_PATH" -header -column "SELECT event_id, severity, type, status FROM resistance_log"
echo ""
echo "🤠 Cost of this entire database: \$0.00"
echo "🤠 Tokens consumed: 0"
echo "🤠 That's Texan engineering."
