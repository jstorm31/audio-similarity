from mongoengine import *
import pickle
from bson.binary import Binary
from enum import Enum


class FingerprintType(Enum):
    MFCC = 'mfcc'
    CHROMAPRINT = 'chromaprint'
    CHROMAPRINT_CC = 'chromaprint_cc'

    @classmethod
    def create(cls, raw_type):
        if raw_type == 'mfcc':
            return cls.MFCC
        elif raw_type == 'chromaprint':
            return cls.CHROMAPRINT
        elif raw_type == 'chromaprint_cc':
            return cls.CHROMAPRINT_CC

        raise Exception("Undefined engine type. Available engines: ",
                        [t.value for t in FingerprintType])


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
