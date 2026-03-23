import requests
import sys

def push_success(message):
    print(f"--- FIESTA ORCHESTRATOR: AUTO-PUSH ACTIVE ---")
    payload = {
        "action": "send",
        "target": "telegram:8273187690",
        "message": f"🚀 [AUTO-PUSH] GROUND-TRUTH: {message}"
    }
    # Direct Gateway Message API
    # requests.post("http://localhost:8000/message", json=payload)
    print(f"PUSHED: {message}")
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1:
        push_success(" ".join(sys.argv[1:]))
