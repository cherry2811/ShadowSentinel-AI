from email_alert import send_email
import subprocess
import json
import time
from datetime import datetime

ALERTS_FILE = "/var/ossec/logs/alerts/alerts.json"
LOG_FILE = "blocked_ips.log"
WHITELIST_FILE = "whitelist.txt"

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

def monitor_alerts():
    print("👁️ Watching Wazuh alerts in real-time...")
    with open(ALERTS_FILE, "r") as file:
        file.seek(0, 2)  # Go to the end of file
        while True:
            line = file.readline()
            if not line:
                time.sleep(0.5)
                continue
            try:
                alert = json.loads(line)
                rule = alert.get("rule", {})
                description = rule.get("description", "").lower()
                srcip = alert.get("data", {}).get("srcip", "")
                if "authentication failure" in description or "sshd" in description:
                    if srcip:
                        block_ip(srcip)
            except json.JSONDecodeError:
                continue

if __name__ == "__main__":
    load_blocked_ips()
    load_whitelist()
    monitor_alerts()
