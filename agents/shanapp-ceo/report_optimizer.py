import json
import os
import time
import hashlib

CACHE_DIR = "/root/.openclaw/workspace/agents/shanapp-ceo/reports_cache"
CACHE_INDEX = os.path.join(CACHE_DIR, "index.json")

class ReportCacher:
    def __init__(self):
        if not os.path.exists(CACHE_DIR):
            os.makedirs(CACHE_DIR)
        self.index = self._load_index()

    def _load_index(self):
        if os.path.exists(CACHE_INDEX):
            with open(CACHE_INDEX, "r") as f:
                return json.load(f)
        return {}

    def _save_index(self):
        with open(CACHE_INDEX, "w") as f:
            json.dump(self.index, f, indent=2)

    def cache_report(self, report_text):
        timestamp = time.time()
        report_id = hashlib.md5(report_text.encode()).hexdigest()
        
        # Avoid duplicate "Boring Buzz"
        if report_id in self.index:
            return self.index[report_id]["path"], True

        filename = f"report_{int(timestamp)}_{report_id[:8]}.md"
        path = os.path.join(CACHE_DIR, filename)
        
        with open(path, "w") as f:
            f.write(report_text)
            
        self.index[report_id] = {
            "timestamp": timestamp,
            "path": path,
            "summary_hash": report_id
        }
        self._save_index()
        return path, False

    def get_latest_context(self, limit=5):
        sorted_reports = sorted(self.index.values(), key=lambda x: x["timestamp"], reverse=True)
        return sorted_reports[:limit]

if __name__ == "__main__":
    # Integration hook for Excellence Creep
    import sys
    if len(sys.argv) > 1:
        cacher = ReportCacher()
        path, cached = cacher.cache_report(sys.stdin.read())
        if cached:
            print(f"CACHE_HIT: {path}")
        else:
            print(f"CACHE_NEW: {path}")
