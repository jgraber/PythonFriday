import moviepy
import moviepy.editor
# from moviepy.editor import *

video = moviepy.editor.VideoFileClip("myvideo.mp4")
audio = video.audio

audio.write_audiofile("only_audio.mp3")


# # Generate a text clip. You can customize the font, color, etc.
# txt_clip = TextClip("My Holidays 2023",fontsize=70,color='white')

# # Say that you want it to appear 10s at the center of the screen
# txt_clip = txt_clip.set_pos('center').set_duration(10)

# # Overlay the text clip on the first video clip
# video = CompositeVideoClip([video, txt_clip])

# # Write the result to a file (many options available !)
# video.write_videofile("myHolidays_edited.webm")