# coding: utf8

import os
import sys
import glob
import string

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

def main(argv):
    usage = 'python chars2png.py [dir with png file]'

    if len(argv) != 2:
        print(usage)
        sys.exit()

    chars = string.ascii_letters + string.digits + string.punctuation + u'à' + u'â' + u'ç' + u'è' + u'é' + u'ê' + u'î' + u'ô' + u'ù' + u'û' + u'À' + u'Â' + u'Ç' + u'È' + u'É' + u'Ê' + u'Î' + u'Ô' + u'Ù' + u'Û'
    chars_check = ""
    image= Image.new('RGBA', (64*len(chars),64), 'white')
    path = argv[1]
    for filename in glob.glob(os.path.join(path, '*.png')):
        char_file = os.path.basename(filename).split("_",2)[0]
        if "COLON" in char_file:
            char_file = ':'
        if "POINT" in char_file:
            char_file = '.'
        if (char_file in chars and char_file not in chars_check):
            pos = chars.index(char_file)
            chars_check = chars_check + char_file
            tmp_image = Image.open(filename)
            width, height = tmp_image.size
            char_img = Image.new("RGBA", (64,64), "white")
            if width >= height:
                new_height = 64 * height / width
                tmp_image = tmp_image.resize((64,int(new_height)), Image.ANTIALIAS)
                char_img.paste(tmp_image,(0,int((64-new_height)/2)))
            else:
                new_width = 64 * width / height
                tmp_image = tmp_image.resize((int(new_width),64), Image.ANTIALIAS)
                char_img.paste(tmp_image,(int((64-new_width)/2),0))

            pixdata = char_img.load()
            width, height = char_img.size
            for y in range(height):
                for x in range(width):
                    if pixdata[x, y][3] < 20:
                        pixdata[x, y] = (255, 255, 255, 255)

            image.paste(char_img, (64*pos, 0))
    print(chars_check)
    image.save(os.path.basename(os.path.normpath(path))+".png")
if __name__ == "__main__":
    main(sys.argv)
