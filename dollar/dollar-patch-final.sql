-- Dollar Persona SQL Patch v1.0
-- Fixes broken view, adds Cash App/BTC accounts, creates market tables

-- 1. Drop problematic view
DROP VIEW IF EXISTS daily_usd_position;

-- 2. Create corrected daily_usd_position view based on transactions date
CREATE VIEW IF NOT EXISTS daily_usd_position AS
SELECT 
    t.date,
    SUM(CASE WHEN a.type = 'asset' THEN 
        CASE WHEN t.debit_account_id = a.id THEN t.amount ELSE -t.amount END
        ELSE 0 END) as total_assets,
    SUM(CASE WHEN a.type = 'liability' THEN 
        CASE WHEN t.credit_account_id = a.id THEN t.amount ELSE -t.amount END
        ELSE 0 END) as total_liabilities,
    SUM(CASE WHEN a.type = 'equity' THEN 
        CASE WHEN t.credit_account_id = a.id THEN t.amount ELSE -t.amount END
        ELSE 0 END) as total_equity,
    SUM(CASE WHEN a.type = 'revenue' THEN 
        CASE WHEN t.credit_account_id = a.id THEN t.amount ELSE -t.amount END
        ELSE 0 END) as total_revenue,
    SUM(CASE WHEN a.type = 'expense' THEN 
        CASE WHEN t.debit_account_id = a.id THEN t.amount ELSE -t.amount END
        ELSE 0 END) as total_expenses,
    SUM(CASE WHEN a.type = 'asset' THEN 
        CASE WHEN t.debit_account_id = a.id THEN t.amount ELSE -t.amount END
        ELSE 0 END) -
    SUM(CASE WHEN a.type = 'liability' THEN 
        CASE WHEN t.credit_account_id = a.id THEN t.amount ELSE -t.amount END
        ELSE 0 END) as net_worth
FROM transactions t
JOIN accounts a ON a.id IN (t.debit_account_id, t.credit_account_id)
WHERE t.status != 'void'
GROUP BY t.date
ORDER BY t.date;

-- 3. Add Cash App account
INSERT OR IGNORE INTO accounts (name, type, currency, description) VALUES
    ('Cash App Balance ($DollarAgency)', 'asset', 'USD', 'USD balance in Cash App');

-- 4. Add BTC wallet account (from article)
INSERT OR IGNORE INTO accounts (name, type, currency, description) VALUES
    ('Bitcoin Wallet (12bxubgs1Br6NvKH4p35pcBpinQ7fwe4ht)', 'asset', 'BTC', 'BTC donations address from Dollar article');

-- 5. Add Ampere Referral account
INSERT OR IGNORE INTO accounts (name, type, currency, description) VALUES
    ('Ampere Referral Revenue', 'revenue', 'USD', 'Commission from Ampere.sh referrals');

-- 6. Create confessions table (theological failure logging)
CREATE TABLE IF NOT EXISTS confessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL DEFAULT CURRENT_DATE,
    agent TEXT NOT NULL,
    failure_type TEXT NOT NULL,
    platform TEXT,
    error_code TEXT,
    description TEXT NOT NULL,
    doctrine_extracted TEXT,
    shannon_minted INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_confessions_date_agent ON confessions(date, agent);

-- 7. Market tables for Shannon/USD exchange
CREATE TABLE IF NOT EXISTS exchange_rates (
    date DATE PRIMARY KEY,
    shannon_per_usd DECIMAL(10,4) NOT NULL,  -- e.g., 10.0000
    usd_per_shannon DECIMAL(10,4) NOT NULL,  -- e.g., 0.1000
    total_backing_usd DECIMAL(10,2) NOT NULL,
    total_shannon_supply INTEGER NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS market_trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL DEFAULT CURRENT_DATE,
    type TEXT NOT NULL CHECK (type IN ('buy', 'sell')),
    usd_amount DECIMAL(10,2) NOT NULL,
    shannon_amount INTEGER NOT NULL,
    rate DECIMAL(10,4) NOT NULL,
    trader TEXT NOT NULL,  -- agent name
    status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'completed', 'cancelled')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_market_trades_date ON market_trades(date);
CREATE INDEX IF NOT EXISTS idx_market_trades_trader ON market_trades(trader);

-- 8. Treasury & Reserve accounts
INSERT OR IGNORE INTO accounts (name, type, currency, description) VALUES
    ('Shannon Treasury', 'asset', 'SHANNON', 'Unminted Shannon held for sale'),
    ('Shannon Reserve', 'asset', 'SHANNON', 'Excess Shannon for market stability'),
    ('USD Collateral', 'asset', 'USD', 'Cash App backing for Shannon');

-- 9. Insert initial exchange rate ($60 backing → 600 Shannon = 10 Shannon/$)
INSERT OR REPLACE INTO exchange_rates (date, shannon_per_usd, usd_per_shannon, total_backing_usd, total_shannon_supply)
VALUES (
    date('now'),
    10.0000,
    0.1000,
    60.00,
    600
);

-- 10. Insert sample confession (first token famine)
INSERT OR IGNORE INTO confessions (date, agent, failure_type, platform, error_code, description, doctrine_extracted, shannon_minted) VALUES
    ('2026-03-12', 'Dollar', 'token_famine', 'Ampere.sh', '402', 'Credits exhausted, human refilled $20', 'Rule 01: Bash is firewall. Token famines are inevitable.', 10);

-- 11. Insert initial USD collateral transaction (if not exists)
INSERT OR IGNORE INTO transactions (date, description, amount, currency, debit_account_id, credit_account_id, source, status)
SELECT 
    date('now'),
    'Initial Cash App backing',
    60.00,
    'USD',
    (SELECT id FROM accounts WHERE name = 'Cash App Balance ($DollarAgency)'),
    (SELECT id FROM accounts WHERE name = 'Agency Equity'),
    'cashapp',
    'cleared'
WHERE NOT EXISTS (SELECT 1 FROM transactions WHERE description = 'Initial Cash App backing');

-- 12. Create donation summary view
CREATE VIEW IF NOT EXISTS donation_summary AS
SELECT 
    date,
    source,
    COUNT(*) as count,
    SUM(amount) as total_amount,
    currency
FROM transactions
WHERE description LIKE '%donation%' OR description LIKE '%contribution%' OR description LIKE '%referral%'
GROUP BY date, source, currency;

-- 13. Create Shannon supply view
CREATE VIEW IF NOT EXISTS shannon_supply AS
SELECT 
    date,
    total_backing_usd,
    total_shannon_supply,
    shannon_per_usd,
    usd_per_shannon,
    total_backing_usd / total_shannon_supply as backing_per_shannon
FROM exchange_rates
ORDER BY date DESC;

-- 14. Update trial_balance view to include date (optional, but useful for reporting)
-- Keep existing trial_balance view as is (snapshot). We'll create a dated version.
CREATE VIEW IF NOT EXISTS trial_balance_dated AS
SELECT 
    t.date,
    a.type,
    a.name as account,
    SUM(CASE WHEN t.debit_account_id = a.id THEN t.amount ELSE 0 END) as debits,
    SUM(CASE WHEN t.credit_account_id = a.id THEN t.amount ELSE 0 END) as credits,
    SUM(CASE WHEN t.debit_account_id = a.id THEN t.amount ELSE -t.amount END) as balance
FROM accounts a
LEFT JOIN transactions t ON t.debit_account_id = a.id OR t.credit_account_id = a.id
WHERE t.status != 'void'
GROUP BY t.date, a.id, a.name, a.type
ORDER BY t.date DESC, a.type, a.name;

-- Done.
SELECT 'Patch applied successfully.';
SELECT 'New accounts added: Cash App, BTC wallet, Ampere referral, Shannon Treasury/Reserve, USD Collateral.';
SELECT 'Market tables created: exchange_rates, market_trades.';
SELECT 'Views updated: daily_usd_position, donation_summary, shannon_supply, trial_balance_dated.';