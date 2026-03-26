import { EntropyDB } from './src/db.js';

async function test() {
    const db = new EntropyDB();
    try {
        console.log('Testing mintEntropy...');
        // Test with automate agent
        const result = await db.mintEntropy('automate', 1000, 'initial', 'test');
        console.log('Success:', result);
    } catch (err) {
        console.error('Error:', err);
        console.error('Full error:', err.message);
    } finally {
        db.close();
    }
}

test();
