#!/usr/bin/env node

// src/index.ts
import { createServer } from "http";
import { spawn } from "child_process";
import { appendFile, mkdir } from "fs/promises";
import { join } from "path";
var PORT = Number(process.env.AGENCY_BASH_PORT ?? 8484);
var HOST = process.env.AGENCY_BASH_HOST ?? "127.0.0.1";
var LOG_DIR = process.env.AGENCY_BASH_LOG_DIR ?? join(process.cwd(), "logs");
var MAX_TIMEOUT_MS = 3e4;
var MAX_OUTPUT_BYTES = 512e3;
var DENIED_PATTERNS = [
  /\brm\s+-rf\s+\/(?!\w)/,
  // rm -rf / (root wipe)
  /\bmkfs\b/,
  // format filesystems
  /\bdd\b.*of=\/dev/,
  // raw disk writes
  /\b:(){.*};:/,
  // fork bombs
  /\bcurl\b.*\|\s*(?:ba)?sh/,
  // pipe curl to shell
  /\bwget\b.*\|\s*(?:ba)?sh/,
  // pipe wget to shell
  /\bshutdown\b/,
  // shutdown
  /\breboot\b/,
  // reboot
  /\binit\s+0\b/,
  // halt
  /\bsystemctl\s+(?:halt|poweroff)\b/
];
async function auditLog(entry) {
  await mkdir(LOG_DIR, { recursive: true });
  const date = (/* @__PURE__ */ new Date()).toISOString().slice(0, 10);
  const path = join(LOG_DIR, `agency-bash-${date}.jsonl`);
  await appendFile(path, JSON.stringify(entry) + "\n");
}
function execCommand(command, timeoutMs, cwd) {
  return new Promise((resolve) => {
    const start = Date.now();
    let stdout = "";
    let stderr = "";
    let stdoutBytes = 0;
    let stderrBytes = 0;
    let killed = false;
    const child = spawn("bash", ["-c", command], {
      cwd: cwd ?? process.env.HOME ?? "/root",
      timeout: timeoutMs,
      env: {
        ...process.env,
        // Restrict PATH to safe locations
        PATH: "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
      }
    });
    child.stdout.on("data", (chunk) => {
      stdoutBytes += chunk.length;
      if (stdoutBytes <= MAX_OUTPUT_BYTES) {
        stdout += chunk.toString();
      }
    });
    child.stderr.on("data", (chunk) => {
      stderrBytes += chunk.length;
      if (stderrBytes <= MAX_OUTPUT_BYTES) {
        stderr += chunk.toString();
      }
    });
    const timer = setTimeout(() => {
      killed = true;
      child.kill("SIGKILL");
    }, timeoutMs);
    child.on("close", (code) => {
      clearTimeout(timer);
      const durationMs = Date.now() - start;
      const truncated = stdoutBytes > MAX_OUTPUT_BYTES || stderrBytes > MAX_OUTPUT_BYTES;
      if (killed) {
        stderr += `
[agency-bash] Process killed after ${timeoutMs}ms timeout`;
      }
      resolve({
        stdout: stdout.slice(0, MAX_OUTPUT_BYTES),
        stderr: stderr.slice(0, MAX_OUTPUT_BYTES),
        exitCode: code,
        durationMs,
        truncated
      });
    });
    child.on("error", (err) => {
      clearTimeout(timer);
      resolve({
        stdout: "",
        stderr: err.message,
        exitCode: -1,
        durationMs: Date.now() - start,
        truncated: false
      });
    });
  });
}
async function readBody(req) {
  const chunks = [];
  let size = 0;
  const MAX_BODY = 64e3;
  for await (const chunk of req) {
    size += chunk.length;
    if (size > MAX_BODY) throw new Error("Body too large");
    chunks.push(chunk);
  }
  return Buffer.concat(chunks).toString();
}
function json(res, status, data) {
  const body = JSON.stringify(data);
  res.writeHead(status, {
    "Content-Type": "application/json",
    "Content-Length": Buffer.byteLength(body)
  });
  res.end(body);
}
async function handleExec(req, res) {
  if (req.method !== "POST") {
    return json(res, 405, { error: "Method not allowed" });
  }
  let body;
  try {
    body = JSON.parse(await readBody(req));
  } catch {
    return json(res, 400, { error: "Invalid JSON" });
  }
  const command = body.command?.trim();
  const agent = body.agent ?? "unknown";
  const timeoutMs = Math.min(body.timeout ?? 1e4, MAX_TIMEOUT_MS);
  const cwd = body.cwd;
  if (!command) {
    return json(res, 400, { error: "Missing 'command' field" });
  }
  for (const pattern of DENIED_PATTERNS) {
    if (pattern.test(command)) {
      const entry2 = {
        ts: (/* @__PURE__ */ new Date()).toISOString(),
        agent,
        command,
        exitCode: null,
        durationMs: 0,
        denied: true,
        error: `Denied: matched pattern ${pattern.source}`,
        stdoutBytes: 0,
        stderrBytes: 0
      };
      await auditLog(entry2);
      return json(res, 403, {
        error: "Command denied by security policy",
        pattern: pattern.source
      });
    }
  }
  const result = await execCommand(command, timeoutMs, cwd);
  const entry = {
    ts: (/* @__PURE__ */ new Date()).toISOString(),
    agent,
    command,
    exitCode: result.exitCode,
    durationMs: result.durationMs,
    stdoutBytes: Buffer.byteLength(result.stdout),
    stderrBytes: Buffer.byteLength(result.stderr)
  };
  await auditLog(entry);
  return json(res, 200, {
    ok: result.exitCode === 0,
    exitCode: result.exitCode,
    stdout: result.stdout,
    stderr: result.stderr,
    durationMs: result.durationMs,
    truncated: result.truncated
  });
}
function handleHealth(_req, res) {
  return json(res, 200, {
    status: "ok",
    service: "agency-bash",
    version: "0.1.0",
    uptime: process.uptime(),
    tier: 0,
    cost: "$0.00"
  });
}
async function handleStats(_req, res) {
  const date = (/* @__PURE__ */ new Date()).toISOString().slice(0, 10);
  const logPath = join(LOG_DIR, `agency-bash-${date}.jsonl`);
  let totalCommands = 0;
  let deniedCommands = 0;
  let totalDurationMs = 0;
  const agentCounts = {};
  try {
    const { readFile } = await import("fs/promises");
    const content = await readFile(logPath, "utf-8");
    const lines = content.trim().split("\n").filter(Boolean);
    for (const line of lines) {
      try {
        const entry = JSON.parse(line);
        totalCommands++;
        if (entry.denied) deniedCommands++;
        totalDurationMs += entry.durationMs;
        agentCounts[entry.agent] = (agentCounts[entry.agent] ?? 0) + 1;
      } catch {
      }
    }
  } catch {
  }
  return json(res, 200, {
    date,
    totalCommands,
    deniedCommands,
    totalDurationMs,
    avgDurationMs: totalCommands > 0 ? Math.round(totalDurationMs / totalCommands) : 0,
    agentCounts,
    tier: 0,
    cost: "$0.00"
  });
}
var server = createServer(async (req, res) => {
  const url = new URL(req.url ?? "/", `http://${HOST}:${PORT}`);
  try {
    switch (url.pathname) {
      case "/exec":
        return await handleExec(req, res);
      case "/health":
        return handleHealth(req, res);
      case "/stats":
        return await handleStats(req, res);
      default:
        return json(res, 404, { error: "Not found. Endpoints: /exec, /health, /stats" });
    }
  } catch (err) {
    console.error("[agency-bash] Unhandled error:", err);
    return json(res, 500, { error: "Internal server error" });
  }
});
server.listen(PORT, HOST, () => {
  console.log(`[agency-bash] Tier 0 execution server listening on ${HOST}:${PORT}`);
  console.log(`[agency-bash] Endpoints: POST /exec, GET /health, GET /stats`);
  console.log(`[agency-bash] Logs: ${LOG_DIR}`);
  console.log(`[agency-bash] Cost: $0.00 (always)`);
});
var shutdown = () => {
  console.log("\n[agency-bash] Shutting down...");
  server.close();
  process.exit(0);
};
process.on("SIGINT", shutdown);
process.on("SIGTERM", shutdown);
//# sourceMappingURL=index.js.map