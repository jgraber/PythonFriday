from vosk import Model, KaldiRecognizer
import wave
import json

wf = wave.open("audio_demo.wav", "rb")
if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
    raise ValueError("Audio file must be WAV format PCM mono.")

model = Model("vosk-model-small-en-us-0.15")  # Make sure this folder exists
rec = KaldiRecognizer(model, wf.getframerate())

result = ""
while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        res = json.loads(rec.Result())
        result += res.get("text", "") + " "

# Final partial result
res = json.loads(rec.FinalResult())
result += res.get("text", "")

print("Recognized text:\n", result)
