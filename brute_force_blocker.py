from email_alert import send_email
import json
import subprocess
from datetime import datetime

# File paths
ALERTS_FILE = "test_alerts.json"
LOG_FILE = "blocked_ips.log"
WHITELIST_FILE = "whitelist.txt"
MEMORY_FILE = "threat_memory.json"

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

def load_threat_memory():
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ Could not load threat memory: {e}")
        return {}

def save_threat_memory(memory):
    try:
        with open(MEMORY_FILE, "w") as f:
            json.dump(memory, f, indent=4)
    except Exception as e:
        print(f"⚠️ Could not save threat memory: {e}")

def block_ip(ip):
    if ip in WHITELISTED_IPS:
        print(f"✅ Skipped whitelisted IP: {ip}")
        return

    memory = load_threat_memory()

    if ip in memory:
        memory[ip]["attempts"] += 1
        memory[ip]["last_seen"] = str(datetime.now())
        print(f"⚠️ Repeat attacker: {ip} — Attempts: {memory[ip]['attempts']}")
    else:
        memory[ip] = {
            "attempts": 1,
            "first_seen": str(datetime.now()),
            "last_seen": str(datetime.now())
        }
        print(f"🆕 New attacker detected: {ip}")

    save_threat_memory(memory)

    if memory[ip]["attempts"] >= 2 and ip not in BLOCKED_IPS:
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"])
        BLOCKED_IPS.add(ip)
        print(f"🔥 Blocked IP: {ip}")
        with open(LOG_FILE, "a") as log_file:
            log_file.write(f"[{datetime.now()}] Blocked IP: {ip}\n")
        send_email("ShadowSentinel Alert 🚨", f"Blocked brute-force IP: {ip}")
    else:
        print(f"🚫 Not blocking yet — IP {ip} has {memory[ip]['attempts']} attempt(s)")

def detect_brute_force(alert_line):
    try:
        data = json.loads(alert_line)
        rule = data.get("rule", {})
        description = rule.get("description", "").lower()

        srcip = data.get("srcip") or data.get("data", {}).get("srcip", "")

        if ("authentication failure" in description or "sshd" in description or "failed ssh" in description) and srcip:
            block_ip(srcip)
    except json.JSONDecodeError:
        pass

def main():
    print("🔍 Scanning for brute-force attempts...")
    load_blocked_ips()
    load_whitelist()
    with open(ALERTS_FILE, "r") as file:
        for line in file:
            detect_brute_force(line)

if __name__ == "__main__":
    main()
