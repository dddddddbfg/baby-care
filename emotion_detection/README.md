# Emotion Detection

## Intro
This mainly contains two parts:
- The model
  - We have the model `.prototxt` in the `models` directory.
  - We can generate the `.caffemodel` file (weights of the caffenet) by running several scripts in the `train` directory, just follow the instructions
- The RealTimeEmotionDetection
  - We already have the model struccture. so what we need is openCV and get the emotion scores and return this parameter to the user
