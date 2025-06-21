import os
import wave
import numpy as np

# Set environment variable before importing sounddevice. Value is not important.
# os.environ["SD_ENABLE_ASIO"] = "1"

import sounddevice as sd


# select device
# sd.default.device = 'Echo Cancelling Speakerphone (D, MME'

# Parameters
duration = 5  # seconds
sample_rate = 44100  # 44.1 kHz
channels = 1  # 1 = Mono, 2 = Stereo
file_name = "output_sounddevice.wav"
frames = int(duration * sample_rate)
dtype = 'int16'

print("Recording...")

# Record audio
audio_data = sd.rec(frames, 
                    sample_rate=sample_rate, 
                    channels=channels, 
                    dtype=dtype)
sd.wait()  # Wait until recording is finished

# Save to file
with wave.open(file_name, 'wb') as wf:
    wf.setnchannels(channels)
    wf.setsampwidth(np.dtype(dtype).itemsize)
    wf.setframerate(sample_rate)
    wf.writeframes(audio_data.tobytes())

print(f"Recording saved as {file_name}")
