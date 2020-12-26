import keras
import os
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPool2D, Flatten, Dropout
from keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.optimizers import Adam
from pathlib import Path
import numpy as np

IMG_WIDTH, IMG_HEIGHT = 224, 224
BATCH_SIZE = 32

generator = ImageDataGenerator(
    rescale=1./255,
    samplewise_center=True,
    validation_split=0.15,
)

train_data = generator.flow_from_directory(
    directory="./my_resources/raw-img/",
    target_size=(IMG_WIDTH, IMG_HEIGHT),
    batch_size=BATCH_SIZE,
    subset="training",
)
test_data = generator.flow_from_directory(
    directory="./my_resources/raw-img/",
    target_size=(IMG_WIDTH, IMG_HEIGHT),
    batch_size=BATCH_SIZE,
    subset="validation",
)


model = Sequential()
model.add(Conv2D(input_shape=(IMG_WIDTH, IMG_HEIGHT, 3), filters=64,
                 kernel_size=(3, 3), padding="same", activation="relu"))
model.add(MaxPool2D(pool_size=(2, 2), strides=(2, 2)))
model.add(Conv2D(filters=128, kernel_size=(
    3, 3), padding="same", activation="relu"))
model.add(MaxPool2D(pool_size=(2, 2), strides=(2, 2)))
model.add(Conv2D(filters=256, kernel_size=(
    3, 3), padding="same", activation="relu"))
model.add(MaxPool2D(pool_size=(2, 2), strides=(2, 2)))
model.add(Conv2D(filters=512, kernel_size=(
    3, 3), padding="same", activation="relu"))
model.add(MaxPool2D(pool_size=(2, 2), strides=(2, 2)))
model.add(Conv2D(filters=1024, kernel_size=(
    3, 3), padding="same", activation="relu"))
model.add(MaxPool2D(pool_size=(2, 2), strides=(2, 2)))
model.add(Dropout(0.35))

model.add(Flatten())
model.add(Dense(units=4096, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(units=4096, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(units=10, activation='softmax'))

model.compile(
    loss=keras.losses.categorical_crossentropy,
    optimizer=Adam(lr=0.001),
    metrics=['accuracy']
)
model.summary()

# Save model structure
model_structure = model.to_json()
f = Path("./my_resources/manual_model.json")
f.write_text(model_structure)


checkpoint = ModelCheckpoint(
    "./my_resources/manual_weights.h5",
    monitor='val_accuracy',
    verbose=1,
    save_best_only=True,
    save_weights_only=False,
    mode='auto',
    period=1
)
early = EarlyStopping(
    monitor='val_accuracy',
    min_delta=0,
    patience=20,
    verbose=1,
    mode='auto'
)

hist = model.fit(
    train_data,
    validation_data=test_data,
    validation_steps=10,
    steps_per_epoch=100,
    epochs=100,
    callbacks=[checkpoint, early]
)


# Here we will visualize training/validation accuracy and loss using matplotlib.
plt.plot(hist.history["accuracy"])
plt.plot(hist.history['val_accuracy'])
plt.plot(hist.history['loss'])
plt.plot(hist.history['val_loss'])
plt.title("model accuracy")
plt.ylabel("Accuracy")
plt.xlabel("Epoch")
plt.legend(["Accuracy", "Validation Accuracy", "loss", "Validation Loss"])
plt.show()
