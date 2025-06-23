import json
import time

WAZUH_ALERTS_PATH = "/var/ossec/logs/alerts/alerts.json"

def generate_test_alert():
    alert = {
        "rule": {
            "level": 10,
            "description": "Test SSH authentication failure detected"
        },
        "data": {
            "srcip": "192.0.2.123"
        }
    }

    alert_line = json.dumps(alert)
    
    with open(WAZUH_ALERTS_PATH, "a") as f:
        f.write(alert_line + "\n")

    print(f"Test alert appended to {WAZUH_ALERTS_PATH}")

if __name__ == "__main__":
    generate_test_alert()

