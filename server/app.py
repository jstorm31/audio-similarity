import datetime
import os
from dotenv import load_dotenv

from flask import Flask, Response, request
from flask_mongoengine import MongoEngine
from model.Audiotrack import Audiotrack
from model.Fingerprint import Fingerprint
from core.MFCCEngine import MFCCEngine


load_dotenv()

app = Flask(__name__)

host = os.getenv('MONGODB_HOST')
username = os.getenv('MONGO_INITDB_ROOT_USERNAME')
password = os.getenv('MONGO_INITDB_ROOT_PASSWORD')
database = os.getenv('MONGO_INITDB_DATABASE')

app.config['MONGODB_SETTINGS'] = {
    'connect': False,
    'host': 'mongodb://' + username + ':' + password + '@' + host + ':27017' + '/' + database + '?authSource=admin'
}

db = MongoEngine()
db.init_app(app)

engine = MFCCEngine(data_path=os.getenv(
        'DATA_PATH'), sample_size=200, n_mfcc=10)

@app.route("/search")
def index():
    # tracks = Audiotrack.objects().to_json()

    # track = Audiotrack.create(filename='recorded_sample_1.m4a')
    # matches = engine.find_match(track, top_k=5)

    return Response("{}", mimetype="application/json", status=200)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
