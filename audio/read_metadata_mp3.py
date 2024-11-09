import mutagen
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

file = "sample.mp3"
print(f"file: \t\t {file}")
print("-" * 50)

audio = MP3(file)
print(f"length: \t {audio.info.length}")
print(f"sample_rate: \t {audio.info.sample_rate}")
print(f"bitrate: \t {audio.info.bitrate}")
print(f"bitrate_mode: \t {audio.info.bitrate_mode}")
print(f"channels: \t {audio.info.channels}")
print(f"pprint: \t {audio.info.pprint()}")

print("-" * 50)

id3 = EasyID3(file)
print(id3.pprint())

print("*" * 50)
