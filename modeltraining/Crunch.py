import os
import matplotlib.pyplot as plt
from pathlib import Path
from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, Flatten
from keras.applications import vgg16
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import optimizers

#New approach. - # https://www.kaggle.com/alessiocorrado99/animals10 <- Animals download images to run this file.
#Global values
from sklearn.model_selection import train_test_split

IMG_WIDTH, IMG_HEIGHT = 224, 224
BATCH_SIZE = 32

# Path to folders with training data
# current working directory from which main.py is located
cur_dir = os.getcwd()
raw_image_path = os.path.join(cur_dir, 'my_resources/raw-img/')

# Create generator to load dataset

# Perform VGG preprocessing : Normalize and mean-shift.
# Normalize image data to 0-to-1 range - rescale
datagen = ImageDataGenerator(
    rescale=1./255,
    samplewise_center=True,
    validation_split=0.3
)

#Split the data into train and test
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
    optimizer = optimizers.SGD(lr=1e-3, momentum=0.9),
    metrics=['accuracy']
)







# Model summary
model.summary()




#Train the model
#https://www.tensorflow.org/api_docs/python/tf/data/Dataset
history = model.fit(
    train_data,
    epochs=10,
    batch_size=BATCH_SIZE,
    validation_data=test_data,
    shuffle=True
)











#Plot the model accuracy
plt.plot(history.history["accuracy"])
plt.plot(history.history["val_accuracy"])
plt.title("Model Acc.")
plt.xlabel("epochs")
plt.ylabel("Acc.")
plt.legend(["Train", "Test"])
plt.show()








# Save neural network structure - Then we can use it later.
model_structure = model.to_json()
f = Path("./my_resources/model_structure_animal10.json")
f.write_text(model_structure)
model.save_weights("./my_resources/model_weights_animal10.h5")

