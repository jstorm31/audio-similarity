from mongoengine import *
import pickle
from bson.binary import Binary


class Fingerprint(Document):
    audiotrack = ReferenceField('Audiotrack', required=True)
    type = StringField(required=True)
    data = BinaryField()
    meta = {'allow_inheritance': True}

    @classmethod
    def create(cls, type, audiotrack, sample):
        "Creates an instance from sample (descriptor or chromaprint)"
        data = Binary(pickle.dumps(sample, protocol=2))
        return cls(audiotrack=audiotrack, type=type, data=data)

    def deserialize_data(self):
        "Deserializes binary data"
        return pickle.loads(self.data)
