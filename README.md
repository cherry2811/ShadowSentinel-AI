# 🧠 ShadowSentinel AI – Real-Time Cyber Guardian

**ShadowSentinel AI** is an elite, real-time cyber defense bot that uses AI to monitor Wazuh security alerts, auto-detect brute-force attacks, block attacker IPs instantly with `iptables`, and summarize threats using a local LLM. It also tracks system health, detects intrusions, generates daily reports, and includes an AI voice assistant named **Hazel**.

> 🕵️ Built by [@cherry2811](https://github.com/cherry2811) as a real-world, agentic cybersecurity project powered by automation and AI.

---

## 🎯 Features

✅ Real-time brute-force detection using Wazuh logs  
✅ Automatic IP blocking via `iptables`  
✅ Alert summarization with LLM (OpenRouter or local model)  
✅ AI memory: avoids re-blocking known threats  
✅ Daily summary report and email alerting  
✅ Hazel AI voice assistant: threat narration + wake word  
✅ System resource tracker (CPU, RAM, screentime logs)  
✅ USB & process watchlist intrusion alerts  
✅ Self-learning threat engine using `threat_memory.json`  
✅ Beautiful threat dashboard with 7-day trends  
✅ Stealth mode, vault unlock (face unlock), wake word: `"Hey Shadow"`

---

## 🛠️ Tech Stack

- **Python 3.12+**
- **Wazuh SIEM** for log input
- **iptables** for blocking
- **FAISS + LangChain + LLM (OpenRouter or Ollama)** for RAG-based threat summaries
- **Whisper / Vosk / Silero** for voice recognition
- **Text-to-Speech**: `gTTS`, `speech-dispatcher`, or Silero
- **Face Recognition** for vault unlock

---

## 📁 Folder Structure

wazuh-brute-force-blocker/
├── brute_force_blocker.py ← Brute force detection + IP block
├── realtime_monitor.py ← Monitors /var/ossec/logs/alerts.json
├── summarizer.py ← Summarizes alerts using AI
├── hazel_voice_assistant.py ← Hazel AI assistant (voice output)
├── wake_word_hey_shadow.py ← Wake word detection loop
├── resource_tracker.py ← Tracks CPU, RAM, screentime
├── threat_dashboard.py ← Generates visual dashboard (HTML)
├── daily_report.py ← Sends daily reports
├── intrusion_detector.py ← USB/process watchlist
├── threat_memory.json ← Stores previously seen threats
├── email_config.py ← Secure email credentials

---

## 🚀 How to Run

### 1. Clone the repo

```bash
git clone https://github.com/cherry2811/ShadowSentinel-AI.git
cd ShadowSentinel-AI


. Create and activate virtual environment
bash
Copy code
python3 -m venv sentinel-venv
source sentinel-venv/bin/activate



Install dependencies
bash
Copy code
pip install -r requirements.txt



Start real-time Wazuh alert monitoring
bash
Copy code
python3 realtime_monitor.py



Run Hazel voice assistant (optional)
bash
Copy code
python3 hazel_voice_assistant.py



Daily Report Setup (Optional)
Add your Gmail and receiver email to email_config.py

Setup email_daily_summary.py to run with a daily cron job






📊 Threat Dashboard
Run the dashboard generator:

bash
Copy code
python3 threat_dashboard.py
It will generate dashboard.html showing daily threat scores and top IPs.

🤖 Wake Word + Vault Mode (Advanced)
Run wake_word_hey_shadow.py to activate wake word: "Hey Shadow"

Vault mode uses face unlock via webcam (see vault_lock.py)

🔐 Security Notes
All alerts, logs, and threat memory are local

You can extend to cloud storage or external APIs safely

Built for personal/home SOC lab security

👨‍💻 Author
Made with 💙 by Charan Reddy (cherry2811)



License
This project is licensed under the MIT License.
