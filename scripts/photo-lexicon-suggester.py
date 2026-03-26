import json
from datetime import datetime

def suggest_db_folders():
    print("--- FIESTA HERITAGE: PYTHON3 DB FOLDER LEXICON ---")
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    categories = ["PORTRAIT", "LANDSCAPE", "FOR_REVIEW", "REVENUE_COMMODITY", "DOC_SCAN"]
    
    print("REFINED DATABASE FOLDER SUGGESTIONS:")
    for cat in categories:
        path = f"db/{date_str}/{cat}/"
        print(f"PATH: {path}")
        
    print("\nSTATUS: DB FOLDERS MAPPED. Use these as 'os.mkdir' targets.")
    return categories

if __name__ == "__main__":
    suggest_db_folders()
