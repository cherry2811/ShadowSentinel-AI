import subprocess
import time
from speak_alerts import speak  # 🎤 Hazel speaks alerts
from datetime import datetime

# ⚠️ Watchlist of suspicious tools
WATCHLIST_PROCESSES = ["sqlmap", "ngrok", "nmap", "hydra", "netcat", "netcat6", "wireshark", "tcpdump"]
WATCHLIST_USB_NAMES = ["Android", "USB Ethernet", "Kingston", "SanDisk", "WD", "Transcend"]

def check_usb_devices():
    try:
        result = subprocess.check_output("lsusb", shell=True).decode()
        for line in result.splitlines():
            for name in WATCHLIST_USB_NAMES:
                if name.lower() in line.lower():
                    alert_msg = f"🚨 Suspicious USB detected: {name}"
                    print(alert_msg)
                    speak(alert_msg)
                    log_alert(alert_msg)
    except Exception as e:
        print("USB check failed:", e)

def check_processes():
    try:
        result = subprocess.check_output("ps -ef", shell=True).decode()
        for proc in result.splitlines():
            for watch_proc in WATCHLIST_PROCESSES:
                if watch_proc.lower() in proc.lower():
                    alert_msg = f"🚨 Watchlist process detected: {watch_proc}"
                    print(alert_msg)
                    speak(alert_msg)
                    log_alert(alert_msg)
    except Exception as e:
        print("Process check failed:", e)

def log_alert(msg):
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_entry = f"{datetime.now()} — {msg}"
    
    # ✍️ Write to intrusion log
    with open("intrusion_log.txt", "a") as f:
        f.write(log_entry + "\n")

    # 📸 Take screenshot
    screenshot_file = f"screenshots/alert_{now}.png"
    try:
        subprocess.run(["scrot", screenshot_file])
        print(f"📸 Screenshot saved: {screenshot_file}")
    except Exception as e:
        print("❌ Screenshot failed:", e)

if __name__ == "__main__":
    print("🔍 Running intrusion scan...")
    check_usb_devices()
    check_processes()
    print("✅ Scan complete. See intrusion_log.txt if any alerts were triggered.")
