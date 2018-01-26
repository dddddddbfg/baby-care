# Generate the LMDB training set

## Intro
This is the training model of the emotion detection caffenet.

## Requirements

 - Python = 3.6
 - Caffe
 - openCV

## Description

### Some directories
- train_set: the training set, about 150 pictures.This is the raw data, and we need to transfer it to lmdb format
- val_set: the validation set,about 60 pictures
- trainging_set_lmdb: the training set which has been transfered to the lmdb format, and can be used for the caffe model
- validation_set_lmdb: the validation set which are used for the caffe model to validation
