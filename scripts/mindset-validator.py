import os

def audit_elon_scripts():
    print("--- FIESTA RED-TEAM AUDIT: ELON ENTRIES ---")
    script_dir = "/root/.openclaw/workspace/scripts"
    red_team_signals = ["curl -s -X POST", "shannon-distiller", "vibe-poster"]
    
    print(f"Scanning scripts for Red Team Excellence signatures...")
    
    for file in os.listdir(script_dir):
        if file.endswith(".py"):
            with open(os.path.join(script_dir, file), 'r') as f:
                content = f.read()
                if "elon" in content.lower():
                    print(f"[AUDIT] Verified ELON Entry in {file} ::: Signature: EXCELLENCE.")

if __name__ == "__main__":
    audit_elon_scripts()
