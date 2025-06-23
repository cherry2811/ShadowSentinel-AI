import openai
import speech_recognition as sr
import subprocess
import time

# 🔐 OpenRouter API Setup
openai.api_key = "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"
openai.api_base = "https://openrouter.ai/api/v1"

WAKE_WORD = "hey shadow"
EXIT_WORDS = ["exit", "goodbye", "stop", "quit"]

# 🎤 Speak response using espeak
def speak(text):
    print(f"💬 Hazel replied: {text}")
    with open("hazel_chat.log", "a") as f:
        f.write(f"Hazel: {text}\n")
    subprocess.call(["espeak", text])

# 🧠 Ask AI model
def ask_ai(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="mistralai/mistral-7b-instruct",
            messages=[
                {"role": "system", "content": "You are Hazel, a helpful cybersecurity assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error talking to Hazel: {e}"

# 🎙️ Listen to speech
def listen_for_speech():
    r = sr.Recognizer()
    with sr.Microphone(sample_rate=16000) as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("🎧 Listening...")
        try:
            audio = r.listen(source, timeout=6)
            return r.recognize_google(audio).lower()
        except:
            return ""

# 🚀 Main loop
if __name__ == "__main__":
    print("🔐 ShadowSentinel AI listening for wake word...")

    while True:
        try:
            speech = listen_for_speech()
            if WAKE_WORD in speech:
                speak("Yes, I'm here. How can I help?")
                while True:
                    user_query = listen_for_speech()
                    if user_query:
                        print(f"🧠 You said: {user_query}")
                        with open("hazel_chat.log", "a") as f:
                            f.write(f"You: {user_query}\n")

                        if any(word in user_query for word in EXIT_WORDS):
                            speak("Goodbye, I’ll be here when you need me.")
                            break

                        reply = ask_ai(user_query)
                        speak(reply)
            time.sleep(0.5)

        except KeyboardInterrupt:
            print("\n🛑 Exiting.")
            break
