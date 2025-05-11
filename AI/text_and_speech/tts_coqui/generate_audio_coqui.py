import torch
from TTS.api import TTS

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

# Initialize TTS
tts = TTS("tts_models/en/jenny/jenny").to(device)

# TTS to a file
tts.tts_to_file(
  text="Welcome to Python Friday.",
  file_path="coqui_jenny.wav",
)