import json

INPUT_LOG = "/var/ossec/logs/alerts/alerts.json"  # Change if your path differs
OUTPUT_TEXT = "wazuh_alerts.txt"

def parse_alerts():
    with open(INPUT_LOG, "r") as infile, open(OUTPUT_TEXT, "w") as outfile:
        for line in infile:
            try:
                alert = json.loads(line)
                timestamp = alert.get("timestamp", "N/A")
                rule = alert.get("rule", {})
                description = rule.get("description", "No description")
                agent = alert.get("agent", {}).get("name", "Unknown agent")
                src_ip = alert.get("srcip", "N/A")
                full_msg = alert.get("full_log", "No full log")

                text_line = f"{timestamp} | {agent} | {src_ip} | {description} | {full_msg}\n"
                outfile.write(text_line)

            except json.JSONDecodeError:
                continue

if __name__ == "__main__":
    parse_alerts()
    print(f"✅ Wazuh alerts parsed into {OUTPUT_TEXT}")
