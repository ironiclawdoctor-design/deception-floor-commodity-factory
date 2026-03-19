import express from 'express';
import { db } from './db.js';

const app = express();
app.use(express.json());

const PORT = 9001; // Different from deception floor factory (9000)

// Health endpoint
app.get('/health', (req, res) => {
    res.json({ status: 'ok', economy: 'entropy', timestamp: new Date().toISOString() });
});

// Get agent balance
app.get('/balance/:agentName', async (req, res) => {
    try {
        const balance = await db.getAgentBalance(req.params.agentName);
        if (balance === null) {
            return res.status(404).json({ error: 'Agent not found' });
        }
        res.json({ agent: req.params.agentName, balance_shannon: balance });
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: err.message });
    }
});

// Mint entropy (internal use only, should be authenticated)
app.post('/mint', async (req, res) => {
    const { agent, amount, type, description } = req.body;
    if (!agent || !amount || !type) {
        return res.status(400).json({ error: 'Missing required fields' });
    }
    try {
        const result = await db.mintEntropy(agent, amount, type, description);
        res.json(result);
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: err.message });
    }
});

// Mint security entropy for mutation detection
app.post('/mint/security', async (req, res) => {
    const { agent, amount, description, reference, severity } = req.body;
    if (!agent || !amount) {
        return res.status(400).json({ error: 'Missing agent or amount' });
    }
    try {
        const result = await db.mintEntropy(agent, amount, 'security', description);
        // Optionally record in intrusion_events
        res.json({ ...result, severity, reference });
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: err.message });
    }
});

// Debt: advance mint (negative balance allowed)
app.post('/debt/advance', async (req, res) => {
    const { agent, amount, description, maxDebt } = req.body;
    if (!agent || !amount) {
        return res.status(400).json({ error: 'Missing agent or amount' });
    }
    const ceiling = maxDebt || 500;
    try {
        const currentBalance = await db.getAgentBalance(agent);
        if (currentBalance === null) {
            return res.status(404).json({ error: `Agent ${agent} not found` });
        }
        const projectedBalance = currentBalance - amount;
        if (projectedBalance < -ceiling) {
            return res.status(403).json({
                error: 'Debt ceiling breach',
                currentBalance,
                requestedDebit: amount,
                projectedBalance,
                maxDebt: -ceiling
            });
        }
        // Debit: subtract from wallet, record as negative mint
        const result = await db.mintEntropy(agent, -amount, 'debt_advance', description || 'Advance against future work');
        res.json({ ...result, debt: Math.min(0, result.newBalance), projectedBalance });
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: err.message });
    }
});

// Debt: garnish payroll (auto-repay on earn)
app.post('/debt/garnish', async (req, res) => {
    const { agent, grossPayout, garnishmentRate, description } = req.body;
    if (!agent || !grossPayout) {
        return res.status(400).json({ error: 'Missing agent or grossPayout' });
    }
    const rate = garnishmentRate || 0.50;
    try {
        const currentBalance = await db.getAgentBalance(agent);
        if (currentBalance === null) {
            return res.status(404).json({ error: `Agent ${agent} not found` });
        }
        if (currentBalance >= 0) {
            // Not in debt — full payout
            const result = await db.mintEntropy(agent, grossPayout, 'payroll', description || 'Standard payroll');
            return res.json({ ...result, garnished: 0, netPayout: grossPayout, debtRemaining: 0 });
        }
        // In debt — garnish
        const garnished = Math.round(grossPayout * rate);
        const netPayout = grossPayout - garnished;
        const result = await db.mintEntropy(agent, netPayout, 'payroll_garnished', description || `Garnished payroll (${Math.round(rate*100)}% to debt)`);
        res.json({ ...result, garnished, netPayout, debtRemaining: Math.min(0, result.newBalance) });
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: err.message });
    }
});

// Autograph: mint Shannon for GMRC compliance
app.post('/autograph', async (req, res) => {
    const { agent, event, description } = req.body;
    if (!agent || !event) {
        return res.status(400).json({ error: 'Missing agent or event' });
    }
    const rewards = {
        'compliance': 1,
        'introduction': 5,
        'conversion': 15,
        'retention': 25,
        'referral': 50
    };
    const penalties = {
        'missing': -2,
        'buried': -1,
        'oversell': -3
    };
    const amount = rewards[event] || penalties[event];
    if (!amount) {
        return res.status(400).json({ error: `Unknown event: ${event}. Valid: ${Object.keys({...rewards,...penalties}).join(', ')}` });
    }
    const entropyType = amount > 0 ? `autograph_${event}` : `autograph_violation_${event}`;
    try {
        const result = await db.mintEntropy(agent, amount, entropyType, description || `Autograph ${event}`);
        res.json({ ...result, event, amount, type: amount > 0 ? 'reward' : 'penalty' });
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: err.message });
    }
});

// Debt: agency-wide exposure report
app.get('/debt/exposure', async (req, res) => {
    try {
        const agents = await db.listAgents();
        const inDebt = agents.filter(a => a.balance_shannon < 0);
        const totalDebt = inDebt.reduce((sum, a) => sum + a.balance_shannon, 0);
        const frozen = totalDebt < -5000;
        res.json({
            agentsInDebt: inDebt.length,
            totalAgents: agents.length,
            totalDebt,
            frozen,
            freezeThreshold: -5000,
            unfreezeAt: -2500,
            agents: inDebt.map(a => ({ name: a.name, balance: a.balance_shannon }))
        });
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: err.message });
    }
});

// Transfer entropy
app.post('/transfer', async (req, res) => {
    const { from, to, amount, description } = req.body;
    if (!from || !to || !amount) {
        return res.status(400).json({ error: 'Missing required fields' });
    }
    try {
        const result = await db.transferEntropy(from, to, amount, description);
        res.json(result);
    } catch (err) {
        console.error(err);
        res.status(400).json({ error: err.message });
    }
});

// List all agents with balances
app.get('/agents', async (req, res) => {
    try {
        const agents = await db.listAgents();
        res.json({ agents });
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: err.message });
    }
});

// Market orders (placeholder)
app.get('/market', (req, res) => {
    res.json({ message: 'Market endpoint not yet implemented' });
});

app.listen(PORT, () => {
    console.log(`Entropy Economy API listening on port ${PORT}`);
    console.log(`Health check: http://localhost:${PORT}/health`);
});