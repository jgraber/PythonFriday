import pyaudio
import wave
import threading
import sys

# Audio recording parameters
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
WAVE_OUTPUT_FILENAME = "output_pyaudio.wav"

frames = []
recording = True

def record_audio():
    global frames, recording

    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Open stream
    stream = audio.open(format=FORMAT,
                        input_device_index=0,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    print("Recording... Press Enter to stop.")

    # Record loop
    while recording:
        data = stream.read(CHUNK)
        frames.append(data)

    print("Recording stopped.")

    # Stop and close stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save to file
    with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    print(f"Saved recording as {WAVE_OUTPUT_FILENAME}")

# Thread to handle recording
recording_thread = threading.Thread(target=record_audio)
recording_thread.start()

# Wait for Enter key
input()  # Press Enter to stop
recording = False
recording_thread.join()
