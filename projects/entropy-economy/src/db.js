import sqlite3 from 'sqlite3';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import crypto from 'crypto';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const DB_PATH = join(__dirname, '..', 'entropy_ledger.db');

export class EntropyDB {
    constructor() {
        this.db = new sqlite3.Database(DB_PATH);
    }

    query(sql, ...params) {
        return new Promise((resolve, reject) => {
            this.db.all(sql, params, (err, rows) => {
                if (err) reject(err);
                else resolve(rows);
            });
        });
    }

    run(sql, ...params) {
        return new Promise((resolve, reject) => {
            this.db.run(sql, params, function(err) {
                if (err) reject(err);
                else resolve(this);
            });
        });
    }

    get(sql, ...params) {
        return new Promise((resolve, reject) => {
            this.db.get(sql, params, (err, row) => {
                if (err) reject(err);
                else resolve(row);
            });
        });
    }

    close() {
        this.db.close();
    }

    // High-level methods
    async getAgentBalance(agentName) {
        const row = await this.get(`
            SELECT w.balance_shannon
            FROM agents a
            JOIN wallets w ON a.id = w.agent_id
            WHERE a.name = ?
        `, agentName);
        return row ? row.balance_shannon : null;
    }

    async mintEntropy(agentName, amount, entropyType, description) {
        const agent = await this.get('SELECT id FROM agents WHERE name = ?', agentName);
        if (!agent) throw new Error(`Agent ${agentName} not found`);
        // Start transaction
        await this.run('BEGIN TRANSACTION');
        try {
            await this.run(
                'INSERT INTO minting_events (agent_id, amount_shannon, entropy_type, source_description) VALUES (?, ?, ?, ?)',
                agent.id, amount, entropyType, description
            );
            await this.run(
                'UPDATE wallets SET balance_shannon = balance_shannon + ? WHERE agent_id = ?',
                amount, agent.id
            );
            await this.run('COMMIT');
            return { success: true, newBalance: await this.getAgentBalance(agentName) };
        } catch (err) {
            await this.run('ROLLBACK');
            throw err;
        }
    }

    async transferEntropy(fromAgent, toAgent, amount, description = '') {
        const from = await this.get('SELECT id FROM agents WHERE name = ?', fromAgent);
        const to = await this.get('SELECT id FROM agents WHERE name = ?', toAgent);
        if (!from || !to) throw new Error('Agent not found');
        // Check balance
        const balance = await this.getAgentBalance(fromAgent);
        if (balance < amount) throw new Error('Insufficient entropy');
        await this.run('BEGIN TRANSACTION');
        try {
            // Deduct from sender
            await this.run(
                'UPDATE wallets SET balance_shannon = balance_shannon - ? WHERE agent_id = ?',
                amount, from.id
            );
            // Add to receiver
            await this.run(
                'UPDATE wallets SET balance_shannon = balance_shannon + ? WHERE agent_id = ?',
                amount, to.id
            );
            // Record transaction
            await this.run(
                'INSERT INTO transactions (from_agent, to_agent, amount_shannon, description) VALUES (?, ?, ?, ?)',
                from.id, to.id, amount, description
            );
            await this.run('COMMIT');
            return { success: true };
        } catch (err) {
            await this.run('ROLLBACK');
            throw err;
        }
    }

    async listAgents() {
        return await this.query(`
            SELECT a.name, w.balance_shannon
            FROM agents a
            LEFT JOIN wallets w ON a.id = w.agent_id
            ORDER BY w.balance_shannon DESC
        `);
    }

    async recordContribution(agentName, contributionHash, contributionType, equityPercentage = 100.0, metadata = {}) {
        const agent = await this.get('SELECT id FROM agents WHERE name = ?', agentName);
        if (!agent) throw new Error(`Agent ${agentName} not found`);
        const contributionId = crypto.randomUUID();
        const timestamp = Math.floor(Date.now() / 1000);
        const metadataStr = JSON.stringify(metadata);
        await this.run(
            `INSERT INTO ip_registry (contribution_id, agent_id, contribution_hash, contribution_type, equity_percentage, timestamp, metadata)
             VALUES (?, ?, ?, ?, ?, ?, ?)`,
            contributionId, agentName, contributionHash, contributionType, equityPercentage, timestamp, metadataStr
        );
        return contributionId;
    }

    async mintEquity(agentName, contributionId, shannonAmount) {
        const agent = await this.get('SELECT id FROM agents WHERE name = ?', agentName);
        if (!agent) throw new Error(`Agent ${agentName} not found`);
        // Verify contribution exists and belongs to agent (optional)
        const contrib = await this.get('SELECT agent_id FROM ip_registry WHERE contribution_id = ?', contributionId);
        if (!contrib) throw new Error(`Contribution ${contributionId} not found`);
        if (contrib.agent_id !== agentName) throw new Error(`Contribution belongs to another agent`);
        const timestamp = Math.floor(Date.now() / 1000);
        await this.run('BEGIN TRANSACTION');
        try {
            await this.run(
                'INSERT INTO equity_ledger (agent_id, contribution_id, shannon_amount, minted_at) VALUES (?, ?, ?, ?)',
                agentName, contributionId, shannonAmount, timestamp
            );
            await this.run(
                'UPDATE wallets SET balance_shannon = balance_shannon + ? WHERE agent_id = ?',
                shannonAmount, agent.id
            );
            await this.run('COMMIT');
            return { success: true, newBalance: await this.getAgentBalance(agentName) };
        } catch (err) {
            await this.run('ROLLBACK');
            throw err;
        }
    }
}

// Singleton instance
export const db = new EntropyDB();