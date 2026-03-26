import express from 'express';
import { db } from './db.js';
import path from 'path';
import { fileURLToPath } from 'url';
import expressLayouts from 'express-ejs-layouts';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
app.use(express.json());
app.use(expressLayouts);
app.set('view engine', 'ejs');
app.set('layout', 'layout');

const PORT = 8000;

app.get('/', async (req, res) => {
    const agents = await db.listAgents();
    const total = agents.reduce((s, a) => s + a.balance_shannon, 0);
    res.render('pages/index', { title: 'Console', agents, shannonTotal: total.toLocaleString() });
});

app.get('/most-wanted', (req, res) => { 
    res.render('pages/most-wanted', { title: 'Most Wanted' }); 
});

app.get('/comic-con', (req, res) => { 
    res.render('pages/text', { title: 'Comic Con', content: '<h3>🛡️ Blue Team Convention Hall</h3><p>Status: Maximum Vigilance.<br>Panels starting soon.</p>' }); 
});

app.get('/resistance', (req, res) => {     res.render('pages/resistance', { title: 'Resistance' }); });
app.get('/raistlin-audit', (req, res) => { 
    res.render('pages/text', { title: 'Raistlin Audit', content: '<h3>📜 Archmage Scroll</h3><p>Audit Passed. Port 9001 evacuated safely to Port 8000.</p>' }); 
});

app.post('/report-failure', async (req, res) => {
    const { reason } = req.body;
    await db.mintEntropy('fiesta', -10, 'human_error', reason);
    res.json({ success: true });
});

app.get('/dashboard', async (req, res) => { 
    res.json({ status: 'ok', entropy_agents: await db.listAgents() }); 
});

app.listen(PORT, "0.0.0.0", () => { console.log(`SSR Engine live on port ${PORT}`); });
