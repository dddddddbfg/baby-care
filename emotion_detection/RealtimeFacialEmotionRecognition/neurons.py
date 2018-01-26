#!/usr/bin/env python

import caffe
import numpy as np

from caffe_functions import *
from opencv_functions import *
from utility_functions import *

dir = 'datasets/validation_images/'
img1 = caffe.io.load_image(dir + 'Y1.HA.jpg')
img2 = caffe.io.load_image(dir + 'Y2.SU.jpg')
img3 = caffe.io.load_image(dir + 'Y3.SU.jpg')
#imgList = [img1, img2, img3]
imgList = [img1]

# Master list of categories for EmotitW network
categories = [ 'Angry' , 'Disgust' , 'Fear' , 'Happy'  , 'Neutral' ,  'Sad' , 'Surprise']

#mean = loadMeanCaffeImage()
VGG_S_Net = make_net(net_dir='Custom_Model')
#layers = ['conv1', 'fc7']
layers = ['conv1','conv2', 'conv3','conv4','conv5','fc6','fc7']

fc = []
n = 0
for img in imgList:
    pred = VGG_S_Net.predict([img], oversample=False)
    print(categories[pred.argmax()])
    for layer in layers:
        plt.figure(n)
        feat = VGG_S_Net.blobs[layer].data[0]
        if layer[0] == 'c': # convolutional layer
            vis_square(feat)
        else: # fully connected
            fc.append(feat.copy())
            plt.imshow(feat.reshape((88,-1)))
        plt.axis('off')
        n += 1
    n += 10

# Computes the cosine similarity between two vectors
def cos_sim(a, b):
    return np.inner(a,b)/(np.linalg.norm(a)*np.linalg.norm(b))

#print('Person Similarity', cos_sim(fc[0], fc[1]))
#print('Emotion Similarity', cos_sim(fc[1], fc[2]))
plt.show()
