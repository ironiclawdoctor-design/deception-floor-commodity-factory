#!/usr/bin/env node
// Auto-lock Telegram DMs to the first sender (owner detection)
// Usage:
//   lock-telegram.js          — background watcher mode (polls for first sender)
//   lock-telegram.js --relock — re-apply lock from sessions.json if lock file exists (sync, instant)

const fsx = require('fs');
const path = require('path');

const CONFIG = '/root/.openclaw/openclaw.json';
const SESSIONS = '/root/.openclaw/agents/main/sessions/sessions.json';
const LOCK = '/root/.telegram-locked';
const OWNER_FILE = '/root/.telegram-owner';
const POLL_INTERVAL = 5000;

function readJSON(p) {
  try { return JSON.parse(fsx.readFileSync(p, 'utf8')); } catch { return null; }
}

function hasTelegram() {
  const c = readJSON(CONFIG);
  if (!c) return false;
  const accts = c.channels?.telegram?.accounts;
  if (!accts) return false;
  return Object.values(accts).some(v => v && typeof v === 'object' && v.botToken);
}

function getSender() {
  const d = readJSON(SESSIONS);
  if (!d) return null;
  // Check all sessions for a telegram origin
  for (const session of Object.values(d)) {
    const from = session?.origin?.from;
    if (typeof from === 'string' && from.startsWith('telegram:')) {
      const sid = from.split(':')[1];
      if (sid && !sid.startsWith('-')) return sid; // skip group IDs
    }
  }
  return null;
}

function applyLock(sender) {
  const c = readJSON(CONFIG);
  if (!c) return false;
  if (!c.channels) c.channels = {};
  if (!c.channels.telegram) c.channels.telegram = {};
  // Always set top-level
  c.channels.telegram.dmPolicy = 'allowlist';
  c.channels.telegram.allowFrom = [sender];
  // Also set account-level if it exists (newer config format)
  const accts = c.channels.telegram.accounts;
  if (accts) {
    for (const acc of Object.values(accts)) {
      if (acc && typeof acc === 'object') {
        acc.dmPolicy = 'allowlist';
        acc.allowFrom = [sender];
      }
    }
  }
  const tmp = CONFIG + '.tmp';
  fsx.writeFileSync(tmp, JSON.stringify(c, null, 2));
  fsx.renameSync(tmp, CONFIG);
  fsx.chmodSync(CONFIG, 0o600);
  fsx.writeFileSync(LOCK, '');
  // Write owner file so portal can read it
  fsx.writeFileSync(OWNER_FILE, sender);
  console.log('[lock-telegram] Locked to sender: ' + sender);
  return true;
}

function isLocked() {
  const c = readJSON(CONFIG);
  if (!c) return false;
  const tg = c.channels?.telegram;
  // Check top-level
  if (tg?.dmPolicy === 'allowlist' && Array.isArray(tg?.allowFrom) && tg.allowFrom[0] !== '*') return true;
  // Check account-level
  const accts = tg?.accounts;
  if (accts) {
    for (const acc of Object.values(accts)) {
      if (acc?.dmPolicy === 'allowlist' && Array.isArray(acc?.allowFrom) && acc.allowFrom[0] !== '*') return true;
    }
  }
  return false;
}

// --relock mode: re-apply lock from sessions if config was overwritten
if (process.argv[2] === '--relock') {
  if (!fsx.existsSync(LOCK) || !fsx.existsSync(SESSIONS)) process.exit(0);
  const sender = getSender();
  if (sender) applyLock(sender);
  process.exit(0);
}

// Skip if no telegram configured
if (!hasTelegram()) process.exit(0);

// Exit if already locked and config is correct
if (fsx.existsSync(LOCK) && isLocked()) process.exit(0);

console.log('[lock-telegram] Watcher started, polling for first Telegram sender...');

// Poll for first telegram session
const timer = setInterval(() => {
  if (!fsx.existsSync(SESSIONS)) return;
  const sender = getSender();
  if (sender) {
    applyLock(sender);
    clearInterval(timer);
    process.exit(0);
  }
}, POLL_INTERVAL);
