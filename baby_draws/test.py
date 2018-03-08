import sys
sys.path.append('scripts/')

from label_image import *
label_file = "tf_files/retrained_labels.txt"
labels = load_labels(label_file)

while True:
	index = np.random.randint(0,11)
	print("You need to draw a ",labels[index])

	img = input('Enter your image name: ')
	
	most, second = run_disc(img)
	print('The most likely ', most, ' and the second ',second) 
