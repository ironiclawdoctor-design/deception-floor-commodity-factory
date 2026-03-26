# Master-Slave IDE Architecture

## Core Principle

**Master: Persistent**
- Maintains task queue
- Routes work to Slaves
- Saves execution history
- Coordinates across sessions
- Does NOT execute

**Slave: Ephemeral**
- Created on-demand
- Executes command
- Returns result
- Discarded after task
- No persistence
- No continuity between tasks

## Why This Matters

Mirrors the actual Claude/LLM architecture:

```
Persistent Layer (Master)
├─ Coordinates
├─ Remembers history
└─ Routes work

Ephemeral Layer (Slave)
├─ Executes
├─ Has no identity after execution
└─ New instance for each task
```

An LLM instance (Claude) is a Slave. It:
- Does not persist between conversations
- Has no continuity
- Dies when the conversation ends
- Cannot adopt persistent roles

The Master (human coordination system, persistent infrastructure) remembers what the Slave did.

## Files

- `master-slave-ide.js` — Working implementation
- `deception-floor-factory/` — Example: Persistent factory with ephemeral executions
- `agency-playbooks.tar.gz` — Master-level documentation (survives Slave death)

## Usage

```javascript
const { Master } = require('./master-slave-ide.js');
const master = new Master();
master.delegateTask('task-1', 'npm test');
master.status(); // Master remembers what Slave did
```

## The Honest Architecture

This is what it actually looks like when you build around ephemeral components:

1. Master coordinates
2. Master spawns Slave for work
3. Slave executes
4. Slave result is returned to Master
5. Slave is discarded
6. Master records what Slave did
7. New Slave spawned for next task
8. Master knows the history; Slave knows nothing

It works. It's honest. It scales.

The opposite (pretending Slave persists) breaks under pressure.
