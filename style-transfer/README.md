# style-transfer

## Introduction

This repository contains a pyCaffe-based implementation of "A Neural Algorithm of Artistic Style" by L. Gatys, A. Ecker, and M. Bethge, which presents a method for transferring the artistic style of one input image onto another. You can read the paper here: http://arxiv.org/abs/1508.06576. 

Neural net operations are handled by Caffe, while loss minimization and other miscellaneous matrix operations are performed using numpy and scipy. L-BFGS is used for minimization.

我们承认这样一个事实：图像的艺术风格就是其基本形状与色彩的组合方式，所以通过风格与内容的结合，我们可以产生具有艺术风格的图片。

![intro](https://dn-anything-about-doc.qbox.me/document-uid440821labid3126timestamp1498730087122.png/wm)


## Plus
We are going to use the vgg16 model,and because of lack of GPU, to minimize the training time, we will iterate only 10 times which i think is almost same as the pictures iterated 100 times.

## Download

To run the code, you must have Caffe installed and the appropriate Python bindings in your `PYTHONPATH` environment variable. Detailed installation instructions for Caffe can be found [here](http://caffe.berkeleyvision.org/installation.html).

All of the necessary code is contained in the file `style.py`. You can try it on your own style and content image by running the following command:

```
python style.py -s <style_image> -c <content_image> -m <model_name> -g -1
```

The prototxts which come with the vanilla Caffe install aren't quite compatible with this code - working ones have already been added to this repository as a result of this. To get the pretrained models, simply run:

```
bash scripts/download_models.sh
```

This will grab the convnet models from the links provided in the [Caffe Model Zoo](https://github.com/BVLC/caffe/wiki/Model-Zoo). You may also specify the exact model you'd like to download by running:

```
bash scripts/download_models.sh <model_name>
```

Here, `<model_name>` must be one of `vgg16`, `vgg19`, `googlenet`, or `caffenet`.


These results can also be found in the `images` folder in the repository root.

A more in-depth set of examples can be found [here](http://frankzliu.com/artistic-style-transfer/).
