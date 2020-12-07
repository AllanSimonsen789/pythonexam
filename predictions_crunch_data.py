import os
from keras.models import model_from_json
from pathlib import Path
from keras.preprocessing import image
import numpy as np
from keras.applications import vgg16

IMG_WIDTH, IMG_HEIGHT = 224, 224

# Making predictions - with our trained neural network.
cur_dir = os.getcwd()
data_dir = os.path.join(cur_dir, 'my_resources/raw-img/')
animal_labels = os.listdir(data_dir)
translate = {"cane": "dog", "cavallo": "horse", "elefante": "elephant", "farfalla": "butterfly", "gallina": "chicken", "gatto": "cat", "mucca": "cow", "pecora": "sheep", "scoiattolo": "squirrel", "ragno":"spider"}

# Load the json file that contains the model's structure
f = Path("./my_resources/model_structure_animal10.json")
model_structure = f.read_text()

# Recreate the Keras model object from the json data
model = model_from_json(model_structure)

# Re-load the model's trained weights
model.load_weights("./my_resources/model_weights_animal10.h5")

# Load an image file to test, resizing it to 224x224 pixels (as required by this model)
img = image.load_img("./my_resources/horse_disguised.jpg", target_size=(IMG_WIDTH, IMG_HEIGHT))

# Convert the image to a numpy array
image_array = image.img_to_array(img) / 255

# Add a fourth dimension to the image (since Keras expects a list of images, not a single image)
images = np.expand_dims(image_array, axis=0)

# Make a prediction using the model
results = model.predict(images)

for id, percentage in enumerate(results[0]):
    print(translate[animal_labels[id]], f'{(percentage * 100):.2f}')#To get % times 100

