import os
import getopt
import sys
import time
from os import listdir
from os.path import isfile, join
from dotenv import load_dotenv
from mongoengine import connect

from model.Audiotrack import Audiotrack
from model.Fingerprint import Fingerprint
from core.MFCCEngine import MFCCEngine
from core.ChromaprintEngine import ChromaprintEngine


def is_audiofile(data_path, file):
    audio_extensions = {'m4a', 'flac', 'mp3', 'wav'}
    extension = file.split('.')[-1]
    return isfile(join(data_path, file)) and extension in audio_extensions


def build_db(engine_type):
    print("Building db with %s engine" % engine_type)
    start = time.time()
    data_path = os.getenv('DATA_PATH')

    if engine_type == 'mfcc':
        engine = MFCCEngine(data_path=data_path, sample_size=200, n_mfcc=10)
    elif engine_type == 'chromaprint':
        engine = ChromaprintEngine(data_path=data_path, sample_size=40)
    else:
        print("Undefined engine type. Available engines: mfcc, chromaprint")
        sys.exit(2)

    files = [f for f in listdir(data_path) if is_audiofile(data_path, f)]
    fingerprint_cnt = 0

    for file in files:
        track = Audiotrack.create(filename=file)
        track.save()
        fingerprints = engine.extract_fingerprints(track)

        for fingerprint in fingerprints:
            fingerprint_cnt += 1
            fingerprint.save()

    print("Created %d fingerprints from %d songs in %.2f s" %
          (fingerprint_cnt, len(files), time.time() - start))


def db_connect():
    connect(db=os.getenv('MONGO_INITDB_DATABASE'),
            host=os.getenv('MONGODB_HOST'),
            username=os.getenv('MONGO_INITDB_ROOT_USERNAME'),
            password=os.getenv('MONGO_INITDB_ROOT_PASSWORD'),
            authentication_source='admin')


if __name__ == '__main__':
    load_dotenv()
    db_connect()

    try:
        arguments, values = getopt.getopt(sys.argv[1:], 'e', 'engine')
    except getopt.error as err:
        print(str(err))
        sys.exit(2)

    engine_type = 'chromaprint'
    for i in range(len(arguments)):
        if arguments[i][0] in ('-e', '--engine'):
            engine_type = values[i]

    # Clear collections
    Audiotrack.drop_collection()
    Fingerprint.drop_collection()

    build_db(engine_type)
