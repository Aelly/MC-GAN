# PFE - MC-GAN

This is a fork of azadis MC-GAN realised for a school project. It's primary objectif is to 
be able to complete fonts extract from a Labri's software: "DocCreator". This project can also 
be use to easily train a new model and complete image containing characters not processed by the 
original repo.

# Getting Started

## Prerequisites

```
Linux or macOS
Python 2.7

PyTorch
visdom
dominate
scikit-image
Pillow
numpy
glob2
tqdm
```

## Installation

Clone this repo in a separate folder

```
mkdir FontTransfer
cd FontTransfer
mkdir datasets
git clone https://github.com/Aelly/MC-GAN
cd MC-GAN
```

## How to use

- (Optional) Download our model (first version)  
http://www.mediafire.com/file/03bsjb5u8au95uh/200_net_G.pth/file
http://www.mediafire.com/file/zo7srld08tuol5q/200_net_G_3d.pth/file

### Train your own model

- (Optional) You can download our fonts database (4 600 files) at this link:
http://www.mediafire.com/file/b5cfkh8wxvhwdxh/font.zip/file

- Create the images that will be used to train the network:
To train the network you can create images from font file (.ttf or .otf) with
```
python process/font2png.py [dir with font file] [output dir]
```

- Create the dataset that will be use to train the network :
The following script will divide the images into multiple folder and create a dictionary needed by the network. In order to create the correct training dataset you need to have the Code-New-Roman image. This font can be found in our dataset or in the test/test-font directory.
```
python process/png2pretrain.py [dir with png file] [output dir]
```
The resulting directory must be placed in the datasets directory (which was created before cloning).

- Train Glyph Network:
```
./scripts/train_cGan.sh [datasetName] [output dir]
```
[datasetName] is the name of the directory you created in the previous step.

### Complete a font

- Extract the font from DocCreator
```
cd ExtractImagesFromOF
make
./ExtractImagesFromOF [.of file] [output dir]
```

- Create the image containing all the known characters 
```
python process/chars2png.py [dir with png files]
```
[dir with png files] is the output directory from the previous step.

- Create the training dataset
```
python process/png2train.py [png file]
```
[png file] is the image produced by the previous step, named the same as the directory.
The resulting directory must be placed in the datasets directory.

- Train the full model
```
./scripts/train_StackGAN.sh [datasetName] [model dir]
```
[datasetName] is the name of the directory you just placed in the datasets folder.
[model dir] is the name of the pretrained model (same as [output dir] from the train_cGan step)

- Complete the image
```
./scripts/test_StackGAN [datasetName] [model dir]
```
[datasetName] is the same name as the previous step. It's used to load the previously trained model.
[model dir] is the name of the pretrained model (same as [output dir] from the train_cGan step)

- Create the completed of file
```

```
## Changing training settings
 
It's possible to change the parameters of the network, you can do so for each file in the scripts directory :
- BATCHSIZE is the number of images you process at once, the current number fit on a 8Gb GPU but if you can you should increase it
- NITER is the number of epoch you do before reducing the learning rate
- NITER_D is the number of epoch you do after reducing the learning rate
- LOADSIZE and FINESIZE are the size of each letter you process and produce, only 48x48 images fit on a 8Gb GPU but if you can you should increase it to 64x64

## Changing dataset format

In this fork we are generating 114 characters, in order to change that number you need to :
- Modify the list of characters to extract in the process/chars.json
- In each file in the scripts directory change the variables IN_NC, O_NC and GRP to the number of characters you want

## Test the process programs

To test our process scripts, you can go in the test directory and execute the main_test.sh script.
You will find in the Procedure folder explanation for each test and the expected behaviour.
To reset the directory you can execute the clean.sh script.
