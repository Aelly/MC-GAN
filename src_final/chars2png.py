# coding: utf8

import os
import sys
import glob
import string
import json

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

reload(sys)
sys.setdefaultencoding('utf-8')

CHAR_SIZE = 64

def main(argv):
    usage = 'python chars2png.py [PNG directory]'

    if len(argv) != 2:
        print(usage)
        sys.exit()

    # Load the list of char stored in chars.json
    listOfChars = []

    json_path = os.path.join(os.path.dirname(sys.argv[0]), "chars.json")

    with open(json_path) as json_data:
        d = json.load(json_data)
        for char in d['char']:
            listOfChars.append(char)

    chars_check = ""
    image= Image.new('RGBA', (CHAR_SIZE*len(listOfChars), CHAR_SIZE), 'white')

    # Add the / for linux and \ for windows at the end of the dir name if not present
    path = os.path.join(argv[1], '')

    dataset_name = os.path.basename(os.path.dirname(path))

    if '_' in dataset_name:
        print("The dataset name can't contain '_'")
        print(usage)
        sys.exit()

    if not os.path.isdir(path):
        print('PNG dir is not a directory')
        print(usage)
        sys.exit()

    if len([filename for filename in glob.glob(os.path.join(path, '*.png'))]) < 2:
        print("Need at least 2 png file in the image directory")
        print(usage)
        sys.exit()

    for filename in glob.glob(os.path.join(path, '*.png')):
        char_file = os.path.basename(filename).split("_",2)[0]
        # Detect special filename used by the etractor from DocCreator
        if "COLON" in char_file:
            char_file = ':'
        if "POINT" in char_file:
            char_file = '.'
        if "SPACE" in char_file:
            char_file = ' '
        if "STAR" in char_file:
            char_file = '*'
        if "SLASH" in char_file:
            char_file = '/'
        # Check if the char has already been created
        if (char_file in listOfChars and char_file not in chars_check):
            pos = listOfChars.index(char_file)
            chars_check = chars_check + char_file
            tmp_image = Image.open(filename)
            width, height = tmp_image.size
            char_img = Image.new("RGBA", (CHAR_SIZE, CHAR_SIZE), "white")

            # Resize img if not CHAR_SIZE*CHAR_SIZE
            if width >= height:
                new_height = CHAR_SIZE * height / width
                tmp_image = tmp_image.resize((CHAR_SIZE,int(new_height)), Image.ANTIALIAS)
                char_img.paste(tmp_image,(0,int((CHAR_SIZE-new_height)/2)))
            else:
                new_width = CHAR_SIZE * width / height
                tmp_image = tmp_image.resize((int(new_width), CHAR_SIZE), Image.ANTIALIAS)
                char_img.paste(tmp_image,(int((CHAR_SIZE-new_width)/2),0))

            # Fill the transparent background with white
            pixdata = char_img.load()
            width, height = char_img.size
            for y in range(height):
                for x in range(width):
                    if pixdata[x, y][3] < 20:
                        pixdata[x, y] = (255, 255, 255, 255)

            # Paste the character on the final image
            image.paste(char_img, (CHAR_SIZE*pos, 0))
    print("Characters on the image : '" + chars_check + "'")
    image.save(os.path.basename(os.path.normpath(path))+".png")
if __name__ == "__main__":
    main(sys.argv)
