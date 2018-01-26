#!/usr/bin/env sh
# Compute the mean image from the imagenet training lmdb

EXAMPLE=data/train
DATA=data/train
TOOLS=build/tools

echo "Start..."
$TOOLS/compute_image_mean $EXAMPLE/training_set_lmdb \
	$DATA/mean_training_image.binaryproto

echo "Done."
