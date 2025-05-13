# https://github.com/nateshmbhat/pyttsx3

import pyttsx3
engine = pyttsx3.init()

# RATE (= speed)
rate = engine.getProperty('rate')   # get current speaking rate
print (rate)                        # 200 on Windows 11                     
engine.setProperty('rate', 160)     # set new voice rate

# VOICE
voices = engine.getProperty('voices')  # get installed voices
for voice in voices:
    print(voice.id)

engine.setProperty('voice', voices[1].id) # set a specific voice

engine.say("Welcome to Python Friday, a weekly post on Python.")
engine.runAndWait()

engine.save_to_file('Hello World', 'test.mp3')
engine.runAndWait()

engine.stop()