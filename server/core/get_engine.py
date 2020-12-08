import os

from model.Fingerprint import Fingerprint, FingerprintType
from core.MFCCEngine import MFCCEngine
from core.ChromaprintEngine import ChromaprintEngine
from core.ChromaprintCrossCorrelationEngine import ChromaprintCrossCorrelationEngine


def get_engine(engine_type, params = {}):
    engine = None
    data_path = os.getenv('DATA_PATH')

    if engine_type == FingerprintType.MFCC:
        engine = MFCCEngine(data_path=data_path, sample_size=200, n_mfcc=10, n_average=1)
    elif engine_type == FingerprintType.CHROMAPRINT:
        engine = ChromaprintEngine(data_path=data_path, sample_size=160, n_average=1)
    elif engine_type == FingerprintType.CHROMAPRINT_CC:
        engine = ChromaprintCrossCorrelationEngine(data_path=data_path, span=80, step=2)
    return engine
