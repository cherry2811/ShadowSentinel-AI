import json
import subprocess
from threat_memory import ThreatMemory

print("DEBUG: Script started running")

def generate_ai_summary(alert_json):
    print("DEBUG: generate_ai_summary function called")
    alert_text = json.dumps(alert_json, indent=2)
    prompt = f"""You are a cybersecurity analyst AI. Summarize the following Wazuh alert:

{alert_text}
"""

    print(f"DEBUG: Running ollama with prompt:\n{prompt}\n")

    shell_command = f'ollama run mistral "{prompt}"'

    result = subprocess.run(
        shell_command,
        shell=True,
        capture_output=True,
        text=True
    )

    print(f"DEBUG: Ollama return code: {result.returncode}")
    print(f"DEBUG: Ollama stdout:\n{result.stdout}")
    print(f"DEBUG: Ollama stderr:\n{result.stderr}")

    if result.returncode == 0 and result.stdout.strip():
        return result.stdout.strip()
    else:
        return "Error generating summary"

def extract_ip(alert_json):
    return alert_json.get('srcip', 'unknown')

def process_alert(alert_json, threat_memory):
    summary = generate_ai_summary(alert_json)
    ip = extract_ip(alert_json)

    print(f"AI Summary: {summary}")

    similar = threat_memory.find_similar(summary)
    if similar:
        response = f"This alert looks similar to an earlier alert from {similar['ip']}. Already handled."
    else:
        threat_memory.add_alert(summary, ip)
        response = f"New alert processed and stored for IP {ip}."

    return response

if __name__ == "__main__":
    with open("test_alerts.json", "r") as f:
        alert_json = json.load(f)

    threat_memory = ThreatMemory()
    result = process_alert(alert_json, threat_memory)
    print("Result from process_alert:", result)
