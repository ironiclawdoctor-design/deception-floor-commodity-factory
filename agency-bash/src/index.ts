import { createServer, type IncomingMessage, type ServerResponse } from "node:http";
import { spawn } from "node:child_process";
import { appendFile, mkdir } from "node:fs/promises";
import { join } from "node:path";

// ── Config ──────────────────────────────────────────────────────────
const PORT = Number(process.env.AGENCY_BASH_PORT ?? 8484);
const HOST = process.env.AGENCY_BASH_HOST ?? "127.0.0.1";
const LOG_DIR = process.env.AGENCY_BASH_LOG_DIR ?? join(process.cwd(), "logs");
const MAX_TIMEOUT_MS = 30_000;
const MAX_OUTPUT_BYTES = 512_000; // 500KB per stream

// ── Security: command denylist (patterns that should never run) ─────
const DENIED_PATTERNS: RegExp[] = [
  /\brm\s+-rf\s+\/(?!\w)/,     // rm -rf / (root wipe)
  /\bmkfs\b/,                   // format filesystems
  /\bdd\b.*of=\/dev/,           // raw disk writes
  /\b:(){.*};:/,                // fork bombs
  /\bcurl\b.*\|\s*(?:ba)?sh/,  // pipe curl to shell
  /\bwget\b.*\|\s*(?:ba)?sh/,  // pipe wget to shell
  /\bshutdown\b/,               // shutdown
  /\breboot\b/,                 // reboot
  /\binit\s+0\b/,               // halt
  /\bsystemctl\s+(?:halt|poweroff)\b/,
];

// ── Audit logger ────────────────────────────────────────────────────
interface AuditEntry {
  ts: string;
  agent: string;
  command: string;
  exitCode: number | null;
  durationMs: number;
  denied?: boolean;
  error?: string;
  stdoutBytes: number;
  stderrBytes: number;
}

async function auditLog(entry: AuditEntry): Promise<void> {
  await mkdir(LOG_DIR, { recursive: true });
  const date = new Date().toISOString().slice(0, 10);
  const path = join(LOG_DIR, `agency-bash-${date}.jsonl`);
  await appendFile(path, JSON.stringify(entry) + "\n");
}

// ── Command execution ───────────────────────────────────────────────
interface ExecResult {
  stdout: string;
  stderr: string;
  exitCode: number | null;
  durationMs: number;
  truncated: boolean;
}

function execCommand(
  command: string,
  timeoutMs: number,
  cwd?: string
): Promise<ExecResult> {
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
        PATH: "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
      },
    });

    child.stdout.on("data", (chunk: Buffer) => {
      stdoutBytes += chunk.length;
      if (stdoutBytes <= MAX_OUTPUT_BYTES) {
        stdout += chunk.toString();
      }
    });

    child.stderr.on("data", (chunk: Buffer) => {
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
      const truncated =
        stdoutBytes > MAX_OUTPUT_BYTES || stderrBytes > MAX_OUTPUT_BYTES;

      if (killed) {
        stderr += `\n[agency-bash] Process killed after ${timeoutMs}ms timeout`;
      }

      resolve({
        stdout: stdout.slice(0, MAX_OUTPUT_BYTES),
        stderr: stderr.slice(0, MAX_OUTPUT_BYTES),
        exitCode: code,
        durationMs,
        truncated,
      });
    });

    child.on("error", (err) => {
      clearTimeout(timer);
      resolve({
        stdout: "",
        stderr: err.message,
        exitCode: -1,
        durationMs: Date.now() - start,
        truncated: false,
      });
    });
  });
}

// ── HTTP helpers ────────────────────────────────────────────────────
async function readBody(req: IncomingMessage): Promise<string> {
  const chunks: Buffer[] = [];
  let size = 0;
  const MAX_BODY = 64_000;
  for await (const chunk of req) {
    size += (chunk as Buffer).length;
    if (size > MAX_BODY) throw new Error("Body too large");
    chunks.push(chunk as Buffer);
  }
  return Buffer.concat(chunks).toString();
}

function json(res: ServerResponse, status: number, data: unknown): void {
  const body = JSON.stringify(data);
  res.writeHead(status, {
    "Content-Type": "application/json",
    "Content-Length": Buffer.byteLength(body),
  });
  res.end(body);
}

// ── Routes ──────────────────────────────────────────────────────────
async function handleExec(req: IncomingMessage, res: ServerResponse) {
  if (req.method !== "POST") {
    return json(res, 405, { error: "Method not allowed" });
  }

  let body: { command?: string; agent?: string; timeout?: number; cwd?: string };
  try {
    body = JSON.parse(await readBody(req));
  } catch {
    return json(res, 400, { error: "Invalid JSON" });
  }

  const command = body.command?.trim();
  const agent = body.agent ?? "unknown";
  const timeoutMs = Math.min(body.timeout ?? 10_000, MAX_TIMEOUT_MS);
  const cwd = body.cwd;

  if (!command) {
    return json(res, 400, { error: "Missing 'command' field" });
  }

  // Security check
  for (const pattern of DENIED_PATTERNS) {
    if (pattern.test(command)) {
      const entry: AuditEntry = {
        ts: new Date().toISOString(),
        agent,
        command,
        exitCode: null,
        durationMs: 0,
        denied: true,
        error: `Denied: matched pattern ${pattern.source}`,
        stdoutBytes: 0,
        stderrBytes: 0,
      };
      await auditLog(entry);
      return json(res, 403, {
        error: "Command denied by security policy",
        pattern: pattern.source,
      });
    }
  }

  // Execute
  const result = await execCommand(command, timeoutMs, cwd);

  // Audit
  const entry: AuditEntry = {
    ts: new Date().toISOString(),
    agent,
    command,
    exitCode: result.exitCode,
    durationMs: result.durationMs,
    stdoutBytes: Buffer.byteLength(result.stdout),
    stderrBytes: Buffer.byteLength(result.stderr),
  };
  await auditLog(entry);

  return json(res, 200, {
    ok: result.exitCode === 0,
    exitCode: result.exitCode,
    stdout: result.stdout,
    stderr: result.stderr,
    durationMs: result.durationMs,
    truncated: result.truncated,
  });
}

function handleHealth(_req: IncomingMessage, res: ServerResponse) {
  return json(res, 200, {
    status: "ok",
    service: "agency-bash",
    version: "0.1.0",
    uptime: process.uptime(),
    tier: 0,
    cost: "$0.00",
  });
}

async function handleStats(_req: IncomingMessage, res: ServerResponse) {
  // Quick stats from today's log
  const date = new Date().toISOString().slice(0, 10);
  const logPath = join(LOG_DIR, `agency-bash-${date}.jsonl`);
  let totalCommands = 0;
  let deniedCommands = 0;
  let totalDurationMs = 0;
  const agentCounts: Record<string, number> = {};

  try {
    const { readFile } = await import("node:fs/promises");
    const content = await readFile(logPath, "utf-8");
    const lines = content.trim().split("\n").filter(Boolean);
    for (const line of lines) {
      try {
        const entry: AuditEntry = JSON.parse(line);
        totalCommands++;
        if (entry.denied) deniedCommands++;
        totalDurationMs += entry.durationMs;
        agentCounts[entry.agent] = (agentCounts[entry.agent] ?? 0) + 1;
      } catch {
        // skip malformed lines
      }
    }
  } catch {
    // no log file yet
  }

  return json(res, 200, {
    date,
    totalCommands,
    deniedCommands,
    totalDurationMs,
    avgDurationMs: totalCommands > 0 ? Math.round(totalDurationMs / totalCommands) : 0,
    agentCounts,
    tier: 0,
    cost: "$0.00",
  });
}

// ── Server ──────────────────────────────────────────────────────────
const server = createServer(async (req, res) => {
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

// Graceful shutdown
const shutdown = () => {
  console.log("\n[agency-bash] Shutting down...");
  server.close();
  process.exit(0);
};
process.on("SIGINT", shutdown);
process.on("SIGTERM", shutdown);
