from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import sys
import time

import numpy as np
import tensorflow as tf
# import cv2 as cv

from label_image import *

label_file = "tf_files/retrained_labels.txt"
labels = load_labels(label_file)

while True:
	index = np.random.randint(0,11)
	print("You need to draw a ",labels[index])

	img = raw_input('Enter your image name: ')
	
	most, second = run_disc(img)
	print('The most likely ', most, ' and the second ',second) 
