import keras
import tensorflow as tf
import numpy as np

from keras.layers import Dense

MAX_STRING_LENGTH=100

track_name = keras.Input(shape=(MAX_STRING_LENGTH, ))
track_artists = keras.Input(shape=(MAX_STRING_LENGTH, ))
track_album_name = keras.Input(shape=(MAX_STRING_LENGTH, ))

features = keras.layers.Concatenate()([track_name, track_artists, track_album_name])

features = Dense(128, activation='relu')(features)
features = Dense(64, activation='relu')(features)
features = Dense(32, activation='relu')(features)

rating = Dense(5, activation='softmax')(features)

model = keras.Model(inputs=[track_name, track_album_name, track_artists])

print(model.summary())