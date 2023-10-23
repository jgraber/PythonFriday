import moviepy
import moviepy.editor

video = moviepy.editor.VideoFileClip("myvideo.mp4")
audio = video.audio

audio.write_audiofile("only_audio.mp3")
