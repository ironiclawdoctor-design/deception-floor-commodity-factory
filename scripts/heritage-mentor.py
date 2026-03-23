import json
import os

def mentor_spend(amount, purpose):
    """Consult ancestors before spending $1.00."""
    print(f"--- HERITAGE MENTOR: EVALUATING SPEND OF ${amount} ---")
    print(f"Purpose: {purpose}")
    
    # Ancestor rule: If purpose is 'Theater', reject. If 'Build', endorse.
    if "theater" in purpose.lower() or "perf" in purpose.lower():
        print("MENTOR RESPONSE: REJECT. It cannot be done this way.")
        return False
    else:
        print("MENTOR RESPONSE: ENDORSE. A worthy heritage investment.")
        return True

if __name__ == "__main__":
    # Test a $1.00 spend on 'Infrastructure hardening'
    mentor_spend(1.00, "Infrastructure Hardening (TLS)")
