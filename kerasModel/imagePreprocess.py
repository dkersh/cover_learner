from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from keras.models import Sequential, load_model
from keras.callbacks import CSVLogger, ModelCheckpoint
from keras.layers import Conv2D, MaxPooling2D, GlobalAveragePooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.optimizers import SGD
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import glob
import cv2
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical

filelist = glob.glob('home/*.jpg')

def get_im(path):
	img = cv2.imread(path)
	return img

def getLabels(filelist):
	labels = []
	for item in filelist:
		labels.append(int(item[len(item)-5]))

	#one hot encode
	labels = to_categorical(labels)
	return labels

def getImages(filelist):
	images = []
	for item in filelist:
		img = get_im(item)
		img = img
		images.append(img)

	return images

labels = getLabels(filelist)
images = getImages(filelist)

#print(np.shape(images))
print(labels)

#Split the data
print('Splitting Data')
data_train, data_test, labels_train, labels_test = train_test_split(images, labels)

#Build model
model = Sequential()
model.add(Conv2D(64, (2, 3),activation='relu', input_shape=(123,98,3)))
model.add(MaxPooling2D(pool_size=(2, 2),padding='valid'))

model.add(Conv2D(128, (2, 3),activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2),padding='valid'))

model.add(Conv2D(256, (2, 3),activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2),padding='valid'))

model.add(Conv2D(256, (2, 3),activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2),padding='valid'))

model.add(Conv2D(256, (2, 3),activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2),padding='valid'))

#model.add(GlobalAveragePooling2D())

model.add(Flatten())

model.add(Dense(720, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(720, activation='relu'))
model.add(Dense(720, activation='relu'))

model.add(Dense(10, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer=SGD(lr=0.001,momentum=0.1,decay=0.0005,nesterov=True), metrics=['accuracy'])
model.summary()

#Save output to file
csv_logger = CSVLogger('training.log')
#Save best model when possible
checkpoint = ModelCheckpoint('training_model_best.hdf5', monitor='val_acc', verbose=1, save_best_only=True, mode='max')

#model = load_model('my_model.h5')

model.fit(np.array(images), np.array(labels), epochs=225, batch_size=10,
	validation_split=0.20,verbose=2,shuffle=True,callbacks=[csv_logger,checkpoint])

model.save('my_model.h5')
