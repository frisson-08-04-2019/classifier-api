print('importing libraries...')
from flask import Flask, request, jsonify
from werkzeug import secure_filename
import time
from pathlib import Path
import requests, os
import boto3

from classifier.classifier.classifier import Classifier

from settings import *

path_tmp = os.path.join(PATH_DATA, 'tmp')
os.makedirs(path_tmp, exist_ok=True)

path_model = os.path.join(PATH_DATA, 'models', 'model.p')
if not os.path.exists(path_model):
    print('Downloading model...')
    os.makedirs(os.path.join(PATH_DATA, 'models'), exist_ok=True)
    s3_resource = boto3.resource('s3')
    s3_resource.Object(MODEL_BUCKET, MODEL_PATH).download_file(path_model)

classifier = Classifier(load_net_path=path_model)
classifier.class_labels = LABELS

print('Starting server...')

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Image classification\n'


@app.route('/predict', methods=['GET'])
def predict():
    t = time.time()
    url = request.args['url']
    app.logger.info('Classifying image %s' % (url), )

    tmp_filename = Path(os.path.join(path_tmp, secure_filename(url)))
    response = requests.get(url)
    tmp_filename.write_bytes(response.content)

    predicted, certainty, label, scores, t_predict = classifier.eval_single_img(path=tmp_filename)

    t_whole = time.time() - t
    app.logger.info('Execution time: %0.02f seconds' % t_whole)
    app.logger.info('Prediction time: %0.02f seconds' % t_predict)
    app.logger.info('Image %s classified as %s with certainty %.2f' % (url, label, certainty))
    app.logger.info('Predicted scores:')
    for k, v in scores.items():
        app.logger.info('%.2f - %s' % (v, k))

    txt = 'Execution time: %0.02f seconds.\n' % t_whole
    txt += 'Image classified as %s with certainty %.3f\n' % (label.upper(), certainty)
    txt += 'Predicted scores:\n'
    for k, v in scores.items():
        txt += '%.3f - %s\n' % (v, k)

    return txt


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=PORT)
