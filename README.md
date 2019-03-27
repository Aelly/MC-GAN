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
```

## Installation

Clone this repo in a separate folder (will be needed later to add the dataset)

```
mkdir FontTransfer
cd FontTransfer
git clone https://github.com/Aelly/MC-GAN
cd MC-GAN
```

## How to use

- (Optional) Download our model
```
./download/download_model.sh
```

### Train your own model

- (Optional) You can download our fonts database (4 600 files) with:
```
./download/download_fonts.sh
```

- Create the images that will be used to train the network:
To train the network you can create images from font file (.ttf or .otf) with
```
python font2png.py [dir with font file] [output dir]
```

- Create the dataset that will be use to train the networkd:
The following script will divide the images into multiple folder and create a dictionary needed by the network. In order to create the correct training dataset you need to have the Code-New-Roman image. This font cas be found in the test/test-font directory.
```
python png2pretrain.py [dir with png file] [output dir]
```

- Train Glyph Network:
```
./scripts/train_cGan.sh [datasetName] [output dir]
```
### Complete a font

- Extract the font from DocCreator
```
cd ExtractImagesFromOF
make
./ExtractImagesFromOF [of file] [output dir]
```

- Create the image containing all the known characters 
```
python chars2png.py [dir with png files]
```

- Create the training dataset
```
python png2train.py [png file]
```

- Train the full model
```
./scripts/train_StackGAN.sh [datasetName] [model dir]
```

- Complete the image
```
./scripts/test_StackGAN [datasetName] [model dir]
```

- Create the completed of file
```

```
## Changing dataset format

In this fork we are generating 114 characters, in order to change that number you need to :
- Modify the list of characters to extract in font2png.py line 13
- In each file in the scripts directory change the variables IN_NC, O_NC and GRP to the number you want

