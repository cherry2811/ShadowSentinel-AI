import psutil
from datetime import datetime
import os

# Create logs folder if it doesn't exist
LOG_DIR = "/home/charan/wazuh-brute-force-blocker/logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "resource_log.txt")

def log_resources():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{now}] CPU: {cpu}% | RAM: {ram}% | Disk: {disk}%\n"

    with open(LOG_FILE, "a") as f:
        f.write(log_line)

if __name__ == "__main__":
    log_resources()
