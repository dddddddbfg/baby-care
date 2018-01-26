#!/usr/bin/env sh
# This script converts the mnist data into lmdb/leveldb format,
# depending on the value assigned to $BACKEND.
set -e

EXAMPLE=data/train
# the path  to store train.txt and val.txt
DATA=data/train
TOOLS=build/tools

BACKEND="lmdb"

# path to store train images and val images
TRAIN_DATA_ROOT=data/train/
VAL_DATA_ROOT=data/train/

echo "Creating train ${BACKEND}..."

rm -rf $EXAMPLE/training_set_lmdb
rm -rf $EXAMPLE/validation_set_lmdb

GLOG_logtostderr=1 $TOOLS/convert_imageset \
	--shuffle \
	$TRAIN_DATA_ROOT \
	$DATA/train.txt \
	$EXAMPLE/training_set_lmdb

echo "Creating val ${BACKEND}..."

# rm -rf $EXAMPLE/mnist_train_${BACKEND}
# rm -rf $EXAMPLE/mnist_test_${BACKEND}

GLOG_logtostderr=1 $TOOLS/convert_imageset \
	--shuffle \
	$VAL_DATA_ROOT \
	$DATA/val.txt \
	$EXAMPLE/validation_set_lmdb

echo "Done."
