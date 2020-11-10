import os
from dotenv import load_dotenv

from db import db_connect
from core.MFCCEngine import MFCCEngine
from model.Fingerprint import Fingerprint
from model.Audiotrack import Audiotrack

if __name__ == '__main__':
    load_dotenv()
    db_connect()

    engine = MFCCEngine(data_path=os.getenv(
        'DATA_PATH'), sample_size=200, n_mfcc=13)

    track = Audiotrack.create(filename='recorded_sample_1.m4a')
    matches = engine.find_match(track)

    for match in matches:
        print("%s: %f" % (match['audiotrack'].filename, match['dist']))
