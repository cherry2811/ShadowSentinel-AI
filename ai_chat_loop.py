import os
import torch
import whisper
import speech_recognition as sr
import requests
import soundfile as sf
import time

# ========== CONFIG ==========
OPENROUTER_API_KEY = "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"
sample_rate = 48000
speaker = "en_1"
device = torch.device("cpu")  # Use 'cuda' if you have GPU

# ========== SETUP ==========
print("📦 Loading models...")
model = torch.package.PackageImporter("silero_en.pt").load_pickle("tts_models", "model")
model.to(device)
whisper_model = whisper.load_model("base")
recognizer = sr.Recognizer()
mic = sr.Microphone(device_index=1)  # Set correct mic index

# ========== AI REQUEST ==========
def get_ai_reply(prompt):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://chat.openai.com",
        "Content-Type": "application/json"
    }
    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You're Hazel, Charan’s elite AI guardian. Speak calmly, clearly, and protectively."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print("❌ GPT error:", e)
        return "Sorry, I couldn't connect to my brain right now."

# ========== VOICE OUTPUT ==========
def speak(text):
    print(f"\n🗣 Hazel says: {text}")
    try:
        print("🔁 Generating voice...")
        audio = model.apply_tts(text=text, speaker=speaker, sample_rate=sample_rate)

        print("💾 Saving to WAV...")
        sf.write("hazel_reply.wav", audio, sample_rate)

        print("🔃 Downsampling to 16kHz...")
        os.system("sox hazel_reply.wav hazel_reply_16k.wav rate 16000")

        print("🔊 Playing voice...")
        time.sleep(0.3)  # small delay helps VM breathe
        os.system("aplay hazel_reply_16k.wav")
    except Exception as e:
        print("❌ Voice generation failed:", e)

# ========== MAIN CHAT LOOP ==========
def listen_and_respond():
    with mic as source:
        print("\n🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    with open("user.wav", "wb") as f:
        f.write(audio.get_wav_data())

    print("🧠 Transcribing with Whisper...")
    result = whisper_model.transcribe("user.wav")
    user_input = result["text"]
    print("🧍 You said:", user_input)

    reply = get_ai_reply(user_input)
    print("🧠 AI replied:", reply)

    speak(reply)

# ========== RUN LOOP ==========
if __name__ == "__main__":
    while True:
        listen_and_respond()
