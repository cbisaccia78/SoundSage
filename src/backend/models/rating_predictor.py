import keras
import tensorflow as tf
import numpy as np

from keras.layers import Dense
from ml_utils.transformations import string_to_1hot_sequence, split_vector, flatten_dict_values, normalize
from ml_utils.validation import strat_kfold
import pdb

def create_rating_model(tracks):
    ## Create dataset and labels
    track_names = []
    track_artists = []
    track_album_names = []
    track_audio_features = []
    track_audio_analysis = []
    track_ratings = []

    for track in tracks:
        track_names.append(track.name)
        track_artists.append(" ".join(track.artists))
        track_album_names.append(track.album_name)
        track_audio_features.append(track.audio_features)
        track_audio_analysis.append(track.audio_analysis)

        track_ratings.append(track.rating)

    ## data transformations
    track_names = np.array(track_names)
    track_artists = np.array(track_artists)
    track_album_names = np.array(track_album_names)
    track_ratings = np.array(track_ratings)

    # one-hot all the string data based on frequency
    track_names = string_to_1hot_sequence(track_names)
    track_artists = string_to_1hot_sequence(track_artists)
    track_album_names = string_to_1hot_sequence(track_album_names)
    # bars, beats, sections, segments, tatums all need to be padded
    # determine the maximum length of each, respectively. 
    max_bars = max_beats = max_sections = max_segments = max_tatums = 0
    for analysis in track_audio_analysis:
        bar_len = len(analysis['bars'])
        beat_len = len(analysis['beats'])
        section_len = len(analysis['sections'])
        segment_len = len(analysis['segments'])
        tatum_len = len(analysis['tatums'])

        if bar_len > max_bars:
            max_bars = bar_len
        
        if beat_len > max_beats:
            max_beats = beat_len
        
        if section_len > max_sections:
            max_sections = section_len
        
        if segment_len > max_segments:
            max_segments = segment_len
        
        if tatum_len > max_tatums:
            max_tatums = tatum_len

        # store lengths for subsequent calculation
        analysis['bar_len'] = bar_len
        analysis['beat_len'] = beat_len
        analysis['section_len'] = section_len
        analysis['segment_len'] = segment_len
        analysis['tatum_len'] = tatum_len

    # pad analysis with dummies to ensure max length, and also flatten the dict structure for future processing
    beat_dummy = bar_dummy = tatum_dummy = {'start': 0.0, 'duration': 0.0, 'confidence': 0.0}
    section_dummy = {"start": 0.0,"duration": 0.0,"confidence": 0,"loudness": 0.0,"tempo": 0.0,"tempo_confidence":0.0,"key": 0.0,"key_confidence": 0.0,"mode": -1,"mode_confidence": 0.0,"time_signature": 0,"time_signature_confidence": 0}
    segment_dummy = {"start": 0.0,"duration": 0.0,"confidence": 0.0,"loudness_start": 0.0,"loudness_max": 0.0,"loudness_max_time": 0.0,"loudness_end": 0,"pitches": [0.0, 0.0, 0.0,0.0, 0.0, 0.0,0.0, 0.0, 0.0,0.0, 0.0, 0.0],"timbre": [0.0, 0.0, 0.0,0.0, 0.0, 0.0,0.0, 0.0, 0.0,0.0, 0.0, 0.0]}
    flattened_analysis = []
    for analysis in track_audio_analysis:
        bars = analysis['bars']
        bar_len = analysis['bar_len']
        bars.extend(bar_dummy for _ in range(max_bars - bar_len))

        beats = analysis['beats']
        beat_len = analysis['beat_len']
        beats.extend([beat_dummy for _ in range(max_beats - beat_len)])

        sections = analysis['sections']
        section_len = analysis['section_len']
        sections.extend([section_dummy for _ in range(max_sections - section_len)])

        segments = analysis['segments']
        segment_len = analysis['segment_len']
        segments.extend([segment_dummy for _ in range(max_segments - segment_len)])

        tatums = analysis['tatums']
        tatum_len = analysis['tatum_len']
        tatums.extend([tatum_dummy for _ in range(max_tatums - tatum_len)])
        

        # delete un-needed field
        del analysis['bar_len']
        del analysis['beat_len']
        del analysis['section_len']
        del analysis['segment_len']
        del analysis['tatum_len']

        flattened_analysis.append(flatten_dict_values(analysis))

    track_audio_analysis = np.array(flattened_analysis)

    # features need to be flattened as well
    track_audio_features = np.array([flatten_dict_values(audio_features) for audio_features in track_audio_features])

    ## partition data/labels into train, validation, test

    track_names_train, track_names_valid, track_names_test = split_vector(track_names, 0.6, 0.8)
    track_artists_train, track_artists_valid, track_artists_test = split_vector(track_artists, 0.6, 0.8)
    track_album_names_train, track_album_names_valid, track_album_names_test = split_vector(track_album_names, 0.6, 0.8)
    track_audio_features_train, track_audio_features_valid, track_audio_features_test = split_vector(track_audio_features, 0.6, 0.8)
    track_audio_analysis_train, track_audio_analysis_valid, track_audio_analysis_test = split_vector(track_audio_analysis, 0.6, 0.8)

    track_ratings_train, track_ratings_valid, track_ratings_test = split_vector(track_ratings, 0.6, 0.8)
    pdb.set_trace()
    ## normalize features/analysis
    feature_mean = track_audio_features_train.mean(axis=0)
    feature_std = track_audio_features_train.std(axis=0)
    normalize(track_audio_features_train, feature_mean, feature_std)
    normalize(track_audio_features_valid, feature_mean, feature_std)
    normalize(track_audio_features_test, feature_mean, feature_std)

    ## drop any feature columns with 0 standard deviation
    nonzero_std_idx = np.where(feature_std != 0)[0]
    track_audio_features_train = track_audio_features_train[:, nonzero_std_idx]
    track_audio_features_valid = track_audio_features_valid[:, nonzero_std_idx]
    track_audio_features_test = track_audio_features_test[:, nonzero_std_idx]

    analysis_mean = track_audio_analysis_train.mean(axis=0)
    analysis_std = track_audio_analysis_train.std(axis=0)
    normalize(track_audio_analysis_train, analysis_mean, analysis_std)
    normalize(track_audio_analysis_valid, analysis_mean, analysis_std)
    normalize(track_audio_analysis_test, analysis_mean, analysis_std)

    ## drop any analysis columns with 0 standard deviation
    nonzero_std_idx = np.where(analysis_std != 0)[0]
    track_audio_analysis_train = track_audio_analysis_train[:, nonzero_std_idx]
    track_audio_analysis_valid = track_audio_analysis_valid[:, nonzero_std_idx]
    track_audio_analysis_test = track_audio_analysis_test[:, nonzero_std_idx]

    ## Create model

    track_name_layer = keras.Input(shape=track_names[0].shape)
    track_artists_layer = keras.Input(shape=track_artists[0].shape)
    track_album_name_layer = keras.Input(shape=track_album_names[0].shape)
    track_audio_features_layer = keras.Input(shape=track_audio_features[0].shape)
    track_audio_analysis_layer = keras.Input(shape=track_audio_analysis[0].shape)

    features = keras.layers.Concatenate()([
        track_name_layer,
        track_artists_layer,
        track_album_name_layer,
        track_audio_features_layer,
        track_audio_analysis_layer])

    features = Dense(128, activation='relu')(features)
    features = Dense(64, activation='relu')(features)
    features = Dense(32, activation='relu')(features)

    rating = Dense(5, activation='softmax')(features)

    model = keras.Model(
        inputs=[track_name_layer, track_artists_layer, track_album_name_layer,track_audio_features_layer,track_audio_analysis_layer],
        outputs=[rating])
    model.compile(optimizer='adam', loss=keras.losses.SparseCategoricalCrossentropy(), metrics=[keras.metrics.SparseCategoricalAccuracy()])
    
    ## Fit model
    model.fit(
        x=[track_names_train, track_artists_train, track_album_names_train, track_audio_features_train, track_audio_analysis_train],
        y=[track_ratings_train],
        epochs=200,
        batch_size=2,
        validation_data=(
            [track_names_valid, track_artists_valid, track_album_names_valid, track_audio_features_valid, track_audio_analysis_valid],
            [track_ratings_valid]
        )
    )
    
    test_loss, test_accuracy = model.evaluate(
        x=[track_names_test, track_artists_test, track_album_names_test, track_audio_features_test, track_audio_analysis_test],
        y=[track_ratings_test],
    )

    print(f'test_loss: {test_loss}, test_accuracy: {test_accuracy}')

    return model