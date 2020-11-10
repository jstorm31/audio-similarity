import os
import librosa
from mongoengine import *


class Audiotrack(Document):
    filename = StringField(required=True, unique=True)
    duration = FloatField(required=True)

    @classmethod
    def create(cls, filename):
        signal, sr = librosa.load(os.getenv('DATA_PATH') + filename)
        duration = librosa.get_duration(y=signal, sr=sr)
        return cls(filename=filename, duration=duration)
