import math
import librosa
import pandas as pd
import numpy as np


def convert_to_spectogram(section, sr=22050, normalize=True):
    spectrogram = librosa.feature.melspectrogram(y=section, sr=sr, n_mels=32)
    M_db = librosa.power_to_db(spectrogram, ref=np.max)
    if not normalize:
        return M_db
    else:
        return librosa.util.normalize(M_db) + 1


def slice_audio(samples, slice_len_sec=3, sr=22050):
    num_sections = math.floor(len(samples) / sr / slice_len_sec)
    sliced = samples[:(sr * slice_len_sec * num_sections)]
    return np.split(sliced, num_sections)


def process_audio(df, file_path, samples, class_id):
    sections = slice_audio(samples)

    for slice_id in range(len(sections)):
        section = sections[slice_id]
        spectogram = convert_to_spectogram(section)
        df = pd.concat([df, pd.DataFrame(
            {'file_path': [file_path], 'slice_id': [slice_id], 'spectrogram': [spectogram], 'label': [class_id]})], ignore_index=True)
    return df


def process_dataset(dataset):
    df = pd.DataFrame(
        {'file_path': [], 'slice_id': [], 'spectrogram': [], 'label': []})
    for [file_path, data, class_id] in dataset.values:
        df = process_audio(df, file_path, data, class_id)
    return df


def read_file_and_resample(file_path):
    samples, sr = librosa.load(file_path)
    return samples


def predict_using_model(X, model, verbose=0):
    softmax_predictions = model.predict(np.array(X))
    predictions = np.array([softmax_result.argmax()
                           for softmax_result in softmax_predictions])
    labels_predicted, frequency = np.unique(predictions, return_counts=True)
    final_prediction = labels_predicted[frequency.argmax()]
    if verbose > 0:
        print("Slice predictions: ", predictions)
        print("Cumul. Prediction, Labels predicted, Labels frequency")
        print(final_prediction, labels_predicted, frequency)
    return final_prediction


def predict_song(file_path, model, verbose=0):
    samples, sr = librosa.load(file_path)

    slices = slice_audio(samples)

    X = [convert_to_spectogram(section) for section in slices]

    return predict_using_model(X, model, verbose=verbose)
