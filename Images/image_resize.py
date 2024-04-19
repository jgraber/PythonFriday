from PIL import Image

img = Image.open(r"Image.png")
base_width = 500
wpercent = (base_width / float(img.size[0]))
hsize = int((float(img.size[1]) * float(wpercent)))
img = img.resize((base_width, hsize), Image.Resampling.LANCZOS)
img.save(r"Image_small.png")