import os
import sys
import glob
import shutil
import random
import pickle
import numpy as np
from array import array
from decimal import Decimal
from  PIL import Image

def main(argv):
    usage = 'Usage : python png2pretrain.py [dir with png file] [output dir]'

    CHAR_SIZE = 64

    if len(argv) != 3:
        print(usage)
        sys.exit()

    png_path = argv[1]
    dataset_path = argv[2]

    # Check if input and output are dir
    if os.path.exists(dataset_path):
        if not os.path.isdir(dataset_path):
            print("output dir '" + dataset_path + "' is not a directory")
            print(usage)
            sys.exit()
    else:
        print ("Create output directory : " + dataset_path)
        os.mkdir(dataset_path)

    if not os.path.isdir(png_path):
        print('font dir is not a directory')
        print(usage)
        sys.exit()

    # Create the dir for the dataset if not already exist
    if not os.path.exists(os.path.join(dataset_path, 'BASE/')):
        print "create ", os.path.join(dataset_path, 'BASE/')
        os.mkdir(os.path.join(dataset_path, 'BASE/'))
    if not os.path.exists(os.path.join(dataset_path, 'test/')):
        print "create ", os.path.join(dataset_path, 'test/')
        os.mkdir(os.path.join(dataset_path, 'test/'))
    if not os.path.exists(os.path.join(dataset_path, 'test_dict/')):
        print "create ", os.path.join(dataset_path, 'test_dict/')
        os.mkdir(os.path.join(dataset_path, 'test_dict/'))
    if not os.path.exists(os.path.join(dataset_path, 'train/')):
        print "create ", os.path.join(dataset_path, 'train/')
        os.mkdir(os.path.join(dataset_path, 'train/'))
    if not os.path.exists(os.path.join(dataset_path, 'val/')):
        print "create ", os.path.join(dataset_path, 'val/')
        os.mkdir(os.path.join(dataset_path, 'val/'))

    # Get the number of png file in the dataset
    nb_png = len([name for name in os.listdir(png_path) if name.endswith(".png")]) - 1
    print(str(nb_png) + ' images in png dir')

    train_ratio = 0.9
    train_part = int(Decimal(train_ratio) * nb_png)
    test_part = nb_png - train_part
    val_part = int(1 * train_part / 9)
    print('Train: ' + str(train_part))
    print('Test: ' + str(test_part))
    print('Val:' + str(val_part))


    # Calculate the number of char in image (width / CHAR_SIZE)
    img = Image.open(os.path.join(png_path, "Code-New-Roman.0.0.png"))
    width, height = img.size
    nb_char = int(width / CHAR_SIZE)


    # Split the images in the dataset directory
    os.rename(os.path.join(png_path, "Code-New-Roman.0.0.png"), os.path.join(dataset_path, 'BASE/Code-New-Roman.0.0.png'))
    i = 0
    j = 0
    for png_file in glob.glob(os.path.join(png_path, '*.png')):
        fn = os.path.basename(png_file)
        if i < train_part:
            if j < val_part:
                shutil.copy2(png_file, os.path.join(dataset_path, 'val/' + fn))
                j = j + 1
            os.rename(png_file, os.path.join(dataset_path, 'train/' + fn))
        else:
            os.rename(png_file, os.path.join(dataset_path, 'test/' + fn))
        i = i + 1

    # Create the dictionary pickle
    dict = {}
    for png_font in glob.glob(os.path.join(dataset_path + 'test/', '*.png')):
        font_name = os.path.basename(png_font)
        random_array = np.array(random.sample(range(0,nb_char), nb_char))
        dict[font_name] = random_array

    pickle.dump(dict, open(os.path.join(dataset_path, 'test_dict/' + 'dict.pkl'), "wb"))

if __name__ == "__main__":
    main(sys.argv)
