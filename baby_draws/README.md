# BABY_DRAWS

## Introduction
This is a retrained CNN which can be used to classify the specified pictures like: cat tornado apple and so on.

## Dependencies

Python 2.7

[TensorFlow 1.0](https://www.tensorflow.org/)

[GoogleCodeLabs](https://github.com/googlecodelabs/tensorflow-for-poets-2)

## Description

`xxx.jpg`: This is the standard input image. Other image formats like `bmp` are also avaliable.

`scripts`: This will be some scripts you can use.

`tf_files`: This contains the dataset and the model parameter.

## How-To-Test
You can run such command to test: 

	cd baby_draws

	python scripts/draw_game.py

You will need to input the image name `xxx.jpg` and the terminal will output the result.

	Evaluation time (1-image): 0.321s

	apple 0.727916
	banana 0.141106
	cloud 0.0667175
	marker 0.0272462
	car 0.0224238
	The most likely  apple  and the second  banana

## Use the script
You will need the `run_disc` in `scripts/label_image.py `.

This will return the `most-likely category` and the `second-likely category` in the tuple format.

## How-To get the dataset and train

This time our team just use the 简笔画 pictures and contains just about 10 categroies. Later you find the dataset in Baidu Cloud.