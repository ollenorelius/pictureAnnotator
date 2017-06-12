import os
import sys
from PIL import Image, ImageOps

folder = sys.argv[1]

if not os.path.exists(folder):
    print('Could not find specified data folder:', folder)
    quit()

file_list = os.listdir(folder)
for f in file_list:
    img = Image.open(folder + '/' + f)
    img = ImageOps.flip(img)
    img.save(folder + '/' + f)
