# coding: utf8

import os
import sys
import glob
import string

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

CHAR_SIZE = 64

def main(argv):
    chars = string.ascii_letters + string.digits + string.punctuation + u'à' + u'â' + u'ç' + u'è' + u'é' + u'ê' + u'î' + u'ô' + u'ù'  + u'û' + u'À' + u'Â' + u'Ç' + u'È' + u'É' + u'Ê' + u'Î' + u'Ô' + u'Ù' + u'Û'

    list_ = []

    for char in chars:
        list_.append(char)

    usage = "Usage : python font2png.py [dir with font file] [output dir]"

    if len(argv) != 3:
        print(usage)
        sys.exit()

    font_path =argv[1]
    out_path = argv[2]

    # Test if argv are directory and create output dir if not exist
    if os.path.exists(out_path):
        if not os.path.isdir(out_path):
            print("output dir '" + out_path + "' is not a directory")
            print(usage)
            sys.exit()
    else:
        print ("Create output directory : " + out_path)
        os.mkdir(out_path)

    if not os.path.isdir(font_path):
        print("font dir '" + font_path + "' is not a directory")
        print(usage)
        sys.exit()

    print("Creating images with " + str(len(list_)) + " characters")
    # Add the / for linux and \ for windows at the end of the dir name if not present
    font_path = os.path.join(argv[1], '')
    out_path = os.path.join(argv[2], '')

    for font_file in glob.glob(os.path.join(font_path, "*.[ot]tf")):
        font = ImageFont.truetype(font_file, CHAR_SIZE)

        font_name = os.path.basename(font_file).split('.')[0]
        font_name = font_name.replace("_", "-")
        font_name = font_name.replace(" ", "-")
        print(font_name)

        image_all = Image.new("RGBA", (CHAR_SIZE*len(list_),CHAR_SIZE), "white")
        offset = 0

        for char in chars:
            # Draw each char on its own image
            # https://stackoverflow.com/questions/43060479/how-to-get-the-font-pixel-height-using-pil-imagefont
            (width, baseline), (offset_x, offset_y) = font.font.getsize(char)
            ascent, descent = font.getmetrics()
            textwidth, textheight = font.getsize(char)
            box = font.getmask(char).getbbox()
            img = Image.new("RGBA", (textwidth, (ascent + descent)), (255,255,255))
            d = ImageDraw.Draw(img)
            d.text((-offset_x, 0),char,(0,0,0),font=font)

            # Resize this image in 64*64 while keeping proportion
            new_img = Image.new("RGBA", (CHAR_SIZE,CHAR_SIZE), "white")
            width, height = img.size
            if width != 0 and height != 0:
                if width >= height:
                    new_height = int(CHAR_SIZE * height / width)
                    if new_height != 0:
                        img = img.resize((CHAR_SIZE,new_height), Image.ANTIALIAS)
                        new_img.paste(img,(0,int((CHAR_SIZE-new_height)/2)))
                        # Paste it in the image with all the characters
                        image_all.paste(new_img, (CHAR_SIZE*offset, 0))
                else:
                    new_width = int(CHAR_SIZE * width / height)
                    if new_width != 0:
                        img = img.resize((new_width,CHAR_SIZE), Image.ANTIALIAS)
                        new_img.paste(img,(int((CHAR_SIZE-new_width)/2),0))
                        # Paste it in the image with all the characters
                        image_all.paste(new_img, (CHAR_SIZE*offset, 0))
            offset = offset + 1

        image_all.save(out_path + font_name + ".0.0.png")

if __name__ == "__main__":
    main(sys.argv)
