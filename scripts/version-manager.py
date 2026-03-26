import sqlite3
from datetime import datetime

DB_PATH = "/root/.openclaw/workspace/projects/entropy-economy/entropy_ledger.db"

def update_version(skill_name, version, notes=""):
    print(f"--- SOVEREIGN SEE: VERSION UPDATE ({skill_name}) ---")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS agency_versions 
                 (skill_name TEXT PRIMARY KEY, 
                  version_number TEXT, 
                  last_updated TIMESTAMP,
                  notes TEXT)''')
    
    c.execute("INSERT OR REPLACE INTO agency_versions VALUES (?, ?, ?, ?)",
              (skill_name, version, datetime.now(), notes))
    
    conn.commit()
    conn.close()
    print(f"[SUCCESS] {skill_name} locked at v{version} in the Rock.")
    return True

if __name__ == "__main__":
    # Initializing versions for the idiots console
    update_version("Agency-Core", "231.0.0", "Phase 231M Mass Realization")
    update_version("Autograph-Skill", "3.0.0", "Optimized via Autoresearch")
    update_version("Shadow-Poster", "2.0.0", "Post-Stealth Active")
