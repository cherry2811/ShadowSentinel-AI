import pvporcupine
import pyaudio
import struct

# Your Porcupine Access Key
ACCESS_KEY = "tdVTsJgIH+Iz+LkBzU0dupqCUEPY4BOQeSxox+xBapjt7GQC/Hi9pg=="

# Initialize Porcupine with "computer" keyword
porcupine = pvporcupine.create(access_key=ACCESS_KEY, keywords=["computer"])

pa = pyaudio.PyAudio()

stream = pa.open(
    rate=porcupine.sample_rate,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=porcupine.frame_length
)

print("🎤 Listening for wake word: 'computer'...")

try:
    while True:
        pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
        pcm_unpacked = struct.unpack_from("h" * porcupine.frame_length, pcm)

        keyword_index = porcupine.process(pcm_unpacked)
        if keyword_index >= 0:
            print("💡 Wake word detected!")

except KeyboardInterrupt:
    print("🛑 Stopped by user")

finally:
    stream.stop_stream()
    stream.close()
    pa.terminate()
    porcupine.delete()
