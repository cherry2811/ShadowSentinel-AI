# email_config.py

EMAIL_SENDER = "charanreddy098@gmail.com"
EMAIL_PASSWORD = "xtvezyelbraalvjg"  # Your Gmail App Password (no spaces)
EMAIL_RECEIVER = "9921004126@klu.ac.in"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 🔐 Your email details
SENDER_EMAIL = "charanreddy098@gmail.com"
SENDER_PASSWORD = "xlwswdqztqdwfvgo"  # use App Password, not regular one
RECEIVER_EMAIL = "9921004126@klu.ac.in"

def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
            print("✅ Email sent successfully.")
    except Exception as e:
        print("❌ Failed to send email:", e)
