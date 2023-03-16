import idx2numpy

# Load test set
data_path = "Dataset/EMNIST"
x_test = idx2numpy.convert_from_file(f"{data_path}/emnist-byclass-test-images-idx3-ubyte")
y_tset = idx2numpy.convert_from_file(f"{data_path}/emnist-byclass-test-labels-idx1-ubyte")

# test
import tensorflow as tf

unixTime = 1678990242
model = tf.keras.models.load_model(f"Models/{unixTime}/model.meow")

## Normalize image data
x_test = tf.keras.utils.normalize(x_test, axis = 1)

loss, accuracy = model.evaluate(x_test, y_tset, batch_size = 16)

print('Loss : ', loss)
print('Accuracy', accuracy)