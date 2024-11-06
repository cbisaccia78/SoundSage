import keras
import tensorflow as tf
import numpy as np

from keras.layers import Dense
from ml_utils.transformations import string_to_1hot_sequence, split_vector


def create_rating_model(tracks):
    # Create dataset and labels
    track_names = []
    track_artists = []
    track_album_names = []
    track_ratings = []

    for track in tracks:
        track_names.append(track.name)
        track_artists.append(" ".join(track.artists))
        track_album_names.append(track.album_name)
        track_ratings.append(track.rating)

    track_names = np.array(track_names)
    track_artists = np.array(track_artists)
    track_album_names = np.array(track_album_names)

    track_ratings = np.array(track_ratings)

    track_names = string_to_1hot_sequence(track_names)
    track_artists = string_to_1hot_sequence(track_artists)
    track_album_names = string_to_1hot_sequence(track_album_names)

    # partition into train, validation, test

    track_names_train, track_names_valid, track_names_test = split_vector(track_names, 0.6, 0.8)
    track_artists_train, track_artists_valid, track_artists_test = split_vector(track_artists, 0.6, 0.8)
    track_album_names_train, track_album_names_valid, track_album_names_test = split_vector(track_album_names, 0.6, 0.8)
    track_ratings_train, track_ratings_valid, track_ratings_test = split_vector(track_ratings, 0.6, 0.8)


    # Create model

    track_name_layer = keras.Input(shape=track_names[0].shape)
    track_artists_layer = keras.Input(shape=track_artists[0].shape)
    track_album_name_layer = keras.Input(shape=track_album_names[0].shape)

    features = keras.layers.Concatenate()([track_name_layer, track_artists_layer, track_album_name_layer])

    features = Dense(128, activation='relu')(features)
    features = Dense(64, activation='relu')(features)
    features = Dense(32, activation='relu')(features)

    rating = Dense(5, activation='softmax')(features)

    model = keras.Model(inputs=[track_name_layer, track_album_name_layer, track_artists_layer], outputs=[rating])
    model.compile(optimizer='adam', loss=keras.losses.SparseCategoricalCrossentropy(), metrics=[keras.metrics.SparseCategoricalAccuracy()])
    
    # Fit model
    model.fit(
        x=[track_names_train, track_artists_train, track_album_names_train],
        y=[track_ratings_train],
        epochs=200,
        batch_size=2,
        validation_data=([track_names_valid, track_artists_valid, track_album_names_valid], [track_ratings_valid])
    )
    
    test_loss, test_accuracy = model.predict(
        x=[track_names_test, track_artists_test, track_album_names_test],
        y=[track_ratings_test],
    )

    print(f'test_loss: {test_loss}, test_accuracy: {test_accuracy}')
    

    return model