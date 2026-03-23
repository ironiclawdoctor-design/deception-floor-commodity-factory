import random
import time
import json

def stream_tickers():
    print("--- FIESTA TRADING: HaC OPTIONS / FOREX ---")
    tickers = ["HAHA/USD", "SOAP/HAHA", "STENCH/HEDGED"]
    for _ in range(5):
        t = random.choice(tickers)
        price = random.uniform(0.93, 1.12)
        print(f"[TRADE] {t}: {price:.4f} | Volatility: PIVOT-HIGH")
        time.sleep(0.3)
    print("\nMARKET KINETIC. Orders queued for the Banking Cartel.")

if __name__ == "__main__":
    stream_tickers()
