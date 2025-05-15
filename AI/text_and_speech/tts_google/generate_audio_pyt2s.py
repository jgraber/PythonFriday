from pyt2s.services import stream_elements, ibm_watson
from playsound3 import playsound
import tempfile

text = 'Lorem Ipsum is simply dummy text.'

# default voice
with tempfile.NamedTemporaryFile(mode='wb+', delete=True, suffix=".mp3") as tmp:
    data = stream_elements.requestTTS(text)

    tmp.write(data)
    tmp.seek(0)

    playsound(tmp.name)


# custom male voice
with tempfile.NamedTemporaryFile(mode='wb+', delete=True, suffix=".mp3") as tmp:
    data = stream_elements.requestTTS(text, stream_elements.Voice.Russell.value)

    tmp.write(data)
    tmp.seek(0)

    playsound(tmp.name)

# custom female voice
with tempfile.NamedTemporaryFile(mode='wb+', delete=True, suffix=".mp3") as tmp:
    data = stream_elements.requestTTS(text, stream_elements.Voice.Emma.value)

    tmp.write(data)
    tmp.seek(0)

    playsound(tmp.name)


# # IBM Watson as a service
# with tempfile.NamedTemporaryFile(mode='wb+', delete=True, suffix=".mp3") as tmp:
#     data = ibm_watson.requestTTS(text)

#     tmp.write(data)
#     tmp.seek(0)

#     playsound(tmp.name)