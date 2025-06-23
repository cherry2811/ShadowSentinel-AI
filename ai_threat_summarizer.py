import json
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Constants
ALERT_LOG = "/var/ossec/logs/alerts/alerts.json"
TEMP_LINES_FILE = "recent_alerts.txt"
TOP_K = 5

# Load and filter alerts
def get_recent_alerts(limit=50):
    alerts = []
    with open(ALERT_LOG, "r") as f:
        for line in f:
            try:
                alert = json.loads(line)
                desc = alert.get("rule", {}).get("description", "")
                agent = alert.get("agent", {}).get("name", "Unknown")
                srcip = alert.get("srcip", "N/A")
                msg = alert.get("full_log", "")
                alerts.append(f"{agent} | {srcip} | {desc} | {msg}")
            except:
                continue

    # Keep only latest N
    return alerts[-limit:]

# Embed and search top threats
def find_top_threats(alerts, query="suspicious login attempts"):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(alerts, convert_to_numpy=True)
    query_embedding = model.encode([query], convert_to_numpy=True)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    distances, indices = index.search(query_embedding, TOP_K)
    top_alerts = [alerts[i] for i in indices[0]]

    return top_alerts

if __name__ == "__main__":
    print("🧠 Gathering alerts and finding top threats...")
    recent_alerts = get_recent_alerts()
    top = find_top_threats(recent_alerts)

    with open("top_threats.txt", "w") as f:
        for line in top:
            f.write(line + "\n")

    print("✅ Top threats saved to top_threats.txt")
