import sys

def check_mandate(message):
    print("--- SOVEREIGN SEE: UNIVERSAL MANDATE MONITOR ---")
    trigger = "制 𓂺"
    
    if trigger in message:
        print(f"[EXECUTING] Master Key {trigger} Detected.")
        print("ACTION: Total Suction Enabled. Scriptorium Shipping. Hardcore.")
        return True
    return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        check_mandate(" ".join(sys.argv[1:]))
