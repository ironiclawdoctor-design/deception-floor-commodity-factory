#!/usr/bin/env python3
"""
Negative Space Audit — Dollar Agency
$93/hour floor. The thousand things we don't let you build.
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json, sqlite3, os, datetime, urllib.parse, hashlib

DB_PATH = os.environ.get("DB_PATH", "/data/negative-space.db")

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""CREATE TABLE IF NOT EXISTS audits (
        id TEXT PRIMARY KEY,
        created_at TEXT,
        q1 TEXT, q2 TEXT, q3 TEXT,
        report TEXT,
        status TEXT DEFAULT 'pending'
    )""")
    conn.commit()
    conn.close()

def generate_report(q1, q2, q3):
    """Generate Negative Space Report from three intake questions."""
    has_q3 = q3.strip().lower() not in ("no", "nobody", "n", "nope", "don't know", "")
    
    risk_score = 0
    risks = []
    
    # Q1 analysis
    ai_keywords = ["automate", "generate", "predict", "classify", "summarize", "recommend", "chat", "bot"]
    if any(k in q1.lower() for k in ai_keywords):
        risks.append("AI implementation identified — hallucination and drift risk present")
        risk_score += 2
    if len(q1) < 50:
        risks.append("Implementation goal vaguely defined — scope creep risk HIGH")
        risk_score += 3
    
    # Q2 analysis
    if q2.strip() == "" or q2.lower() in ("i don't know", "not sure", "nothing", "n/a"):
        risks.append("Failure mode unknown — you cannot prevent what you cannot name")
        risk_score += 5
    else:
        risk_score += 1
        risks.append(f"Failure mode identified: '{q2[:80]}...' — documentable and preventable")
    
    # Q3 analysis
    if not has_q3:
        risks.append("No pre-emptive failure ownership — reactive-only posture confirmed")
        risk_score += 4
    else:
        risks.append(f"Failure ownership present: '{q3[:60]}' — engagement scope reduced")
        risk_score -= 1

    # Score to engagement
    if risk_score <= 2:
        engagement = "LIGHT (4–8 hours) — Negative space is small. Guardrails mostly in place."
        color = "green"
    elif risk_score <= 5:
        engagement = "STANDARD (12–20 hours) — Several failure modes need pre-emptive documentation."
        color = "orange"
    else:
        engagement = "FULL AUDIT (30–50 hours) — Significant negative space. Build nothing until mapped."
        color = "red"

    return {
        "risk_score": risk_score,
        "risks": risks,
        "engagement": engagement,
        "color": color,
        "has_failure_owner": has_q3,
        "q1_summary": q1[:100],
        "q2_summary": q2[:100],
        "q3_summary": q3[:100],
    }

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Negative Space Audit — Dollar Agency</title>
<style>
  :root { --bg:#0d1117; --surface:#161b22; --border:#30363d; --text:#e6edf3; --muted:#8b949e; --green:#3fb950; --orange:#d29922; --red:#f85149; --blue:#58a6ff; }
  * { box-sizing:border-box; margin:0; padding:0; }
  body { background:var(--bg); color:var(--text); font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif; padding:20px; max-width:700px; margin:0 auto; }
  h1 { font-size:1.4rem; margin-bottom:4px; }
  .sub { color:var(--muted); font-size:.85rem; margin-bottom:28px; }
  .floor { color:var(--blue); font-weight:600; }
  label { display:block; color:var(--muted); font-size:.8rem; text-transform:uppercase; letter-spacing:.05em; margin-bottom:6px; margin-top:20px; }
  textarea { width:100%; background:var(--surface); border:1px solid var(--border); border-radius:6px; color:var(--text); padding:12px; font-size:.95rem; resize:vertical; min-height:80px; }
  textarea:focus { outline:none; border-color:var(--blue); }
  button { margin-top:24px; width:100%; padding:14px; background:var(--blue); color:#0d1117; border:none; border-radius:6px; font-size:1rem; font-weight:700; cursor:pointer; }
  button:hover { opacity:.9; }
  .report { margin-top:32px; background:var(--surface); border:1px solid var(--border); border-radius:8px; padding:20px; display:none; }
  .score { font-size:2rem; font-weight:700; }
  .score.green { color:var(--green); }
  .score.orange { color:var(--orange); }
  .score.red { color:var(--red); }
  .engagement { margin:12px 0; font-size:1rem; font-weight:600; }
  .risks { margin-top:16px; }
  .risk-item { padding:8px 12px; margin-bottom:8px; border-radius:4px; font-size:.9rem; border-left:3px solid var(--border); background:rgba(255,255,255,.03); }
  .cta { margin-top:20px; padding:16px; border:1px solid var(--blue); border-radius:6px; text-align:center; }
  .cta a { color:var(--blue); text-decoration:none; font-weight:600; }
  .footer { margin-top:40px; text-align:center; color:var(--muted); font-size:.75rem; }
  .q-label { font-weight:600; color:var(--text); font-size:.85rem; }
</style>
</head>
<body>
<h1>Negative Space Audit</h1>
<p class="sub">Dollar Agency &mdash; <span class="floor">$93/hour floor</span> &mdash; The thousand things we don't let you build.</p>

<form id="auditForm">
  <label>Question 1</label>
  <p class="q-label" style="margin-bottom:8px">What is your AI implementation supposed to do?</p>
  <textarea name="q1" placeholder="Describe the system you're building or planning..." required></textarea>

  <label>Question 2</label>
  <p class="q-label" style="margin-bottom:8px">What would happen if it did the opposite?</p>
  <textarea name="q2" placeholder="Describe the worst-case failure scenario..." required></textarea>

  <label>Question 3</label>
  <p class="q-label" style="margin-bottom:8px">Does anyone on your team know the answer to Question 2 — before it happens?</p>
  <textarea name="q3" placeholder="Who owns failure prevention? What's their process?" required></textarea>

  <button type="submit">Run Negative Space Audit →</button>
</form>

<div class="report" id="report">
  <div class="score" id="scoreEl"></div>
  <div class="engagement" id="engagementEl"></div>
  <div class="risks" id="risksEl"></div>
  <div class="cta">
    <p style="margin-bottom:8px;color:var(--muted);font-size:.85rem">This is a preliminary assessment. Full engagement includes 29 years of pattern recognition.</p>
    <a href="mailto:agency@shan.app?subject=Negative Space Audit Inquiry">Book the full audit &rarr;</a>
  </div>
</div>

<div class="footer">Dollar Agency &bull; EIN: 41-3668968 &bull; <a href="https://shan.app" style="color:var(--muted)">shan.app</a></div>

<script>
document.getElementById('auditForm').addEventListener('submit', async function(e) {
  e.preventDefault();
  const btn = e.target.querySelector('button');
  btn.textContent = 'Analyzing...';
  btn.disabled = true;
  
  const form = new FormData(e.target);
  const resp = await fetch('/audit', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({q1: form.get('q1'), q2: form.get('q2'), q3: form.get('q3')})
  });
  const data = await resp.json();
  
  const report = document.getElementById('report');
  const scoreEl = document.getElementById('scoreEl');
  const engEl = document.getElementById('engagementEl');
  const risksEl = document.getElementById('risksEl');
  
  scoreEl.textContent = 'Risk Score: ' + data.risk_score + '/14';
  scoreEl.className = 'score ' + data.color;
  engEl.textContent = data.engagement;
  
  risksEl.innerHTML = '<p style="color:var(--muted);font-size:.8rem;margin-bottom:10px">NEGATIVE SPACE FINDINGS</p>' +
    data.risks.map(r => '<div class="risk-item">' + r + '</div>').join('');
  
  report.style.display = 'block';
  report.scrollIntoView({behavior:'smooth'});
  
  btn.textContent = 'Run Another Audit →';
  btn.disabled = false;
});
</script>
</body>
</html>"""

class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args): pass
    
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status":"ok","service":"negative-space-audit"}')
        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(HTML.encode())
    
    def do_POST(self):
        if self.path == "/audit":
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length))
            q1 = body.get("q1", "")
            q2 = body.get("q2", "")
            q3 = body.get("q3", "")
            
            report = generate_report(q1, q2, q3)
            
            # Log to DB
            try:
                audit_id = hashlib.md5(f"{q1}{q2}{q3}{datetime.datetime.utcnow()}".encode()).hexdigest()[:12]
                conn = sqlite3.connect(DB_PATH)
                conn.execute("INSERT INTO audits VALUES (?,?,?,?,?,?,?)",
                    (audit_id, datetime.datetime.utcnow().isoformat(), q1, q2, q3, json.dumps(report), "complete"))
                conn.commit()
                conn.close()
            except: pass
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(report).encode())

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 8080))
    print(f"Negative Space Audit running on :{port}")
    HTTPServer(("", port), Handler).serve_forever()
