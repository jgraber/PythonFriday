import pyaudio
import wave

# Audio recording parameters
FORMAT = pyaudio.paInt16  # 16-bit resolution
CHANNELS = 1              # 2: Stereo, 1: Mono
RATE = 44100              # 44.1kHz sampling rate
CHUNK = 1024              # Record in chunks of 1024 samples
RECORD_SECONDS = 5        # Duration of recording
WAVE_OUTPUT_FILENAME = "output_pyaudio.wav"

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open audio stream
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    input_device_index=None,  # device ID or None for default
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

print("Recording...")

frames = []

# Record data in chunks
for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("Finished recording.")

# Stop and close stream
stream.stop_stream()
stream.close()
audio.terminate()

# Save recorded data to WAV file
with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))

print(f"Saved recording as {WAVE_OUTPUT_FILENAME}")
