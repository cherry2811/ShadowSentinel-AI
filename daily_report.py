import json
from datetime import datetime, timedelta

LOG_FILE = "/var/ossec/logs/alerts/alerts.json"

def read_last_24_hours_logs():
    now = datetime.now()
    cutoff = now - timedelta(hours=24)
    alerts = []

    with open(LOG_FILE, "r") as f:
        for line in f:
            try:
                alert = json.loads(line.strip())
                alert_time = datetime.strptime(alert['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ")
                if alert_time > cutoff:
                    alerts.append(alert)
            except:
                continue

    return alerts

def analyze_alerts(alerts):
    brute_force = 0
    blocked_ips = set()
    for alert in alerts:
        rule = alert.get("rule", {})
        desc = rule.get("description", "").lower()
        src_ip = alert.get("data", {}).get("srcip", None)

        if "brute-force" in desc:
            brute_force += 1
            if src_ip:
                blocked_ips.add(src_ip)

    return brute_force, list(blocked_ips)

if __name__ == "__main__":
    alerts = read_last_24_hours_logs()
    brute_force_count, blocked_ips = analyze_alerts(alerts)

    print(f"\n🧠 ShadowSentinel Report – {datetime.now().strftime('%Y-%m-%d')}")
    print(f"Brute-force attempts: {brute_force_count}")
    print(f"Blocked IPs: {blocked_ips}")

    # 🔮 Simulated AI Summary
    if brute_force_count == 0:
        summary = "System secure. No suspicious activity detected."
    elif brute_force_count <= 3:
        summary = "Low threat activity observed. A few brute-force attempts were blocked."
    else:
        summary = "High threat level detected. Multiple brute-force attacks were blocked. Recommend reviewing firewall settings."

    print("\n📩 AI Summary:")
    print(summary)

from email_config import send_email  # 🔐 Already configured by you

def format_email(brute_force_count, blocked_ips, summary):
    subject = f"🧠 ShadowSentinel Daily Report – {datetime.now().strftime('%Y-%m-%d')}"
    body = f"""
🧠 ShadowSentinel AI – Daily Threat Report

📅 Date: {datetime.now().strftime('%Y-%m-%d')}
🔒 Brute-force attempts: {brute_force_count}
🚫 Blocked IPs: {', '.join(blocked_ips) if blocked_ips else 'None'}

📩 AI Summary:
{summary}

Regards,  
ShadowSentinel AI System
"""
    return subject, body

# 📤 Send email
if __name__ == "__main__":
    alerts = read_last_24_hours_logs()
    brute_force_count, blocked_ips = analyze_alerts(alerts)

    print(f"\n🧠 ShadowSentinel Report – {datetime.now().strftime('%Y-%m-%d')}")
    print(f"Brute-force attempts: {brute_force_count}")
    print(f"Blocked IPs: {blocked_ips}")

    # 🔮 Simulated AI Summary
    if brute_force_count == 0:
        summary = "System secure. No suspicious activity detected."
    elif brute_force_count <= 3:
        summary = "Low threat activity observed. A few brute-force attempts were blocked."
    else:
        summary = "High threat level detected. Multiple brute-force attacks were blocked. Recommend reviewing firewall settings."

    print("\n📩 AI Summary:")
    print(summary)

    # Format + send email
    subject, body = format_email(brute_force_count, blocked_ips, summary)
    send_email(subject, body)
    print("✅ Daily report email sent successfully.")

