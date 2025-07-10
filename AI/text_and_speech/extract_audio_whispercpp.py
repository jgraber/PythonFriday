from whispercpp import Whisper

w = Whisper('tiny')

result = w.transcribe("audio_demo.wav")
text = w.extract_text(result)
print(text)