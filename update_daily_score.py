import json
import datetime

WAZUH_ALERTS_PATH = "/var/ossec/logs/alerts/alerts.json"
SCORE_FILE = "daily_scores.json"
TODAY = str(datetime.date.today())
HIGH_SEVERITY_THRESHOLD = 7

def count_today_alerts():
    count = 0
    try:
        with open(WAZUH_ALERTS_PATH, "r") as file:
            for line in file:
                try:
                    alert = json.loads(line)
                    if "rule" in alert and alert["rule"].get("level", 0) >= HIGH_SEVERITY_THRESHOLD:
                        if TODAY in alert.get("timestamp", ""):
                            count += 1
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        print("⚠️ alerts.json not found.")
    return count

def update_score_file(score):
    try:
        with open(SCORE_FILE, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    data[TODAY] = score

    with open(SCORE_FILE, "w") as f:
        json.dump(data, f, indent=4)

    print(f"✅ Threat score for {TODAY} updated as {score}")

if __name__ == "__main__":
    score = count_today_alerts()
    update_score_file(score)
