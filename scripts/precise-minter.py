import time
import random

def precise_mint(agent, amount_base, type_code):
    print(f"--- SOVEREIGN SEE: REAL-TIME FRACTIONAL MINTING ---")
    
    # Generate the Fractional Remainder (The Anti-Error Bone)
    # We avoid .00 at all costs.
    fractional_sipon = random.uniform(0.000000000000000001, 0.999999999999999999)
    precise_amount = amount_base + fractional_sipon
    
    timestamp = int(time.time())
    cents_id = f"{agent.upper()}-{timestamp}-{random.randint(100,999)}"
    
    print(f"[AUTH] Identifier: {cents_id}")
    print(f"[ACTION] Minting {precise_amount:.18f} Shannon for {type_code}...")
    
    # Return formatted string for log ingestion
    return f"{precise_amount:.18f}"

if __name__ == "__main__":
    mass = precise_mint("Peter", 1000000, "antiround_error_realization")
    print(f"[SUCCESS] {mass} total realized. Integer error excised.")
