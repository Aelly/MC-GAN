# coding: utf8

import os
import sys
import glob
import string

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

def main(argv):
    chars = string.ascii_letters + string.digits + string.punctuation + u'à' + u'â' + u'ç' + u'è' + u'é' + u'ê' + u'î' + u'ô' + u'ù'  + u'û' + u'À' + u'Â' + u'Ç' + u'È' + u'É' + u'Ê' + u'Î' + u'Ô' + u'Ù' + u'Û'

    list_ = []

    for char in chars:
        list_.append(char)

    print('Creating images with ' + str(len(list_)) + ' characters')

    usage = 'python font2png.py [dir with font file] [output dir]'

    if len(argv) != 3:
        print(usage)
        sys.exit()

    # Add the / for linux and \ for windows at the end of the dir name if not present
    font_path = os.path.join(argv[1], '')
    out_path = os.path.join(argv[2], '')

    if not os.path.isdir(out_path):
        print('output dir is not a directory')
        print(usage)
        sys.exit()

    if not os.path.isdir(font_path):
        print('font dir is not a directory')
        print(usage)
        sys.exit()

    for font_file in glob.glob(os.path.join(font_path, '*.[ot]tf')):
        font = ImageFont.truetype(font_file, 65)

        font_name = os.path.basename(font_file).split('.')[0]
        font_name = font_name.replace("_", "-")
        font_name = font_name.replace(" ", "-")
        print(font_name)

        image_all = Image.new('RGBA', (64*len(list_),64), 'white')
        offset = 0

        for char in chars:
            # Draw each char on its own image
            # https://stackoverflow.com/questions/43060479/how-to-get-the-font-pixel-height-using-pil-imagefont
            (width, baseline), (offset_x, offset_y) = font.font.getsize(char)
            ascent, descent = font.getmetrics()
            textwidth, textheight = font.getsize(char)
            box = font.getmask(char).getbbox()
            img = Image.new('RGBA', (textwidth, (ascent + descent)), (255,255,255))
            d = ImageDraw.Draw(img)
            d.text((-offset_x, 0),char,(0,0,0),font=font)

            # Resize this image in 64*64 while keeping proportion
            new_img = Image.new("RGBA", (64,64), "white")
            width, height = img.size
            if width != 0 and height != 0:
                if width >= height:
                    new_height = int(64 * height / width)
                    if new_height != 0:
                        img = img.resize((64,new_height), Image.ANTIALIAS)
                        new_img.paste(img,(0,int((64-new_height)/2)))
                        # Paste it in the image with all the characters
                        image_all.paste(new_img, (64*offset, 0))
                else:
                    new_width = int(64 * width / height)
                    if new_width != 0:
                        img = img.resize((new_width,64), Image.ANTIALIAS)
                        new_img.paste(img,(int((64-new_width)/2),0))
                        # Paste it in the image with all the characters
                        image_all.paste(new_img, (64*offset, 0))
            offset = offset + 1

        image_all.save(out_path + font_name + '.0.0.png')

if __name__ == "__main__":
    main(sys.argv)
