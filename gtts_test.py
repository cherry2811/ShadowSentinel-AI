from gtts import gTTS

try:
    tts = gTTS("Hello Charan, testing gTTS.")
    tts.save("test.mp3")
    print("✅ gTTS saved test.mp3 successfully")
except Exception as e:
    print("❌ gTTS error:", e)
