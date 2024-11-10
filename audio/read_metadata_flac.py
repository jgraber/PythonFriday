import mutagen
from mutagen.flac import FLAC

file = "sample.flac"
print(f"file: \t\t {file}")
print("-" * 50)

audio = FLAC(file)
print(f"length: \t {audio.info.length}")
print(f"sample_rate: \t {audio.info.sample_rate}")
print(f"bitrate: \t {audio.info.bitrate}")
print(f"channels: \t {audio.info.channels}")
print(f"pprint: \t {audio.pprint()}")
print("*" * 50)
