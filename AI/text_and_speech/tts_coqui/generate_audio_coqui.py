import torch
from TTS.api import TTS
from playsound3 import playsound

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

# Initialize TTS
tts = TTS("tts_models/en/jenny/jenny").to(device)

# TTS to a file
file_name = "coqui_jenny.wav"
tts.tts_to_file(
  text="Welcome to Python Friday.",
  file_path=file_name,
)

playsound(file_name)
