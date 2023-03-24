'''
Script to export a normalized and resized version of the dataset.
Because colab is big dum dum when it comes to memory management.
'''

import idx2numpy
import numpy as np

data_path = "Dataset/EMNIST"

# Load training data
x_data = idx2numpy.convert_from_file(f"{data_path}/emnist-byclass-train-images-idx3-ubyte")

# Change res because resnet needs 32x32
import cv2

x_data = np.array([cv2.resize(image, (32, 32), interpolation= cv2.INTER_LANCZOS4) for image in x_data], dtype= np.float32)
x_data = np.expand_dims(x_data, axis= -1)
x_data /= 255.0
print(x_data.shape)

import pickle

with open(f"{data_path}/emnist-byclass-train-images-idx3-ubyte-resize-32x", 'wb') as f :
    pickle.dump(x_data, f)