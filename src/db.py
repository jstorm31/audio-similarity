import os
from dotenv import load_dotenv, find_dotenv
from mongoengine import *

from model.Audiotrack import Audiotrack

load_dotenv()

connect(db=os.getenv('MONGO_DB_NAME'),
        host=os.getenv('MONGO_DOMAIN'),
        port=int(os.getenv('MONGO_PORT')),
        username=os.getenv('MONGO_INITDB_ROOT_USERNAME'),
        password=os.getenv('MONGO_INITDB_ROOT_PASSWORD'),
        authentication_source='admin')

track = Audiotrack(filename='sample_1.wav', duration=16.6)
track.save()
