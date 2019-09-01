import os
import keras
from PIL import Image
import numpy as np
from keras import layers, models, backend


APP_DIR = os.path.dirname(os.path.abspath(__file__))
H5_PATH = os.path.join(APP_DIR, 'ocr.h5')

data_index = [(290, 25, 315, 50), (310, 25, 335, 50), (350, 25, 375, 50),
              (713, 25, 735, 60), (735, 25, 757, 60), (755, 25, 780, 60),
              (590, 60, 611, 90), (610, 60, 635, 90), (270, 60, 295, 85),
              (290, 58, 315, 85)]


def predict(image):
    target = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    model = models.Sequential()
    model.add(layers.Conv2D(6, kernel_size=(5, 5), activation='relu', input_shape=(28, 28, 1)))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))
    model.add(layers.Conv2D(16, kernel_size=(5, 5), activation='relu'))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))
    model.add(layers.Flatten())
    model.add(layers.Dense(120, activation='relu'))
    model.add(layers.Dense(84, activation='relu'))
    model.add(layers.Dense(10, activation='softmax'))
    model.compile(loss=keras.metrics.categorical_crossentropy, optimizer=keras.optimizers.Adam(), metrics=['accuracy'])
    model.load_weights(H5_PATH)
    classes = model.predict_classes(image)[0]
    backend.clear_session()
    return target[classes]


def ocr(image):
    pic = Image.open(image).convert("1")
    number_list = []
    for i in range(10):
        number = pic.crop(data_index[i])
        number = number.resize((28, 28), Image.BILINEAR)
        number = np.array(number)
        number = number.astype('float32') / 255
        number = number.reshape(1, 28, 28, 1)
        number = predict(number)
        number_list.append(number)
    liquid_level = number_list[0]+number_list[1]+number_list[2]
    temperature = number_list[3]+number_list[4]+number_list[5]
    high_set = number_list[6]+number_list[7]
    low_set = number_list[8]+number_list[9]
    return [liquid_level, temperature, high_set, low_set]
