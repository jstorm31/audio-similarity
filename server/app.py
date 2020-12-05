import datetime
import os
import json
from dotenv import load_dotenv

from flask import Flask, Response, request, abort, jsonify, send_from_directory
from flask_cors import CORS, cross_origin
from flask_mongoengine import MongoEngine
from model.Audiotrack import Audiotrack
from model.Fingerprint import Fingerprint
from core.MFCCEngine import MFCCEngine
from core.ChromaprintEngine import ChromaprintEngine


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

# engine = MFCCEngine(data_path=data_path, sample_size=200, n_mfcc=10)
engine = ChromaprintEngine(data_path=data_path, sample_size=40)


def json_abort(status_code, message):
    response = jsonify({'error': message})
    response.status_code = status_code
    abort(response)


@app.route("/search", methods=['POST'])
def search():
    if not request.files:
        json_abort(400, "'audiotrack' key not set")

    top_k = int(request.form.get('top_k'))
    audiotrack = request.files['audiotrack']
    audiotrack.save(os.path.join(data_path, audiotrack.filename))

    track = Audiotrack.create(filename=audiotrack.filename)
    matches = engine.find_matches(track, top_k=top_k)

    return Response(json.dumps(matches), mimetype="application/json", status=200)


@app.route('/audiotracks/<path:filename>')
def serve_audiotracks(filename):
    return send_from_directory(data_path, filename)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)
