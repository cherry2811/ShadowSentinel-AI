import speech_recognition as sr

r = sr.Recognizer()
with sr.Microphone() as source:
    print("🎤 Say something in 4 seconds...")
    audio = r.listen(source,timeout=5, phrase_time_limit=4)

print("✅ Got your voice! Trying to recognize it...")

try:
    print("You said:", r.recognize_google(audio))
except sr.UnknownValueError:
    print("❌ Didn't understand you.")
except sr.RequestError as e:
    print("❌ Recognition error:", e)
