import os
import sys
import glob
from PIL import Image
import itertools

size = (64,64)

def main(argv):
    usage = 'python png2train.py [PNG file]'

    if len(sys.argv) != 2:
        print(usage)
        sys.exit()

    png_file = argv[1]
    dataset_path = os.path.splitext(png_file)[0]+"/"
    if not os.path.exists(dataset_path):
        print ("create ", dataset_path)
        os.mkdir(dataset_path)
    if not os.path.exists(os.path.join(dataset_path, 'A/')):
        print ("create ", os.path.join(dataset_path, 'A/'))
        os.mkdir(os.path.join(dataset_path, 'A/'))
    if not os.path.exists(os.path.join(dataset_path, 'B/')):
        print ("create ", os.path.join(dataset_path, 'B/'))
        os.mkdir(os.path.join(dataset_path, 'B/'))
    if not os.path.exists(os.path.join(dataset_path, 'A/train/')):
        print ("create ", os.path.join(dataset_path, 'A/train/'))
        os.mkdir(os.path.join(dataset_path, 'A/train/'))
    if not os.path.exists(os.path.join(dataset_path, 'A/test/')):
        print ("create ", os.path.join(dataset_path, 'A/test/'))
        os.mkdir(os.path.join(dataset_path, 'A/test'))
    if not os.path.exists(os.path.join(dataset_path, 'B/train/')):
        print ("create ", os.path.join(dataset_path, 'B/train/'))
        os.mkdir(os.path.join(dataset_path, 'B/train/'))
    if not os.path.exists(os.path.join(dataset_path, 'B/test/')):
        print ("create ", os.path.join(dataset_path, 'B/test/'))
        os.mkdir(os.path.join(dataset_path, 'B/test/'))

    font_img = Image.open(png_file)
    font_img.save(os.path.join(dataset_path, 'A/test/' + png_file))
    font_img.save(os.path.join(dataset_path, 'B/test/' + png_file))

    width, height = font_img.size
    index_max = int(width/64)

    mask = Image.new("RGBA", (64, 64), "white")

    for index in range(0,index_max):
        crop = (index*64,0,(index+1)*64,64)
        cropped_img = font_img.crop(crop)
        extrema = cropped_img.convert("L").getextrema()
        if extrema != (255, 255):
            cropped_img.save(os.path.join(dataset_path, 'B/train/' + os.path.splitext(png_file)[0] + "_" + str(index) + ".png"))
            tmp_img = font_img.copy()
            tmp_img.paste(mask,(index*64,0))
            tmp_img.save(os.path.join(dataset_path, 'A/train/' + os.path.splitext(png_file)[0] + "_" + str(index) + ".png"))


if __name__ == '__main__':
    main(sys.argv)
