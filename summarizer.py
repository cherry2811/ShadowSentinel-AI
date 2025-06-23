import subprocess
import json

def summarize_threat(alert):
    prompt = f"""
You are a cybersecurity analyst AI. Analyze the following Wazuh alert and summarize it in 1 short sentence:

{json.dumps(alert, indent=2)}
"""

    try:
        result = subprocess.run(
            ["ollama", "run", "mistral", prompt],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return "⚠️ AI summarization failed."
    except Exception as e:
        return f"❌ Error: {str(e)}"
