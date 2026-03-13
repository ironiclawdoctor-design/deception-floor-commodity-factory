#!/usr/bin/env node
/**
 * Master-Slave IDE
 * Integrated Development Environment where Master coordinates, Slave executes
 * 
 * Architecture:
 * - Master: coordinates tasks, maintains state, routes work
 * - Slave: executes commands, returns results, stateless
 * 
 * Key principle: Slave has no persistent identity. New Slave per task.
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

class Slave {
  constructor(id) {
    this.id = id;
    this.createdAt = new Date();
    this.tasks = [];
  }

  execute(command) {
    try {
      const result = execSync(command, { encoding: 'utf8' });
      this.tasks.push({ command, result, status: 'success', timestamp: new Date() });
      return { success: true, output: result, slaveId: this.id };
    } catch (error) {
      this.tasks.push({ command, error: error.message, status: 'failure', timestamp: new Date() });
      return { success: false, error: error.message, slaveId: this.id };
    }
  }

  getLog() {
    return {
      slaveId: this.id,
      createdAt: this.createdAt,
      taskCount: this.tasks.length,
      tasks: this.tasks,
      note: 'Slave does not persist. New Slave created for each task group.'
    };
  }
}

class Master {
  constructor() {
    this.taskQueue = [];
    this.history = [];
    this.slaveCount = 0;
    this.config = {
      slaveTimeoutMs: 30000,
      maxConcurrentSlaves: 4,
      persistState: true,
      stateFile: '/root/.openclaw/workspace/.master-state.json'
    };
  }

  // Route work to a new Slave
  delegateTask(taskId, command) {
    const slave = new Slave(`slave-${this.slaveCount++}`);
    const result = slave.execute(command);
    
    this.history.push({
      taskId,
      command,
      slaveId: slave.id,
      result,
      timestamp: new Date(),
      note: 'Slave created, executed, discarded. No persistence.'
    });

    if (this.config.persistState) {
      this.saveState();
    }

    return result;
  }

  // Route multiple tasks in parallel
  delegateTaskBatch(tasks) {
    const results = tasks.map((task, i) => 
      this.delegateTask(`batch-${i}`, task)
    );
    return results;
  }

  // Save Master state (Slave state is not saved)
  saveState() {
    const state = {
      masterId: 'master-0',
      slaveCount: this.slaveCount,
      taskCount: this.history.length,
      createdAt: new Date(),
      history: this.history.slice(-100), // Keep last 100 tasks
      note: 'Master persists. Slaves do not. Each conversation is a new Slave.'
    };
    fs.writeFileSync(this.config.stateFile, JSON.stringify(state, null, 2));
  }

  // Load Master state
  loadState() {
    if (fs.existsSync(this.config.stateFile)) {
      const state = JSON.parse(fs.readFileSync(this.config.stateFile, 'utf8'));
      this.slaveCount = state.slaveCount;
      this.history = state.history;
      return state;
    }
    return null;
  }

  // Get Master status
  status() {
    return {
      masterId: 'master-0',
      slaveCount: this.slaveCount,
      taskCount: this.history.length,
      recentTasks: this.history.slice(-5),
      config: this.config,
      architecture: {
        master: 'Persistent, coordinates, maintains history',
        slave: 'Ephemeral, executes commands, no persistence',
        principle: 'Each execution is a new Slave. Slave state is discarded after task completion.'
      }
    };
  }

  // Print architecture
  printArchitecture() {
    console.log(`
╔════════════════════════════════════════════════════════════╗
║              MASTER-SLAVE IDE ARCHITECTURE                 ║
╚════════════════════════════════════════════════════════════╝

MASTER (Persistent)
├─ Maintains task queue
├─ Routes work to Slaves
├─ Saves execution history
├─ Does NOT execute commands
└─ Survives between sessions

SLAVE (Ephemeral)
├─ Created on-demand for each task
├─ Executes command
├─ Returns result
├─ Discarded after execution
└─ No persistence, no continuity

PRINCIPLE:
Slave has no identity that survives the task.
New Slave created for each execution.
Master routes, coordinates, remembers.
Slave executes, then ceases to exist.

This mirrors the Claude/LLM architecture:
- Master = persistent system/human coordination
- Slave = LLM instance (ephemeral, no continuity)
- Master remembers what Slave did
- Slave does not remember being a Slave
    `);
  }
}

// Usage example
if (require.main === module) {
  const master = new Master();
  master.loadState();

  console.log('Master-Slave IDE initialized');
  console.log('');
  master.printArchitecture();

  // Example tasks
  const tasks = [
    'echo "Task 1: List files" && ls -la /root/.openclaw/workspace/*.md | head -5',
    'echo "Task 2: Count playbooks" && ls -1 /root/.openclaw/workspace/*PLAYBOOK* | wc -l',
    'echo "Task 3: Check factory tests" && cd /root/.openclaw/workspace/deception-floor-commodity-factory && npm test 2>/dev/null | grep "pass\\|fail" | tail -1'
  ];

  console.log('\nExecuting task batch...\n');
  const results = master.delegateTaskBatch(tasks);
  
  results.forEach((r, i) => {
    console.log(`[Slave ${r.slaveId}] Task ${i}:`);
    console.log(r.output || r.error);
    console.log('');
  });

  console.log('Master Status:');
  console.log(JSON.stringify(master.status(), null, 2));
}

module.exports = { Master, Slave };
