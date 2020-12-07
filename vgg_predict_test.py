from keras.preprocessing import image
import numpy as np
from keras.applications import vgg16
from vgg_labels import translate

IMG_WIDTH, IMG_HEIGHT = 224, 224

# Load an image file to test, resizing it to 224x224 pixels (as required by this model)
img = image.load_img("./my_resources/acorn.png", target_size=(IMG_WIDTH, IMG_HEIGHT))

# Convert the image to a numpy array
image_array = image.img_to_array(img)

# Add a forth dimension to the image (since Keras expects a bunch of images, not a single image)
images = np.expand_dims(image_array, axis=0)

# Normalize the data
images = vgg16.preprocess_input(images)

# Use the pre-trained neural network to extract features from our test image (the same way we did to train the model)
feature_extraction_model = vgg16.VGG16(
    weights='imagenet',
    include_top=True,
    input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
)
results = feature_extraction_model.predict(images)

# Print the result
results_with_id = []

for id, percentage in enumerate(results[0]):
    results_with_id.append([id, percentage])

def sortByPercentage(val):
    return val[1]

results_with_id.sort(reverse=True, key=sortByPercentage)

for element in results_with_id[:10]:
    print(translate[element[0]], f'{(element[1] * 100):.2f}')


