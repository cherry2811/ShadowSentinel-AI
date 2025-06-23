import json
import time
import subprocess
from datetime import datetime
from email_alert import send_email
from process_alerts import process_alert
from threat_memory import ThreatMemory

WAZUH_ALERTS_PATH = "/var/ossec/logs/alerts/alerts.json"
WHITELIST_FILE = "whitelist.txt"
LOG_FILE = "blocked_ips.log"

BLOCKED_IPS = set()
WHITELISTED_IPS = set()

def load_blocked_ips():
    try:
        with open(LOG_FILE, "r") as file:
            for line in file:
                if "Blocked IP:" in line:
                    ip = line.strip().split("Blocked IP:")[1].strip()
                    BLOCKED_IPS.add(ip)
    except FileNotFoundError:
        pass

def load_whitelist():
    try:
        with open(WHITELIST_FILE, "r") as file:
            for line in file:
                WHITELISTED_IPS.add(line.strip())
    except FileNotFoundError:
        pass

def block_ip(ip):
    if ip in WHITELISTED_IPS:
        print(f"✅ Skipped whitelisted IP: {ip}")
        return

    if ip not in BLOCKED_IPS:
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"])
        BLOCKED_IPS.add(ip)
        print(f"🔥 Blocked IP: {ip}")
        with open(LOG_FILE, "a") as log_file:
            log_file.write(f"[{datetime.now()}] Blocked IP: {ip}\n")

        # Send email alert on IP block
        send_email(f"ShadowSentinel Alert:\n\nBlocked brute-force IP: {ip}")

def detect_brute_force(alert):
    # Adjust this based on your alert JSON structure for IP
    srcip = alert.get("srcip") or alert.get("data", {}).get("srcip", "")
    rule = alert.get("rule", {})
    description = rule.get("description", "").lower()

    if ("authentication failure" in description or "sshd" in description) and srcip:
        block_ip(srcip)

def monitor_alerts():
    print("👁️ Monitoring Wazuh alerts in real time...")
    load_blocked_ips()
    load_whitelist()

    threat_memory = ThreatMemory()

    with open(WAZUH_ALERTS_PATH, 'r') as file:
        file.seek(0, 2)  # Move to end of file

        while True:
            line = file.readline()
            if not line:
                time.sleep(0.5)
                continue

            try:
                alert = json.loads(line)
                rule = alert.get("rule", {})
                level = rule.get("level", 0)
                description = rule.get("description", "")

                if level >= 6:
                    print(f"🚨 New Alert: {description}")

                    # Log alert to daily file with timestamp
                    with open("daily_alerts.log", "a") as log_file:
                        log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {description}\n")

                    # Use AI summarization + threat memory process
                    response = process_alert(alert, threat_memory)
                    print("Action:", response)

                    # Also detect and block brute force IPs automatically
                    detect_brute_force(alert)

                    # Send email alert for new alert
                    send_email(f"New ShadowSentinel Alert:\n\n{description}")

            except json.JSONDecodeError:
                continue
            except Exception as e:
                print("ERROR processing alert:", e)

if __name__ == "__main__":
    monitor_alerts()
