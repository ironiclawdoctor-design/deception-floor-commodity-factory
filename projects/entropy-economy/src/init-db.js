import sqlite3 from 'sqlite3';
import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

function runSql(db, sql) {
    return new Promise((resolve, reject) => {
        db.exec(sql, (err) => {
            if (err) reject(err);
            else resolve();
        });
    });
}

function runQuery(db, sql, params = []) {
    return new Promise((resolve, reject) => {
        db.run(sql, params, function(err) {
            if (err) reject(err);
            else resolve(this);
        });
    });
}

function allQuery(db, sql, params = []) {
    return new Promise((resolve, reject) => {
        db.all(sql, params, (err, rows) => {
            if (err) reject(err);
            else resolve(rows);
        });
    });
}

function getQuery(db, sql, params = []) {
    return new Promise((resolve, reject) => {
        db.get(sql, params, (err, row) => {
            if (err) reject(err);
            else resolve(row);
        });
    });
}

async function initializeDatabase() {
    const dbPath = join(__dirname, '..', 'entropy_ledger.db');
    console.log(`Initializing entropy ledger at ${dbPath}`);

    const db = new sqlite3.Database(dbPath);

    // Read schema SQL
    const schemaPath = join(__dirname, 'schema.sql');
    const schemaSql = readFileSync(schemaPath, 'utf8');

    // Execute schema
    await runSql(db, schemaSql);
    console.log('Schema created successfully.');

    // Insert default agents (Fiesta Agents)
    const agents = [
        'growth-engineer',
        'frontend-dev',
        'backend-architect',
        'ui-designer',
        'content-strategist',
        'orchestrator',
        'deception-floor-factory',
        'automate',
        'official',
        'daimyo'
    ];

    for (const agentName of agents) {
        await runQuery(db,
            'INSERT OR IGNORE INTO agents (name) VALUES (?)',
            agentName
        );
    }

    // Initialize wallets with zero balance (they will be created on first mint)
    const agentRows = await allQuery(db, 'SELECT id FROM agents');
    for (const row of agentRows) {
        await runQuery(db,
            'INSERT OR IGNORE INTO wallets (agent_id, balance_shannon) VALUES (?, 0)',
            row.id
        );
    }

    console.log(`Initialized ${agentRows.length} agents.`);

    // Mint some starter entropy for growth-engineer (as a reward for creating the economy)
    const growthEngineer = await getQuery(db, 'SELECT id FROM agents WHERE name = ?', 'growth-engineer');
    if (growthEngineer) {
        await runQuery(db,
            'INSERT INTO minting_events (agent_id, amount_shannon, entropy_type, source_description) VALUES (?, ?, ?, ?)',
            growthEngineer.id, 1000, 'creative', 'Founder reward for designing entropy economy'
        );
        await runQuery(db,
            'UPDATE wallets SET balance_shannon = balance_shannon + ? WHERE agent_id = ?',
            1000, growthEngineer.id
        );
        console.log('Minted 1000 Sh for growth-engineer.');
    }

    db.close();
    console.log('Entropy ledger initialization complete.');
}

initializeDatabase().catch(err => {
    console.error('Failed to initialize database:', err);
    process.exit(1);
});