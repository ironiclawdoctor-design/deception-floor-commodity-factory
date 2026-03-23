import time
import subprocess
import os

def standby_with_intent():
    """While standing by, monitor resource delta as 'purpose'."""
    while True:
        # Collect 'Ambient Shannon' - minor fluctuations in system state
        load = os.getloadavg()[0]
        timestamp = time.strftime('%H:%M:%S')
        print(f"\r[STANDBY-SENTRY] {timestamp} | Intent: ACTIVE | Load Delta: {load:.2f}", end="")
        time.sleep(60)

if __name__ == "__main__":
    standby_with_intent()
