# pip install exif
from exif import Image

with open('venezia.jpg', 'rb') as image_file:
    my_image = Image(image_file)

if(my_image.has_exif):
    print(my_image.list_all())
    for x in my_image.list_all():
        try:
            print(x)
            print(getattr(my_image, x, '-'))
        except Exception:
            print("--")