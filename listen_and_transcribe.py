import whisper
import tempfile
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import time
import os

def record_voice(duration=7, samplerate=16000):
    print("\n🎙️ Speak after the beep...")
    time.sleep(1)
    print("🔴 Beep! Recording now...\n")
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    return recording, samplerate

def save_to_wav(data, samplerate):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    wav.write(temp_file.name, samplerate, data)
    return temp_file.name

def transcribe_audio(file_path):
    print("🧠 Transcribing with Whisper...")
    model = whisper.load_model("base")
    result = model.transcribe(file_path)
    return result["text"]

def listen_and_transcribe():
    data, sr = record_voice()
    file_path = save_to_wav(data, sr)
    print(f"📁 Audio saved at: {file_path}")
    
    try:
        text = transcribe_audio(file_path)
        print(f"\n📝 You said: {text}")
    except Exception as e:
        print(f"❌ Error during transcription: {e}")
        text = ""

    # Optionally delete the temp audio file
    try:
        os.remove(file_path)
    except:
        pass

    return text

# 🔁 Test run
if __name__ == "__main__":
    listen_and_transcribe()
