import time

def follow_file(file_path):
    with open(file_path, 'r') as file:
        file.seek(0, 2)
        while True:
            line = file.readline()
            if not line:
                time.sleep(0.5)
                continue
            yield line

def is_important_alert(line):
    keywords = ["sshd", "failed", "brute-force", "unauthorized", "login attempt"]
    level_keywords = ["level 7", "level 10", "level 9", "level 8"]
    
    return any(kw in line.lower() for kw in keywords + level_keywords)

def main():
    log_path = '/var/ossec/logs/alerts/alerts.log'
    log_lines = follow_file(log_path)
    print("🎯 Monitoring for important alerts...")

    for line in log_lines:
        line = line.strip()
        if line and is_important_alert(line):
            print(f"🚨 Important alert: {line}")

if __name__ == "__main__":
    main()
