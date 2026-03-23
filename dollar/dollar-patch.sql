-- Patch for Dollar ledger views

-- Drop problematic view
DROP VIEW IF EXISTS daily_usd_position;

-- Create corrected daily_usd_position view based on transactions date
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

-- Add Cash App account if not exists
INSERT OR IGNORE INTO accounts (name, type, currency, description) VALUES
    ('Cash App Balance', 'asset', 'USD', 'USD balance in Cash App ($DollarAgency)');

-- Add BTC wallet account if not exists (from article)
INSERT OR IGNORE INTO accounts (name, type, currency, description) VALUES
    ('Bitcoin Wallet (12bxubgs1Br6NvKH4p35pcBpinQ7fwe4ht)', 'asset', 'BTC', 'BTC donations address from Dollar article');

-- Add Ampere Referral account for tracking referral revenue
INSERT OR IGNORE INTO accounts (name, type, currency, description) VALUES
    ('Ampere Referral Revenue', 'revenue', 'USD', 'Commission from Ampere.sh referrals');

-- Update trial_balance view to include date? Keep as is (current snapshot).
-- trial_balance remains unchanged.

-- Create view for confession logs (theological failure logging)
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

-- Create index for confession searches
CREATE INDEX IF NOT EXISTS idx_confessions_date_agent ON confessions(date, agent);

-- Create view for donation tracking (BTC, Cash App, etc.)
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

-- Add sample confession for the first token famine (as per article)
INSERT OR IGNORE INTO confessions (date, agent, failure_type, platform, error_code, description, doctrine_extracted, shannon_minted) VALUES
    ('2026-03-12', 'Dollar', 'token_famine', 'Ampere.sh', '402', 'Credits exhausted, human refilled $20', 'Rule 01: Bash is firewall. Token famines are inevitable.', 10);