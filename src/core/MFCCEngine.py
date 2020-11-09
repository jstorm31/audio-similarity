import os
import math
import librosa
from .Engine import Engine
from model.Audiotrack import Audiotrack
from model.MFCCFingerprint import MFCCFingerprint


class MFCCEngine(Engine):
    def __init__(self, data_path, sample_size, n_mfcc):
        self.data_path = data_path
        self.sample_size = sample_size
        self.n_mfcc = n_mfcc

    def extract_fingerprints(self, audiotrack):
        mfcc = self.__extract_mfcc(audiotrack.filename)
        samples = self.__split_mfcc(mfcc)

        return [MFCCFingerprint(audiotrack, sample) for sample in samples]

    def compare(self, lhs, rhs):
        pass

    def __extract_mfcc(self, file_path):
        "Extracts MFCC descriptors from a audiotrack located in the file_path"
        signal, sr = librosa.load(self.data_path + file_path)
        mfcc = librosa.feature.mfcc(signal, n_mfcc=self.n_mfcc, sr=sr)
        return mfcc

    def __split_mfcc(self, mfcc):
        "Splits MFCC descriptor from a song into many short ones"
        n_samples = math.floor(mfcc.shape[1] / self.sample_size)
        last_sample_size = mfcc.shape[1] % self.sample_size

        samples = []
        for i in range(n_samples):
            samples.append(mfcc[:, i*self.sample_size:(i+1)*self.sample_size])
        samples.append(mfcc[:, n_samples*self.sample_size:])

        return samples
