import sounddevice as sd
import scipy.io.wavfile as wav

samplerate = 16000
duration = 5  # seconds
filename = "test_mic.wav"

print("🎙️ Speak into your mic after the beep...")
sd.sleep(1000)
print("🔴 Recording...")
recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
sd.wait()

print(f"📁 Saving recording to {filename}")
wav.write(filename, samplerate, recording)
print("✅ Done. Play it using: aplay test_mic.wav")
