from keras.models import load_model
import numpy as np
import cv2
import os
import tensorflow as tf
import sys

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

model = load_model('training_model_best.hdf5')

def get_im(path):
	img = cv2.imread(path)
	return np.array(img)

imgfile = '/home/xendev/david_stuff/ImageClassification/images_new/' + sys.argv[1]

data = get_im(imgfile)
data = np.expand_dims(data,axis=0)

print(np.shape(data))

prediction = model.predict(data)

print(np.around(prediction,decimals=2))
print('Actual Score = ' + imgfile[len(imgfile)-5:len(imgfile)-4])
print('Predicted Score = ' + str(np.argmax(prediction)))