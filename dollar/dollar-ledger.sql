-- Dollar Persona Financial Ledger
-- SQLite schema for double-entry accounting

-- Accounts (Chart of Accounts)
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('asset', 'liability', 'equity', 'revenue', 'expense')),
    currency TEXT NOT NULL DEFAULT 'USD',
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert default accounts
INSERT OR IGNORE INTO accounts (name, type, description) VALUES
    ('PayPal Balance', 'asset', 'USD balance in PayPal account'),
    ('Bank Account', 'asset', 'Primary bank account'),
    ('Bitcoin Wallet', 'asset', 'BTC holdings'),
    ('USDC Wallet', 'asset', 'USDC holdings'),
    ('Accounts Receivable', 'asset', 'Money owed to agency'),
    ('Accounts Payable', 'liability', 'Money agency owes'),
    ('Agency Equity', 'equity', 'Owner''s equity in agency'),
    ('Revenue - Services', 'revenue', 'Income from services'),
    ('Revenue - Donations', 'revenue', 'Donation income'),
    ('Expense - Hosting', 'expense', 'Ampere.sh hosting costs'),
    ('Expense - Tokens', 'expense', 'LLM token costs'),
    ('Expense - Development', 'expense', 'Developer costs');

-- Transactions (Double-entry journal)
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL DEFAULT CURRENT_DATE,
    description TEXT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    currency TEXT NOT NULL DEFAULT 'USD',
    debit_account_id INTEGER NOT NULL,
    credit_account_id INTEGER NOT NULL,
    source TEXT,  -- e.g., 'paypal', 'bitcoin', 'bank'
    reference TEXT,  -- transaction ID, invoice number
    status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'cleared', 'reconciled', 'void')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (debit_account_id) REFERENCES accounts(id),
    FOREIGN KEY (credit_account_id) REFERENCES accounts(id)
);

-- Daily balance snapshots
CREATE TABLE IF NOT EXISTS balances (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL DEFAULT CURRENT_DATE,
    account_id INTEGER NOT NULL,
    balance DECIMAL(10,2) NOT NULL,
    currency TEXT NOT NULL DEFAULT 'USD',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(id),
    UNIQUE(date, account_id)
);

-- Budgets per agent/department
CREATE TABLE IF NOT EXISTS budgets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,  -- e.g., 'engineering', 'marketing', 'fiesta'
    period TEXT NOT NULL CHECK (period IN ('daily', 'weekly', 'monthly')),
    amount DECIMAL(10,2) NOT NULL,
    currency TEXT NOT NULL DEFAULT 'USD',
    start_date DATE NOT NULL,
    end_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Budget usage tracking
CREATE TABLE IF NOT EXISTS budget_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    budget_id INTEGER NOT NULL,
    transaction_id INTEGER NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    date DATE NOT NULL DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (budget_id) REFERENCES budgets(id),
    FOREIGN KEY (transaction_id) REFERENCES transactions(id)
);

-- Reconciliation records (bank/crypto vs ledger)
CREATE TABLE IF NOT EXISTS reconciliations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL DEFAULT CURRENT_DATE,
    account_id INTEGER NOT NULL,
    external_balance DECIMAL(10,2) NOT NULL,
    ledger_balance DECIMAL(10,2) NOT NULL,
    difference DECIMAL(10,2) NOT NULL,
    status TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open', 'resolved', 'investigating')),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(id)
);

-- Shannon minting events for financial activities
CREATE TABLE IF NOT EXISTS shannon_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL DEFAULT CURRENT_DATE,
    agent TEXT NOT NULL,
    event_type TEXT NOT NULL CHECK (event_type IN ('revenue', 'cost_saving', 'report', 'budget_compliance', 'certification')),
    amount_usd DECIMAL(10,2),
    shannon_minted INTEGER NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(date);
CREATE INDEX IF NOT EXISTS idx_transactions_debit ON transactions(debit_account_id);
CREATE INDEX IF NOT EXISTS idx_transactions_credit ON transactions(credit_account_id);
CREATE INDEX IF NOT EXISTS idx_balances_date_account ON balances(date, account_id);
CREATE INDEX IF NOT EXISTS idx_budget_usage_date ON budget_usage(date);
CREATE INDEX IF NOT EXISTS idx_shannon_events_date_agent ON shannon_events(date, agent);

-- View: Trial Balance (debits - credits must sum to zero)
CREATE VIEW IF NOT EXISTS trial_balance AS
SELECT 
    a.type,
    a.name as account,
    SUM(CASE WHEN t.debit_account_id = a.id THEN t.amount ELSE 0 END) as debits,
    SUM(CASE WHEN t.credit_account_id = a.id THEN t.amount ELSE 0 END) as credits,
    SUM(CASE WHEN t.debit_account_id = a.id THEN t.amount ELSE -t.amount END) as balance
FROM accounts a
LEFT JOIN transactions t ON t.debit_account_id = a.id OR t.credit_account_id = a.id
WHERE t.status != 'void'
GROUP BY a.id, a.name, a.type
ORDER BY a.type, a.name;

-- View: Daily USD Position
CREATE VIEW IF NOT EXISTS daily_usd_position AS
SELECT 
    date,
    SUM(CASE WHEN a.type = 'asset' THEN balance ELSE 0 END) as total_assets,
    SUM(CASE WHEN a.type = 'liability' THEN balance ELSE 0 END) as total_liabilities,
    SUM(CASE WHEN a.type = 'equity' THEN balance ELSE 0 END) as total_equity,
    SUM(CASE WHEN a.type = 'revenue' THEN balance ELSE 0 END) as total_revenue,
    SUM(CASE WHEN a.type = 'expense' THEN balance ELSE 0 END) as total_expenses,
    (SUM(CASE WHEN a.type = 'asset' THEN balance ELSE 0 END) -
     SUM(CASE WHEN a.type = 'liability' THEN balance ELSE 0 END)) as net_worth
FROM trial_balance
GROUP BY date;

-- View: Monthly Budget vs Actual
CREATE VIEW IF NOT EXISTS monthly_budget_vs_actual AS
SELECT 
    strftime('%Y-%m', b.start_date) as month,
    b.name as budget_name,
    b.amount as budget_amount,
    COALESCE(SUM(bu.amount), 0) as actual_spent,
    b.amount - COALESCE(SUM(bu.amount), 0) as remaining,
    CASE 
        WHEN COALESCE(SUM(bu.amount), 0) > b.amount THEN 'OVER'
        WHEN COALESCE(SUM(bu.amount), 0) > b.amount * 0.8 THEN 'WARNING'
        ELSE 'OK'
    END as status
FROM budgets b
LEFT JOIN budget_usage bu ON bu.budget_id = b.id
WHERE b.period = 'monthly'
GROUP BY month, b.name, b.amount;