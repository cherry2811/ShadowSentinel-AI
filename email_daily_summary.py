import smtplib
from email.mime.text import MIMEText
from email_config import SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL

def send_summary_email():
    print("📤 Sending daily summary email...")  # Status print

    try:
        with open("daily_summary.txt", "r") as f:
            summary = f.read()
    except FileNotFoundError:
        print("❌ daily_summary.txt not found.")
        return

    msg = MIMEText(summary)
    msg["Subject"] = "🛡️ ShadowSentinel AI - Daily Threat Summary"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        print(f"✅ Daily summary email sent successfully to {RECEIVER_EMAIL}!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

if __name__ == "__main__":
    send_summary_email()
