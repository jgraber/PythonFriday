from typing import NamedTuple
import glob
import pathlib
import os
# pip install mutagen
import mutagen
from mutagen.flac import FLAC
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

class Track(NamedTuple):
    artist: str
    album: str
    track: str
    title: str
    year: str


def extract_data(name):
    parts = name.split("-")
    first = parts[0].strip().split(" ")
    artist = first[0]
    album_track = first[1]
    album = album_track[0:3]
    track = album_track[3:]
    title = parts[1][1:parts[1].index("(")].strip()
    year = parts[1][parts[1].index("(")+1:parts[1].index(")")].strip()
    # print(f"{artist}|{album}|{track}|{title}|{year}|")
    return Track(artist, album, track, title, year)


def set_metadata_to_mp3_file(file_name, data):
    audio = EasyID3(file_name)
    audio["artist"] = data.artist
    audio["albumartist"] = data.artist
    audio["album"] = data.album
    audio["tracknumber"] = data.track
    audio["title"] = data.title
    audio["date"] = data.year
    print(audio.pprint())
    audio.save()

def set_metadata_to_flac_file(file_name, data):
    audio = FLAC(file_name)
    audio["artist"] = data.artist
    audio["albumartist"] = data.artist
    audio["album"] = data.album
    audio["tracknumber"] = data.track
    audio["title"] = data.title
    audio["date"] = data.year
    print(audio.pprint())
    audio.save()

# data = extract_data("Poirot S01E01 - The Adventure of the Clapham Cook (1989)-converted.flac")
# print(data)
# set_metadata_to_mp3_file("sample-3s.mp3", data)
# set_metadata_to_flac_file("sample3.flac", data)

# mp3_files = glob.iglob('**/*.mp3', recursive=True)
# for mp3 in mp3_files:
#     print(mp3)


cwd = os.getcwd()
path = pathlib.Path(cwd)
print(cwd)
files = path.rglob("*.flac")
for f in files:
    print(f)
    data = extract_data(f.name)
    set_metadata_to_flac_file(f, data)



# audio = MP3("sample-3s.mp3")
# print(audio.pprint())
# print(audio.keys())
# for frame in mutagen.File("sample-3s.mp3").tags.getall("TXXX"):
#     frame
# # audio["title"] = u"demo"
# # print(audio.pprint())


# print(EasyID3.valid_keys.keys())

