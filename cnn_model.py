# -*- coding: utf-8 -*-
"""CNN_Model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MSiRehhPexgFjFRXSegImT1AZ50Rz9C0
"""

from tensorflow import keras
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout
from keras.layers import Conv1D, MaxPooling1D, Dense, Flatten, Dropout
 
from tensorflow.keras.optimizers import Adam
from keras.callbacks import TensorBoard

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import accuracy_score
from keras.utils import np_utils
import itertools

from google.colab import drive
drive.mount('/content/drive')

#For train split
y_train = []

# For John
for i in range(1, 4):
  y_train.append(0)

# For Morgan
for i in range(1, 4):
  y_train.append(1)

# For Reeves
for i in range(1, 4):
  y_train.append(2)

# For Rock
for i in range(1, 4):
  y_train.append(3)

y_train = np.array(y_train)
y_train

#For test split
y_test = []

# For John
for i in range(1, 2):
  y_test.append(0)

# For Morgan
for i in range(1, 2):
  y_test.append(1)

# For Reeves
for i in range(1, 2):
  y_test.append(2)

# For Rock
for i in range(1, 2):
  y_test.append(3)

y_test = np.array(y_test)
y_test

#Read all Image
import glob
import cv2

x_train = []
x_test = []

for image in glob.glob('/content/drive/MyDrive/Colab Notebooks/Face_Recognition/Train/*.jpg'):
  cv_img = cv2.imread(image)
  x_train.append(cv_img)

for image2 in glob.glob('/content/drive/MyDrive/Colab Notebooks/Face_Recognition/Test/*.jpg'):
  cv_img2 = cv2.imread(image2)
  x_test.append(cv_img2)

fileName = '/content/Facial1.npz'
np.savez(fileName, trainX = x_train, trainY = y_train, testX = x_test, testY = y_test)

!pip install numpy==1.16.1
import numpy as np

from numpy import load

data = load('/content/Facial1.npz')
lst = data.files
for item in lst:
    print(item)
    print(data[item])

#load dataset
data = np.load('/content/Facial1.npz') 

# load the "Train Images"
x_train = data['trainX']
#normalize every image
#x_train = np.array(x_train,dtype='float32')/255

x_test = data['testX']
#x_test = np.array(x_test,dtype='float32')/255

# load the Label of Images
y_train= data['trainY']
y_test= data['testY']

# show the train and test Data format
print('x_train : {}'.format(x_train[:]))
print('Y-train shape: {}'.format(y_train))
print('x_test shape: {}'.format(x_test.shape))

x_train.shape

x_train, x_valid, y_train, y_valid= train_test_split(
    x_train, y_train, test_size=.05, random_state=1234,)

print(x_train.shape)

im_rows=1
im_cols=1
batch_size=2
im_shape=(im_rows, im_cols, 1)

#change the size of images
x_train = x_train.reshape(x_train.shape[0], *im_shape)
x_test = x_test.reshape(x_test.shape[0], *im_shape)
x_valid = x_valid.reshape(x_valid.shape[0], *im_shape)

print('x_train shape: {}'.format(y_train.shape[0]))
print('x_test shape: {}'.format(y_test.shape))

#filters= the depth of output image or kernels
#from keras import backend as  K
#backend.set_image_data_format('channels_first')
cnn_model= Sequential([
    Conv2D(filters=36, kernel_size=7, activation='relu', padding='same', input_shape= im_shape),
    MaxPooling2D(pool_size=2),
    Conv2D(filters=54, kernel_size=5, activation='relu', padding='same', input_shape= im_shape),
    MaxPooling2D(pool_size=2),
    Flatten(),
    Dense(2024, activation='relu'),
     Dropout(0.5),
    Dense(1024, activation='relu'),
    Dropout(0.5),
    Dense(512, activation='relu'),
    Dropout(0.5),
    #20 is the number of outputs
    Dense(20, activation='softmax')  
])

cnn_model.compile(
    loss='sparse_categorical_crossentropy',#'categorical_crossentropy',
    optimizer=Adam(lr=0.0001),
    metrics=['accuracy']
)

cnn_model.summary()

history=cnn_model.fit(
    np.array(x_train), np.array(y_train), batch_size=512,
    epochs=25, verbose=2,
    validation_data=(np.array(x_valid),np.array(y_valid)),
)

scor = cnn_model.evaluate( np.array(x_test),  np.array(y_test), verbose=0)

print('test los {:.4f}'.format(scor[0]))
print('test acc {:.4f}'.format(scor[1]))

# list all data in history
print(history.history.keys())
# summarize history for accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

print(predicted)
print(y_test)

predicted =np.array( cnn_model.predict(x_test))
#print(predicted)
#print(y_test)
#ynew = cnn_model.predict_Classes(x_test)
predict_x=cnn_model.predict(x_test) 
classes_x=np.argmax(predict_x,axis=1)


Acc=accuracy_score(y_test, classes_x)
print("accuracy : ")
print(Acc)
#/tn, fp, fn, tp = confusion_matrix(np.array(y_test), ynew).ravel()
cnf_matrix=confusion_matrix(np.array(y_test), classes_x)

y_test1 = np_utils.to_categorical(y_test, 20)



def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        #print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    #print(cm)
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.show()


print('Confusion matrix, without normalization')
print(cnf_matrix)

plt.figure()
plot_confusion_matrix(cnf_matrix[1:10,1:10], classes=[0,1,2,3,4,5,6,7,8,9],
                      title='Confusion matrix, without normalization')

plt.figure()
plot_confusion_matrix(cnf_matrix[11:20,11:20], classes=[10,11,12,13,14,15,16,17,18,19],
                      title='Confusion matrix, without normalization')

print("Confusion matrix:\n%s" % confusion_matrix(np.array(y_test), classes_x))
print(classification_report(np.array(y_test), classes_x))

