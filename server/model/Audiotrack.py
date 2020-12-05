import os
import librosa
from mongoengine import *


class Audiotrack(Document):
    filename = StringField(required=True, unique=True)

    @classmethod
    def create(cls, filename):
        return cls(filename=filename)
