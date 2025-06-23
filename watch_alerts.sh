#!/bin/bash

echo "👁️ Watching for new Wazuh alerts in real-time..."

ALERT_FILE="/home/charan/wazuh-brute-force-blocker/test_alerts.json"
SCRIPT="/home/charan/wazuh-brute-force-blocker/brute_force_blocker.py"

while true
do
  inotifywait -e modify "$ALERT_FILE" >/dev/null 2>&1
  echo "⚡ New alert detected! Running SOAR script..."
  python3 "$SCRIPT"
done
