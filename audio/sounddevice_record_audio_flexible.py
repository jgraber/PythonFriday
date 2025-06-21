import sounddevice as sd
import numpy as np
import wave
import threading
import sys

# Parameters
sample_rate = 44100  # 44.1 kHz
channels = 1  # 1 = Mono, 2 = Stereo
file_name = "output_sounddevice.wav"
dtype = 'int16'

# Buffer to hold recorded data
recorded_frames = []
recording = True

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    recorded_frames.append(indata.copy())

def wait_for_enter():
    input("Recording... Press Enter to stop.\n")
    global recording
    recording = False

# Start enter-listening thread
stop_thread = threading.Thread(target=wait_for_enter)
stop_thread.start()

# Start recording stream
with sd.InputStream(samplerate=sample_rate, 
                    channels=channels, 
                    dtype=dtype, 
                    callback=callback):
    while recording:
        sd.sleep(100)

# Combine and save to file
audio_data = np.concatenate(recorded_frames)

with wave.open(file_name, 'wb') as wf:
    wf.setnchannels(channels)
    wf.setsampwidth(np.dtype(dtype).itemsize)
    wf.setframerate(sample_rate)
    wf.writeframes(audio_data.tobytes())

print(f"Saved recording as {sample_rate}")
