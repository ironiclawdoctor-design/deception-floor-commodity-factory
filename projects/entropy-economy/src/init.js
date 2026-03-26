import { db } from './db.js';
import { readFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

async function initialize() {
    console.log('Running entropy economy initialization...');
    // Note: tables already created by schema.sql? We'll rely on existing db.
    // For now, just ensure agents exist.
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
        await db.run(
            'INSERT OR IGNORE INTO agents (name) VALUES (?)',
            agentName
        );
        // Ensure wallet exists
        const agent = await db.get('SELECT id FROM agents WHERE name = ?', agentName);
        await db.run(
            'INSERT OR IGNORE INTO wallets (agent_id, balance_shannon) VALUES (?, 0)',
            agent.id
        );
    }

    // Mint initial entropy for growth-engineer
    try {
        const result = await db.mintEntropy('growth-engineer', 1000, 'creative', 'Founder reward');
        console.log('Minted 1000 Sh for growth-engineer:', result);
    } catch (err) {
        console.warn('Minting failed (maybe already minted):', err.message);
    }

    const all = await db.listAgents();
    console.log('Current agent balances:');
    all.forEach(a => console.log(`  ${a.name}: ${a.balance_shannon} Sh`));

    db.close();
    console.log('Initialization complete.');
}

initialize().catch(err => {
    console.error('Initialization error:', err);
    process.exit(1);
});