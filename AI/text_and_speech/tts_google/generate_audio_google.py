from gtts import gTTS, lang
import tempfile
from playsound3 import playsound

# supported languages
languages = lang.tts_langs()
for key in languages.keys():
    print(f"{key}: \t {languages[key]}")


# example with an Enlgish text and an English voice
with tempfile.NamedTemporaryFile(mode='wb+', delete=True, suffix=".mp3") as tmp:
    text = "Hello, I am speaking using Google's text to speech service."
    
    tts = gTTS(text=text, lang='en') #options: slow=True or tld='com.ng'
    
    tts.write_to_fp(tmp)
    tmp.seek(0)
    # tts.save("output.mp3") # for regular files
    
    playsound(tmp.name)


# example with a German text and a German voice
with tempfile.NamedTemporaryFile(mode='wb+', delete=True, suffix=".mp3") as tmp:
    text = "Dies ist ein Text auf Deutsch."
    
    tts = gTTS(text=text, lang='de')
    
    tts.write_to_fp(tmp)
    tmp.seek(0)
    
    playsound(tmp.name)