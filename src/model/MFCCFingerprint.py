import pickle
from bson.binary import Binary
from .Fingerprint import Fingerprint


class MFCCFingerprint(Fingerprint):
    def __init__(self, audiotrack, sample):
        "Creates an instance from an MFCC descriptor sample"
        data = Binary(pickle.dumps(sample, protocol=2))
        super(MFCCFingerprint, self).__init__(audiotrack=audiotrack,
                                              type='mfcc', data=data)

    def deserialize_data(self):
        "Deserializes binary data into MFCC descriptor"
        return pickle.loads(self.data)
