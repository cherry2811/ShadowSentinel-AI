import psutil
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from email_config import *

# Thresholds
CPU_THRESHOLD = 80  # percent
RAM_THRESHOLD = 85  # percent

def check_system():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"""[⚠️ SYSTEM RESOURCE ALERT]

Timestamp: {now}

CPU Usage: {cpu}%
RAM Usage: {ram}%
Disk Usage: {disk}%
"""

    if cpu > CPU_THRESHOLD or ram > RAM_THRESHOLD:
        send_email(message)
        print("🚨 High usage detected. Alert sent!")
    else:
        print("✅ Usage normal. No alert needed.")

def send_email(body):
    msg = MIMEText(body)
    msg['Subject'] = '🚨 ShadowSentinel Alert: High Resource Usage'
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

if __name__ == "__main__":
    check_system()
