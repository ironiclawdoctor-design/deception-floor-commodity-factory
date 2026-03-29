import sqlite3

db1 = '/root/.openclaw/workspace/dollar/dollar.db'
db2 = '/root/.openclaw/workspace/entropy_ledger.db'

print("=== CMD1 ===")
con = sqlite3.connect(db1)
cur = con.cursor()
c1 = cur.execute("SELECT COUNT(*) FROM transactions WHERE status='cleared'").fetchone()[0]
c2 = cur.execute("SELECT COUNT(*) FROM shannon_events").fetchone()[0]
c3 = cur.execute("SELECT COUNT(*) FROM deception_floor_log").fetchone()[0]
con.close()

con2 = sqlite3.connect(db2)
cur2 = con2.cursor()
c4 = cur2.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]
con2.close()

print(c1)
print(c2)
print(c3)
print(c4)

print("=== CMD2 ===")
con = sqlite3.connect(db1)
cur = con.cursor()
rows = cur.execute("SELECT id, date, description, amount, source, reference FROM transactions WHERE status='cleared' ORDER BY date").fetchall()
for r in rows:
    print("|".join(str(x) for x in r))
con.close()

print("=== CMD3 ===")
con = sqlite3.connect(db1)
cur = con.cursor()
rows = cur.execute("SELECT id, date, event_type, amount_usd, shannon_minted, description FROM shannon_events ORDER BY id").fetchall()
for r in rows:
    print("|".join(str(x) for x in r))
con.close()

print("=== CMD4 ===")
con = sqlite3.connect(db1)
cur = con.cursor()
rows = cur.execute("SELECT id, timestamp, source, event_type, amount_usd, tx_ref FROM deception_floor_log ORDER BY id").fetchall()
for r in rows:
    print("|".join(str(x) for x in r))
con.close()
