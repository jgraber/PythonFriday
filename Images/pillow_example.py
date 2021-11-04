# pip install Pillow
from PIL import Image
from PIL.ExifTags import TAGS

for (k,v) in Image.open('venezia.jpg')._getexif().items():
    if (TAGS.get(k) == 'MakerNote' or TAGS.get(k) == 'UserComment'):
        continue
    else:
        print('%s = %s' % (TAGS.get(k), v))