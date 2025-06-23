import subprocess

def load_top_threats(file="top_threats.txt"):
    with open(file, "r") as f:
        content = f.read()
    return content

def summarize_with_ollama(text):
    prompt = f"You are a cybersecurity AI. Summarize the following Wazuh threat logs in one short sentence:\n\n{text}"
    result = subprocess.run(["ollama", "run", "mistral", prompt], capture_output=True, text=True)
    return result.stdout.strip()

if __name__ == "__main__":
    print("📂 Reading top 5 threats...")
    threats_text = load_top_threats()
    print("🧠 Summarizing using Mistral...")
    summary = summarize_with_ollama(threats_text)

    print("\n✅ Daily AI Threat Summary:\n")
    print(f"💡 {summary}")

    with open("daily_summary.txt", "w") as f:
        f.write(summary + "\n")
