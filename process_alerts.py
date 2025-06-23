import json
import subprocess
from threat_memory import ThreatMemory

print("DEBUG: Script started running")

WHITELISTED_IPS = ["192.168.1.100"]  # Add IPs here that should NEVER be blocked

def generate_ai_summary(alert_json):
    import json
    import subprocess

    print("DEBUG: generate_ai_summary function called")

    alert_text = json.dumps(alert_json, indent=2)
    prompt = f"You are a cybersecurity analyst AI. Summarize the following Wazuh alert:\n\n{alert_text}"
    print(f"DEBUG: Prompt:\n{prompt}")

    try:
        result = subprocess.run(
            ["ollama", "run", "mistral"],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=30
        )
    except Exception as e:
        print("ERROR: Exception running ollama:", e)
        return "Error generating summary due to exception."

    print("DEBUG: Ollama return code:", result.returncode)
    print("DEBUG: Ollama stdout:", repr(result.stdout))
    print("DEBUG: Ollama stderr:", repr(result.stderr))

    if result.returncode == 0 and result.stdout.strip():
        return result.stdout.strip()
    else:
        return f"Error generating summary. Ollama stderr: {result.stderr.strip()}"

def extract_ip(alert_json):
    return alert_json.get('srcip', 'unknown')

def block_ip(ip):
    if ip in WHITELISTED_IPS:
        print(f"✅ Skipped blocking whitelisted IP: {ip}")
        return False
    try:
        subprocess.run(
            ["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"],
            check=True
        )
        print(f"🚫 Blocked IP {ip} using iptables")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to block IP {ip}: {e}")
        return False

def process_alert(alert_json, threat_memory):
    print("DEBUG: Calling generate_ai_summary...")
    summary = generate_ai_summary(alert_json)
    print(f"AI Summary: {summary}")

    ip = extract_ip(alert_json)
    print(f"Extracted IP: {ip}")

    similar = threat_memory.find_similar(summary)
    if similar:
        response = f"This alert looks similar to an earlier alert from {similar['ip']}. Already handled."
    else:
        threat_memory.add_alert(summary, ip)
        blocked = block_ip(ip)  # Block IP in Step 3
        response = f"New alert processed and stored for IP {ip}."
        if blocked:
            response += " IP blocked."
        else:
            response += " Failed to block IP."

    print("DEBUG: process_alert completed.")
    return response

if __name__ == "__main__":
    print("DEBUG: Starting main execution")

    with open("test_alerts.json", "r") as f:
        alert_json = json.load(f)

    threat_memory = ThreatMemory()

    print("DEBUG: Calling process_alert")
    result = process_alert(alert_json, threat_memory)
    print("Result from process_alert:", result)
