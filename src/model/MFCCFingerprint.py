import pickle
from bson.binary import Binary
from .Fingerprint import Fingerprint


class MFCCFingerprint(Fingerprint):
    @classmethod
    def create(cls, audiotrack, sample):
        "Creates an instance from an MFCC descriptor sample"
        data = Binary(pickle.dumps(sample, protocol=2))
        return cls(audiotrack=audiotrack, type='mfcc', data=data)

    def deserialize_data(self):
        "Deserializes binary data into MFCC descriptor"
        return pickle.loads(self.data)
