from tensorflow import keras
from flask import Flask, request, flash, redirect, send_file
import os
import sys
sys.path.append('../')
from utils import predict_song


dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.abspath(os.path.join(dir_path, '..'))

loaded_model = keras.models.load_model(parent_dir + '/best_model_colab.h5')

app = Flask(__name__, static_folder='dist')


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

    classname_map = {
        0: 'classical',
        1: 'country',
        2: 'hiphop',
        3: 'jazz',
        4: 'rock'
    }
    return redirect('/results.html?filename=' + file.filename + '&prediction=' + classname_map[prediction])


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080')
