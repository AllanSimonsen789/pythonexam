import argparse
import os
import sys
import matplotlib.pyplot as plt
from pathlib import Path
from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, Flatten
from keras.applications import vgg16
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import optimizers

# Global variables
IMG_WIDTH, IMG_HEIGHT = 224, 224
BATCH_SIZE = 32


def read_images_from_directory(directory_folder):
    # Path to folders with training data
    # current working directory from which main.py is located
    cur_dir = os.getcwd()
    raw_image_path = os.path.join(cur_dir, directory_folder)

    # Check the path exists.
    if os.path.isdir(raw_image_path):
        # Create generator to load dataset

        # Perform VGG preprocessing : Normalize and mean-shift.
        # Normalize image data to 0-to-1 range - rescale
        datagen = ImageDataGenerator(
            rescale=1. / 255,
            samplewise_center=True,
            validation_split=0.3
        )

        # Split the data into train and test
        train_data = datagen.flow_from_directory(
            raw_image_path,
            target_size=(IMG_WIDTH, IMG_HEIGHT),
            batch_size=BATCH_SIZE,
            class_mode="categorical",
            subset="training",
            seed=1
        )
        test_data = datagen.flow_from_directory(
            raw_image_path,
            target_size=(IMG_WIDTH, IMG_HEIGHT),
            batch_size=BATCH_SIZE,
            class_mode="categorical",
            subset="validation",
            seed=1
        )
        # Return a tuple with both data values.
        return train_data, test_data
    else:
        # Path didn't exist
        sys.exit("This path isn't known; " + raw_image_path)


def create_compile_run_model(train_data, test_data):
    # Load a pre-trained neural network to use as a feature extractor
    base_model = vgg16.VGG16(
        weights='imagenet',
        include_top=False,
        input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
    )

    top_model = Sequential()
    top_model.add(Flatten(input_shape=base_model.output_shape[1:]))
    top_model.add(Dropout(0.1))
    top_model.add(Dense(256, activation='relu'))
    top_model.add(Dropout(0.1))
    top_model.add(Dense(10, activation='softmax'))

    # Compile the model
    model = Model(
        inputs=base_model.input,
        outputs=top_model(base_model.output)
    )
    model.compile(
        loss='categorical_crossentropy',
        optimizer=optimizers.SGD(lr=1e-3, momentum=0.9),
        metrics=['accuracy']
    )

    # Model summary
    model.summary()

    # Train the model
    # https://www.tensorflow.org/api_docs/python/tf/data/Dataset
    history = model.fit(
        train_data,
        epochs=10,
        batch_size=BATCH_SIZE,
        validation_data=test_data,
        shuffle=True
    )
    # Return a tuple with both values.
    return history, model


def plot_model_history(history):
    # Plot the model accuracy
    plt.plot(history.history["accuracy"])
    plt.plot(history.history["val_accuracy"])
    plt.title("Model Acc.")
    plt.xlabel("epochs")
    plt.ylabel("Acc.")
    plt.legend(["Train", "Test"])
    plt.show()


def save_model_and_weights(model):
    # Save neural network structure - Then we can use it later.
    print("Saving the model structure to; '/my_resources/TL_model.json'")
    model_structure = model.to_json()
    f = Path("./my_resources/TL_model.json")
    f.write_text(model_structure)
    print("Saving the model weights to; '/my_resources/TL_weights.h5'")
    model.save_weights("./my_resources/TL_weights.h5")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="A program that loads all categorized images from a folder with subfolders, to transfer learn an "
                    "image classification model.")
    # Input argument.
    parser.add_argument('--input_folder',  # Not obligatory, also has a default, if not provided.
                        help='Name of the directory to find the files with images from.',
                        default='./my_resources/raw-img/')
    args = parser.parse_args()

    print("\n\n\nLoading images from directory.")
    train_data, test_data = read_images_from_directory(args.input_folder)  # Input_Folder
    print("\n\n\nCreate model and train data.")
    history, model = create_compile_run_model(train_data, test_data)
    print("\n\n\nPlot model graph history.")
    plot_model_history(history)
    print("\n\n\nSaving model structure and weight.")
    save_model_and_weights(model)

# Loading an image data set
# https://www.kaggle.com/alessiocorrado99/animals10
# https://www.tensorflow.org/api_docs/python/tf/keras/preprocessing/image_dataset_from_directory
