import time
print("playsound3 to play audio files")

from playsound3 import playsound

# Play sounds from disk
playsound("sample.mp3")


print("... sleep for 2 seconds")
time.sleep(2)


# You can play sounds in the background
sound = playsound("sample.mp3", block=False)

# and check if they are still playing
while sound.is_alive():
    print("Sound is still playing!")
    time.sleep(1)

# and stop them whenever you like.
sound.stop()


print("... sleep for 2 seconds")
time.sleep(2)


print("pygame to play audio files")

import pygame

pygame.mixer.init()
pygame.mixer.music.load("sample.mp3")
pygame.mixer.music.play()

# Keep the program running while audio plays
while pygame.mixer.music.get_busy():
    continue


