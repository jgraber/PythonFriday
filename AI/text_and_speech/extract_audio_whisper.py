import whisper

model = whisper.load_model("tiny", device="cpu")
result = model.transcribe("audio_demo.wav")
print(result["text"])
