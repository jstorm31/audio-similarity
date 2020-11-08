import os
from dotenv import load_dotenv
from mongoengine import connect

from model.Audiotrack import Audiotrack
from core.MFCCEngine import MFCCEngine


if __name__ == '__main__':
    load_dotenv()

    connect(db=os.getenv('MONGO_DB_NAME'),
            host=os.getenv('MONGO_DOMAIN'),
            port=int(os.getenv('MONGO_PORT')),
            username=os.getenv('MONGO_INITDB_ROOT_USERNAME'),
            password=os.getenv('MONGO_INITDB_ROOT_PASSWORD'),
            authentication_source='admin')

    engine = MFCCEngine(data_path=os.getenv('DATA_PATH'),
                        sample_size=200, n_mfcc=13)

    track = Audiotrack.fromFilename(filename='sample_1.wav')
    track.save()
    fingerprints = engine.extract_fingerprints(track)

    for x in fingerprints:
        x.save()
