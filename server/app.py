import datetime
import os
import json
import time
from dotenv import load_dotenv

from flask import Flask, Response, request, abort, jsonify, send_from_directory
from flask_cors import CORS, cross_origin
from flask_mongoengine import MongoEngine
from model.Audiotrack import Audiotrack
from model.Fingerprint import Fingerprint, FingerprintType
from core.MFCCEngine import MFCCEngine
from core.ChromaprintEngine import ChromaprintEngine
from core.get_engine import get_engine


load_dotenv()

app = Flask(__name__)
CORS(app)

host = os.getenv('MONGODB_HOST')
username = os.getenv('MONGO_INITDB_ROOT_USERNAME')
password = os.getenv('MONGO_INITDB_ROOT_PASSWORD')
database = os.getenv('MONGO_INITDB_DATABASE')

app.config['MONGODB_SETTINGS'] = {'connect': False, 'host': 'mongodb://' + username +
                                  ':' + password + '@' + host + ':27017' + '/' + database + '?authSource=admin'}

db = MongoEngine()
db.init_app(app)

data_path = os.getenv('DATA_PATH')


def json_abort(status_code, message):
    response = jsonify({'error': message})
    response.status_code = status_code
    abort(response)


@app.route("/search", methods=['POST'])
def search():
    if not request.files:
        json_abort(400, "'audiotrack' key not set")

    form = request.form.to_dict()
    top_k = int(form['top_k'])
    engine_type = FingerprintType.create(form['engine'])

    if not top_k or not engine_type:
        json_abort(400, 'engine and top_k params missing')

    start = time.time()
    engine = get_engine(engine_type)
    audiotrack = request.files['audiotrack']
    audiotrack.save(os.path.join(data_path, audiotrack.filename))

    track = Audiotrack.create(filename=audiotrack.filename)
    matches = engine.find_matches(track, top_k=top_k)

    response = {
        'data': matches,
        'time': time.time() - start,
    }

    return Response(json.dumps(response), mimetype="application/json", status=200)


@app.route('/audiotracks/<path:filename>')
def serve_audiotracks(filename):
    return send_from_directory(data_path, filename)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)
