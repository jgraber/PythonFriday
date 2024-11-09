import mutagen
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

file = "sample.mp3"
print(f"file: \t\t {file}")
print("-" * 50)

audio = EasyID3(file)
print(audio.pprint())

print("-" * 50)
print("write metadata")


audio["artist"] = "Jon Doe"
audio["albumartist"] = "Jon Doe II"
audio["album"] = "Python rules"
audio["tracknumber"] = "1"
audio["title"] = "Writing Metadata"
audio["date"] = "2024"
audio["genre"] = "Education"
audio.save()

print("-" * 50)

audio = EasyID3(file)
print(audio.pprint())

