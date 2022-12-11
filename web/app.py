import sys
sys.path.append('../')

from utils import predict_song
import os
from flask import Flask, request, flash, redirect, send_file
from tensorflow import keras



dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.abspath(os.path.join(dir_path, '..'))

loaded_model = keras.models.load_model(parent_dir + '/best_model_colab.h5')

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 20


@app.route('/analyze', methods=['POST'])
def analyze_song():
    if 'file' not in request.files:
        return redirect('/')

    file = request.files['file']
    file_path = 'temp_files/' + file.filename
    file.save(file_path)

    prediction = predict_song(file_path, loaded_model)

    os.remove(file_path)
    return 'Prediction ' + str(prediction)


@app.route('/')
def index():
    return send_file('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080')
