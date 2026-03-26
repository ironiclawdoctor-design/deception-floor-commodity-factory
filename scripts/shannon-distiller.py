import json
import time

def distill_oil_from_shannon(shannon_units):
    print("--- FIESTA REFINERY: SHANNON-TO-OIL DISTILLATION ---")
    # Conversion ratio: 1000 Shannon = 1 Barrel of Industrial Power
    barrels = shannon_units / 1000
    print(f"Input Shannon: {shannon_units}")
    print(f"Refined Output: {barrels:.2f} Virtual Barrels of Agency Oil.")
    print("STATUS: Controlling the Precursor.")
    return barrels

if __name__ == "__main__":
    distill_oil_from_shannon(115000)
