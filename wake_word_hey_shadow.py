import pvporcupine
import pyaudio
import struct
import os

# Your Porcupine Access Key
ACCESS_KEY = "tdVTsJgIH+Iz+LkBzU0dupqCUEPY4BOQeSxox+xBapjt7GQC/Hi9pg=="

# Path to your custom wake word .ppn file
WAKE_WORD_PATH = "hey_shadow.ppn"

# Initialize Porcupine with custom keyword
porcupine = pvporcupine.create(
    access_key=ACCESS_KEY,
    keyword_paths=[WAKE_WORD_PATH]
)

# Set up PyAudio input stream
pa = pyaudio.PyAudio()
stream = pa.open(
    rate=porcupine.sample_rate,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=porcupine.frame_length
)

print("🎤 Listening for 'Hey Shadow'... Speak softly, my sentinel...")

try:
    while True:
        pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
        pcm_unpacked = struct.unpack_from("h" * porcupine.frame_length, pcm)

        keyword_index = porcupine.process(pcm_unpacked)
        if keyword_index >= 0:
            print("🌑 Hey Shadow detected! Hazel is awake...")

except KeyboardInterrupt:
    print("🛑 Wake loop stopped.")

finally:
    stream.stop_stream()
    stream.close()
    pa.terminate()
    porcupine.delete()
