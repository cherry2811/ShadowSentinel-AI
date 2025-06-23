from gtts import gTTS
import os
import sys
import time

def speak_text(text):
    print("🎤 Speaking with gTTS...")
    try:
        tts = gTTS(text=text, lang='en')
        filename = "alert.mp3"
        tts.save(filename)
        os.system(f"mpg123 {filename}")
        time.sleep(1)
        os.remove(filename)
    except Exception as e:
        print("❌ Error using gTTS:", e)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_text = " ".join(sys.argv[1:])
    else:
        input_text = input("Enter alert summary to speak: ")

    speak_text(input_text)
