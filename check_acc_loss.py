import idx2numpy

# Load test set
data_path = "Dataset/EMNIST"
x_test = idx2numpy.convert_from_file(f"{data_path}/emnist-byclass-test-images-idx3-ubyte")
y_test = idx2numpy.convert_from_file(f"{data_path}/emnist-byclass-test-labels-idx1-ubyte")

## Reshape for Model 2
x_test = x_test.reshape(x_test.shape[0], x_test.shape[1], x_test.shape[2], 1)

# test
import tensorflow as tf

## Normalize image data
x_test = tf.keras.utils.normalize(x_test, axis = 1)

# Load model
unixTime = 1679378923
model = tf.keras.models.load_model(f"Models/{unixTime}/cp.meow")

# Evaluate with test set
loss, accuracy = model.evaluate(x_test, y_test, batch_size = 200)

print('Loss : ', loss)
print('Accuracy', accuracy)