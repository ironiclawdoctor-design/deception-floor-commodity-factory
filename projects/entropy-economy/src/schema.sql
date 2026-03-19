-- Entropy Economy Ledger Schema
-- Version 0.1

-- Agents table (mirrors existing agency agents)
CREATE TABLE IF NOT EXISTS agents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL, -- agent name, e.g., "growth-engineer"
    public_key TEXT UNIQUE, -- Ed25519 public key for signing transactions
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT 1
);

-- Wallets table (holds Shannon balance)
CREATE TABLE IF NOT EXISTS wallets (
    agent_id INTEGER PRIMARY KEY REFERENCES agents(id) ON DELETE CASCADE,
    balance_shannon INTEGER NOT NULL DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Entropy generation events (minting)
CREATE TABLE IF NOT EXISTS minting_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id INTEGER REFERENCES agents(id),
    amount_shannon INTEGER NOT NULL,
    entropy_type TEXT NOT NULL, -- creative, deceptive, information, complexity, security
    source_description TEXT, -- e.g., "deception floor grade S", "novel output"
    source_reference TEXT, -- foreign key to other systems (e.g., floor_id)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Transactions (transfers between wallets)
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_agent INTEGER REFERENCES agents(id),
    to_agent INTEGER REFERENCES agents(id),
    amount_shannon INTEGER NOT NULL,
    entropy_type TEXT, -- optional, for tracking
    description TEXT,
    signature TEXT, -- signature of (from_agent, to_agent, amount, timestamp)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CHECK (from_agent != to_agent)
);

-- Market orders (bid/ask)
CREATE TABLE IF NOT EXISTS market_orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id INTEGER REFERENCES agents(id),
    order_type TEXT NOT NULL, -- 'bid' or 'ask'
    commodity TEXT NOT NULL, -- e.g., 'compute-time', 'deception-floor', 'agent-service'
    price_shannon INTEGER NOT NULL, -- per unit
    quantity INTEGER NOT NULL, -- units available/requested
    status TEXT DEFAULT 'open', -- 'open', 'filled', 'cancelled'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Trades (matched orders)
CREATE TABLE IF NOT EXISTS trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bid_order_id INTEGER REFERENCES market_orders(id),
    ask_order_id INTEGER REFERENCES market_orders(id),
    price_shannon INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Intrusion detection logs (security entropy)
CREATE TABLE IF NOT EXISTS intrusion_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    intruder_ip TEXT,
    intruder_fingerprint TEXT,
    attempted_action TEXT,
    entropy_generated INTEGER DEFAULT 0, -- Shannon awarded to detectors
    handled BOOLEAN DEFAULT 0
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_wallets_agent_id ON wallets(agent_id);
CREATE INDEX IF NOT EXISTS idx_minting_agent ON minting_events(agent_id);
CREATE INDEX IF NOT EXISTS idx_transactions_from ON transactions(from_agent);
CREATE INDEX IF NOT EXISTS idx_transactions_to ON transactions(to_agent);
CREATE INDEX IF NOT EXISTS idx_market_orders_status ON market_orders(status, commodity);
CREATE INDEX IF NOT EXISTS idx_intrusion_detected ON intrusion_events(detected_at);