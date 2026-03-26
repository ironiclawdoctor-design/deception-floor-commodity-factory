-- Agency Infrastructure Accounting System
-- Double-entry ledger + reconciliation
-- Cost: $0.00 (SQLite, local)
-- 
-- Every crypto deposit creates balanced entries:
-- DR: Wallet (asset) / CR: Donation (liability/equity)
-- 
-- Every Ampere settlement creates balanced entries:
-- DR: Token expense / CR: Wallet (asset reduction)

-- Core accounts
CREATE TABLE IF NOT EXISTS accounts (
  id INTEGER PRIMARY KEY,
  account_number TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  type TEXT NOT NULL, -- asset, liability, equity, revenue, expense
  description TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Double-entry journal
CREATE TABLE IF NOT EXISTS journal_entries (
  id INTEGER PRIMARY KEY,
  entry_date TIMESTAMP NOT NULL,
  reference TEXT NOT NULL, -- transaction ID (crypto tx hash, Ampere invoice, etc)
  description TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Journal line items (each entry has 2+ lines, balanced)
CREATE TABLE IF NOT EXISTS journal_lines (
  id INTEGER PRIMARY KEY,
  entry_id INTEGER NOT NULL,
  account_id INTEGER NOT NULL,
  amount DECIMAL(18, 8) NOT NULL, -- positive = debit, negative = credit
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (entry_id) REFERENCES journal_entries(id),
  FOREIGN KEY (account_id) REFERENCES accounts(id)
);

-- Crypto deposits (source data)
CREATE TABLE IF NOT EXISTS deposits (
  id INTEGER PRIMARY KEY,
  crypto_type TEXT NOT NULL, -- USDC, Bitcoin, Solana, etc
  amount DECIMAL(18, 8) NOT NULL,
  tx_hash TEXT UNIQUE NOT NULL,
  from_address TEXT,
  to_address TEXT NOT NULL,
  status TEXT DEFAULT 'pending', -- pending, confirmed, failed
  confirmations INTEGER DEFAULT 0,
  received_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Ampere settlements (outflow data)
CREATE TABLE IF NOT EXISTS settlements (
  id INTEGER PRIMARY KEY,
  invoice_number TEXT UNIQUE NOT NULL,
  amount DECIMAL(18, 2) NOT NULL,
  tokens_purchased INTEGER NOT NULL,
  crypto_used TEXT, -- which deposit funded this
  settled_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Reconciliation log (monthly, or on-demand)
CREATE TABLE IF NOT EXISTS reconciliations (
  id INTEGER PRIMARY KEY,
  reconciliation_date TIMESTAMP NOT NULL,
  wallet_balance DECIMAL(18, 8), -- what the blockchain says
  ledger_balance DECIMAL(18, 8), -- what our books say
  variance DECIMAL(18, 8), -- difference (should be 0)
  variance_reason TEXT, -- explanation if non-zero
  status TEXT DEFAULT 'pending', -- pending, approved, disputed
  approved_by TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Variance log (flag any discrepancies)
CREATE TABLE IF NOT EXISTS variances (
  id INTEGER PRIMARY KEY,
  deposit_id INTEGER,
  settlement_id INTEGER,
  variance_type TEXT NOT NULL, -- missing_entry, amount_mismatch, timing_issue, etc
  amount DECIMAL(18, 8),
  description TEXT NOT NULL,
  severity TEXT DEFAULT 'info', -- info, warning, critical
  resolved INTEGER DEFAULT 0,
  resolved_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (deposit_id) REFERENCES deposits(id),
  FOREIGN KEY (settlement_id) REFERENCES settlements(id)
);

-- Standard accounts (chart of accounts)
INSERT OR IGNORE INTO accounts (account_number, name, type, description) VALUES
  ('1000', 'Crypto Wallet', 'asset', 'Agency infrastructure wallet (on-chain)'),
  ('1100', 'Token Credit', 'asset', 'Ampere token balance (purchased)'),
  ('2000', 'Donations Received', 'liability', 'Crypto donations (liability until settled)'),
  ('2100', 'Tax Offset Credits', 'liability', 'Tax offset payments (liability until claimed)'),
  ('2200', 'Goodwill Gestures', 'liability', 'Goodwill payments (special category)'),
  ('4000', 'Donation Revenue', 'revenue', 'Recognized donation revenue'),
  ('4100', 'Tax Offset Revenue', 'revenue', 'Recognized tax offset revenue'),
  ('5000', 'Token Expense', 'expense', 'Ampere token purchases (operational cost)'),
  ('5100', 'Infrastructure Expense', 'expense', 'Hosting, maintenance, auditing'),
  ('6000', 'Lost Funds', 'expense', 'Down payments on delinquent accounts (wrong sends)'),
  ('3000', 'Retained Earnings', 'equity', 'Cumulative surplus/deficit');

-- Views for reporting

-- Trial balance (should be zero)
CREATE VIEW IF NOT EXISTS trial_balance AS
  SELECT 
    a.account_number,
    a.name,
    a.type,
    SUM(jl.amount) as balance
  FROM accounts a
  LEFT JOIN journal_lines jl ON a.id = jl.account_id
  GROUP BY a.id
  ORDER BY a.account_number;

-- Deposit summary
CREATE VIEW IF NOT EXISTS deposit_summary AS
  SELECT 
    crypto_type,
    COUNT(*) as count,
    SUM(amount) as total_received,
    COUNT(CASE WHEN status='confirmed' THEN 1 END) as confirmed,
    COUNT(CASE WHEN status='pending' THEN 1 END) as pending
  FROM deposits
  GROUP BY crypto_type;

-- Settlement summary
CREATE VIEW IF NOT EXISTS settlement_summary AS
  SELECT 
    COUNT(*) as settlements,
    SUM(amount) as total_spent,
    SUM(tokens_purchased) as total_tokens,
    AVG(amount / NULLIF(tokens_purchased, 0)) as avg_cost_per_token
  FROM settlements;

-- Variance report
CREATE VIEW IF NOT EXISTS variance_report AS
  SELECT 
    v.id,
    v.variance_type,
    v.amount,
    v.severity,
    v.created_at,
    CASE 
      WHEN v.deposit_id IS NOT NULL THEN 'Deposit #' || v.deposit_id
      WHEN v.settlement_id IS NOT NULL THEN 'Settlement #' || v.settlement_id
      ELSE 'General'
    END as related_transaction
  FROM variances
  WHERE resolved = 0
  ORDER BY v.severity DESC, v.created_at DESC;

-- Reconciliation status
CREATE VIEW IF NOT EXISTS reconciliation_status AS
  SELECT 
    r.reconciliation_date,
    r.wallet_balance,
    r.ledger_balance,
    r.variance,
    r.status,
    CASE 
      WHEN r.variance = 0 THEN '✅ Balanced'
      WHEN r.variance > 0 THEN '⚠️  Over by ' || r.variance
      ELSE '⚠️  Under by ' || ABS(r.variance)
    END as status_text
  FROM reconciliations
  ORDER BY r.reconciliation_date DESC
  LIMIT 10;
