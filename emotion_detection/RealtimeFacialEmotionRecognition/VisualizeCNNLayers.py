import os, shutil, sys, time, re, glob
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
from PIL import Image
import caffe
#from win32api import GetSystemMetrics

from caffe_functions import *
from opencv_functions import *
from utility_functions import *

categories = [ 'Angry' , 'Disgust' , 'Fear' , 'Happy'  , 'Neutral' ,  'Sad' , 'Surprise']
layers = ['conv1','conv2', 'conv3','conv4','conv5','fc6','fc7']

saveDir = 'test_screenshots' # Folder to save screenshots to

useCNN = True # Set to false to simply display the default emoji
layerIndex = 0 #Index into CNN Convolution Layers Range = [0-4]

#screenWidth=GetSystemMetrics(0)
#screenHeight=GetSystemMetrics(1)

### START SCRIPT ###

# Set up face detection
faceCascades = load_cascades()

if useCNN:
	VGG_S_Net = make_net(net_dir="Custom_Model")

# Set up display window
cv.namedWindow("preview",cv.WINDOW_NORMAL)
cv.resizeWindow("preview",1600,900)

# Open input video steam
vc = cv.VideoCapture(0)

# Check that video stream is running
if vc.isOpened(): # try to get the first frame
  rval, frame = vc.read()
  #frame = frame.astype(np.float32)
else:
  rval = False

while rval:
  # Mirror image
  frame = np.fliplr(frame)
  fc = []
  pred = VGG_S_Net.predict([frame], oversample=False)
  feat = VGG_S_Net.blobs[layers[layerIndex]].data[0]

  feat = vis_square(feat)

  #Add ColorMap to HELP with VISALIZATION 
  #im_gray = cv.imread(feat, cv.IMREAD_GRAYSCALE)
  #feat = cv.applyColorMap(feat, cv.COLORMAP_JET)

  # Show video with CNN LAYER VISUAL
  cv.imshow("preview", feat)

  # Read in next frame
  rval, frame = vc.read()

  # Wait for user to press key. On ESC, close program
  key = cv.waitKey(20)
  if key == 27: # exit on ESC
    break
  elif key == 115 or key == 83: # ASCII codes for s and S
    filename = saveTestImage(img,outDir=saveDir)
    print ("Image saved to ./" + filename)
  
  #Check for CNN Layer Index Key Press
  elif key == 48:
    layerIndex = 0
  elif key == 49:
    layerIndex = 1
  elif key == 50:
    layerIndex = 2
  elif key == 51:
    layerIndex = 3
  elif key == 52:
    layerIndex = 4
  '''
  #FC LAYERS HAVE DIFFERENT NUMPY DIMENSIONS 
  elif key == 53:
    layerIndex = 5
  elif key == 54:
    layerIndex = 6
  elif key == 55:
    layerIndex = 7
  '''

cv.destroyWindow("preview")
