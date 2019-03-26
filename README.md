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

```

### Train your own model

- Create the images that will be used to train the network:
To train the network you can create images from font file (.ttf or .otf) with
```
python font2png.py [dir with font file] [output dir]
```
You need to first create the output dir that will contain the png files.

- Create the dataset that will be use to train the networkd:
The following script will divide the images into multiple folder and create a dictionary needed by the network.
```
python png2pretrain.py [dir with png file] [output dir] [nb char]
```
"nb char" is the number of char that the network need to be able to generate (without change in the previous step it's 114)

- Train Glyph Network:
```
./scripts/train_cGan.sh [datasetName]

```
### Complete a font
