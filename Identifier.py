import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import numpy as np
import os

model_path = "breed_model.h5"  # full model saved here
class_names_file = "class_names.txt"
img_size = (128, 128)
batch_size = 32


def predict(img_path):
    if not os.path.exists(model_path):
        return("❌ Something wen wrong")
        

    # Load full model
    model = load_model(model_path)

    # Load class names
    if os.path.exists(class_names_file):
        with open(class_names_file, "r") as f:
            class_names = f.read().splitlines()
    else:
        return("❌ class_names.txt not found. Train at least once.")
        

    if os.path.exists(img_path):
        img = image.load_img(img_path, target_size=img_size)
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0

        prediction = model.predict(img_array)
        breed_index = np.argmax(prediction)

        return(class_names[breed_index])
    else:
        return("❌ Image not found at given path!")
