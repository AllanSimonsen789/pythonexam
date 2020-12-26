import argparse
import os
from keras.models import model_from_json
from pathlib import Path
from keras.preprocessing import image
import numpy as np
from keras.applications import vgg16

IMG_WIDTH, IMG_HEIGHT = 224, 224


# Making predictions - with our trained neural network.
def translate_folder_names():
    cur_dir = os.getcwd()
    data_dir = os.path.join(cur_dir, 'my_resources/raw-img/')
    animal_labels_from_dir = os.listdir(data_dir)
    translate_italian_to_english = {"cane": "dog", "cavallo": "horse", "elefante": "elephant", "farfalla": "butterfly",
                 "gallina": "chicken", "gatto": "cat", "mucca": "cow", "pecora": "sheep", "scoiattolo": "squirrel",
                 "ragno": "spider"}
    return animal_labels_from_dir, translate_italian_to_english


# Load the json file that contains the model's structure
def load_model():
    f = Path("./my_resources/TL_model.json")
    model_structure = f.read_text()
    # Recreate the Keras model object from the json data
    loaded_model = model_from_json(model_structure)
    # Re-load the model's trained weights
    loaded_model.load_weights("./my_resources/TL_weights.h5")
    return loaded_model


# Load an image file to test, resizing it to 224x224 pixels (as required by this model)
def prepare_image(image_path):
    img = image.load_img(image_path, target_size=(IMG_WIDTH, IMG_HEIGHT))
    # Convert the image to a numpy array
    image_array = image.img_to_array(img) / 255
    # Add a fourth dimension to the image (since Keras expects a list of images, not a single image)
    images = np.expand_dims(image_array, axis=0)
    return images


def predict_image(model_predict, image_predict, translate_dict, animal_labels):
    # Make a prediction using the model
    results = model_predict.predict(image_predict)

    for id, percentage in enumerate(results[0]):
        print(translate_dict[animal_labels[id]], f'{(percentage * 100):.2f}')  # To get % times 100


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="A program that tries to predicts, what is on a provided image, "
                    "based on the transferlearnings data.")
    # Input argument.
    parser.add_argument('Predict_image', help='Path of image to predict.')
    args = parser.parse_args()

    if args.Predict_image is None:
        print("Please submit a image path")
    else:
        print("\n\n\nLoading images from directory.")
        animal_labels, translate = translate_folder_names()
        print("\n\n\nLoad model from trained data.")
        model = load_model()
        print("\n\n\nPrepare image.")
        prepared_image = prepare_image(args.Predict_image)
        print("\n\n\nMake the prediction of the image.")
        predict_image(model, prepared_image, translate, animal_labels)
