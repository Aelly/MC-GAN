import os
import sys
import glob
from PIL import Image
import itertools
from tqdm import tqdm

CHAR_SIZE = 64

def main(argv):
    usage = 'Usage : python png2train.py [PNG file]'

    if len(sys.argv) != 2:
        print(usage)
        sys.exit()

    png_path = argv[1]
    png_file = os.path.basename(png_path)

    if not png_path.endswith(".png"):
        print("'" + png_file + "' is not a png")
        print(usage)
        sys.exit()

    try:
        font_img = Image.open(png_path)
    except IOError:
        print("'" + png_file + "' is not a valid image")
        print(usage)
        sys.exit()
    
    # Create tree view for Full training model
    dataset_path = os.path.splitext(png_file)[0]+"/"
    if not os.path.exists(dataset_path):
        print ("Create " + dataset_path)
        os.mkdir(dataset_path)
    if not os.path.exists(os.path.join(dataset_path, 'A/')):
        print ("Create " + os.path.join(dataset_path, 'A/'))
        os.mkdir(os.path.join(dataset_path, 'A/'))
    if not os.path.exists(os.path.join(dataset_path, 'B/')):
        print ("Create " + os.path.join(dataset_path, 'B/'))
        os.mkdir(os.path.join(dataset_path, 'B/'))
    if not os.path.exists(os.path.join(dataset_path, 'A/train/')):
        print ("Create " + os.path.join(dataset_path, 'A/train/'))
        os.mkdir(os.path.join(dataset_path, 'A/train/'))
    if not os.path.exists(os.path.join(dataset_path, 'A/test/')):
        print ("Create " + os.path.join(dataset_path, 'A/test/'))
        os.mkdir(os.path.join(dataset_path, 'A/test'))
    if not os.path.exists(os.path.join(dataset_path, 'B/train/')):
        print ("Create " + os.path.join(dataset_path, 'B/train/'))
        os.mkdir(os.path.join(dataset_path, 'B/train/'))
    if not os.path.exists(os.path.join(dataset_path, 'B/test/')):
        print ("Create " + os.path.join(dataset_path, 'B/test/'))
        os.mkdir(os.path.join(dataset_path, 'B/test/'))

    font_img.save(os.path.join(dataset_path, 'A/test/' + png_file))
    font_img.save(os.path.join(dataset_path, 'B/test/' + png_file))

    width, height = font_img.size
    index_max = int(width/CHAR_SIZE)

    mask = Image.new("RGBA", (CHAR_SIZE, CHAR_SIZE), "white")

    # Create Images for each characters (TQDM is our progression bar)
    for index in tqdm(range(0,index_max)):
        crop = (index*CHAR_SIZE,0,(index+1)*CHAR_SIZE, CHAR_SIZE)
        cropped_img = font_img.crop(crop)
        extrema = cropped_img.convert("L").getextrema()
        # Check if the char exists (not blank)
        if extrema != (255, 255):
            # Save image with only one characters
            cropped_img.save(os.path.join(dataset_path, 'B/train/' + os.path.splitext(png_file)[0] + "_" + str(index) + ".png"))
            tmp_img = font_img.copy()
            tmp_img.paste(mask,(index*CHAR_SIZE,0))
            # Save image with all the characters except one
            tmp_img.save(os.path.join(dataset_path, 'A/train/' + os.path.splitext(png_file)[0] + "_" + str(index) + ".png"))


if __name__ == '__main__':
    main(sys.argv)
