import mutagen
from mutagen.flac import FLAC

file = "sample.flac"
print(f"file: \t\t {file}")
print("-" * 50)

audio = FLAC(file)
print("Before")
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
print("After")
print(audio.pprint())

