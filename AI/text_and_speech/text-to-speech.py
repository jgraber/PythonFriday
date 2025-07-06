import warnings

warnings.filterwarnings("ignore", category=UserWarning)

import sounddevice as sd
import numpy as np
import wave
import threading
import sys
import whisper
from datetime import datetime

# Parameters
sample_rate = 44100  # 44.1 kHz
channels = 1  # 1 = Mono, 2 = Stereo
file_name = "output_sounddevice.wav"
dtype = 'int16'
now = datetime.now()
transcription_file = f"transcription_{now.strftime("%Y%m%d_%H%M")}.txt"

# Load Whisper model
model = whisper.load_model("medium", device="cpu")


def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    recorded_frames.append(indata.copy())

def wait_for_enter():
    input("Recording... Press Enter to stop.\n")
    global recording
    recording = False

print("Welcome to the audio recording application!")
print("You can record audio and transcribe it using Whisper.")
print(f"The transcription will be saved to the file {transcription_file}.")
print()

while True:
   
    choice = input("Type 's' to start recording or 'e' to end the application: ").strip().lower()
    if choice == 's':
        # Reset recording state and buffer
        global recorded_frames, recording
        recorded_frames = []
        recording = True
        
        # Start enter-listening thread
        stop_thread = threading.Thread(target=wait_for_enter)
        stop_thread.start()
        print("Recording started... (hit Enter to stop)")

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

        print(f"Start with the transcription of the recorded audio...")

        result = model.transcribe(file_name)
        print(result["text"])
        print("\n\n\n*********")
        with open(transcription_file, "a", encoding="utf-8") as f:
            f.write(result["text"] + "\n")

    elif choice == 'e':
        print("Exiting program.")
        break
    else:
        print("Invalid input. Please type 'record' or 'stop'.")