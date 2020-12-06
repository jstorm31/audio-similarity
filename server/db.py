import os
import getopt
import sys
import time
from os import listdir
from os.path import isfile, join
from dotenv import load_dotenv
from mongoengine import connect

from model.Audiotrack import Audiotrack
from model.Fingerprint import Fingerprint, FingerprintType
from core.MFCCEngine import MFCCEngine
from core.ChromaprintEngine import ChromaprintEngine
from core.ChromaprintCrossCorrelationEngine import ChromaprintCrossCorrelationEngine
from core.get_engine import get_engine


def is_audiofile(data_path, file):
    audio_extensions = {'m4a', 'flac', 'mp3', 'wav'}
    extension = file.split('.')[-1]
    return isfile(join(data_path, file)) and extension in audio_extensions


def build_db(engine_type):
    print("Building db with %s engine" % engine_type.value)
    start = time.time()
    data_path = os.getenv('DATA_PATH')

    engine = get_engine(engine_type)
    files = [f for f in listdir(data_path) if is_audiofile(data_path, f)]
    fingerprint_cnt = 0

    for file in files:
        tracks = Audiotrack.objects(filename=file)
        track = tracks[0] if len(tracks) > 0 else None
        if track is None:
            track = Audiotrack.create(filename=file)
            track.save()

        try:
            fingerprints = engine.extract_fingerprints(track)
        except Exception as e:
            print("Error fingerprinting ", file, e)
            continue

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
        arguments, values = getopt.getopt(
            sys.argv[1:], 'e:c', ['engine', 'clear'])
    except getopt.error as err:
        print(str(err))
        sys.exit(2)

    engine_type = FingerprintType.CHROMAPRINT
    clear = False
    for i in range(len(arguments)):
        if arguments[i][0] in ('-e', '--engine'):
            engine_type = FingerprintType.create(arguments[i][1])
        elif arguments[i][0] in ('-c', '--clear'):
            clear = True

    # Clear collections
    if clear:
        print("Clearing all audiotracks...")
        Audiotrack.drop_collection()
        Fingerprint.drop_collection()
    else:
        Fingerprint.objects(type=engine_type.value).delete()

    build_db(engine_type)
