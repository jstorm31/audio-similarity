import os
import librosa
from mongoengine import *


class Audiotrack(Document):
    filename = StringField(required=True, unique=True)
    duration = FloatField(required=True)

    def __init__(self, filename):
        signal, sr = librosa.load(os.getenv('DATA_PATH') + filename)
        duration = librosa.get_duration(y=signal, sr=sr)
        super(Audiotrack, self).__init__(
            filename=filename, duration=duration)
