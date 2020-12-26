import settings
from keras.models import model_from_json
from pathlib import Path
from keras.preprocessing import image
import numpy as np
from keras.applications import vgg16
import pandas as pd

labels = [ "Dog", "Horse",  "Elephant", "Butterfly", "Chicken", "Cat", "Cow", "Sheep",  "Squirrel", "Spider"]

IMG_WIDTH, IMG_HEIGHT = 224, 224


def scanpicture(filepath, version):
    model = ""
    weights = ""
    if version == "vgg":
        model = "resources/model.json"
        weights = "resources/weights.h5"
    elif version == "manual":
        model = "resources/manual_model.json"
        weights = "resources/manual_weights.h5"
    # Load the json file that contains the model's structure
    f = Path(settings.FILEPATH + model)
    model_structure = f.read_text()

    # Recreate the Keras model object from the json data
    model = model_from_json(model_structure)

    # Re-load the model's trained weights
    model.load_weights(settings.FILEPATH + weights)

    # Load an image file to test, resizing it to 224x224 pixels (as required by this model)
    img = image.load_img(filepath, target_size=(IMG_WIDTH, IMG_HEIGHT))

    # Convert the image to array with 3 color channels normalized
    image_array = image.img_to_array(img) / 255

    # Add a fourth dimension to the image (since Keras expects a list of images, not a single image)
    images = np.expand_dims(image_array, axis=0)

    # Make a prediction using the model
    results = model.predict(images)

    results_with_id = []

    for id, percentage in enumerate(results[0]):
        results_with_id.append([id, percentage])

    def sortByPercentage(val):
        return val[1]

    results_with_id.sort(reverse=True, key=sortByPercentage)

    data_tuples = list(zip(labels,results[0]))
    df = pd.DataFrame(data_tuples, columns=['AnimalName','Percentage'])
    #Convert from normalized data to 100% by multiplying
    df["Percentage"] = 100 * df["Percentage"]

    return (labels[results_with_id[0][0]], df)

