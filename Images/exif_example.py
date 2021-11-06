# pip install exif
from exif import Image

def decimal_coords(coords, ref):
    '''from https://medium.com/spatial-data-science/how-to-extract-gps-coordinates-from-images-in-python-e66e542af354 '''
    decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
    if ref == 'S' or ref == 'W':
        decimal_degrees = -decimal_degrees
    return decimal_degrees

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

lat = decimal_coords(my_image.gps_latitude, my_image.gps_latitude_ref)
long = decimal_coords(my_image.gps_longitude, my_image.gps_longitude_ref)
print(f'Location: {lat}, {long}')