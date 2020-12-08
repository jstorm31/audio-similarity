import os
import math
import librosa
from dtw import dtw
from numpy.linalg import norm

from .Engine import Engine
from model.Audiotrack import Audiotrack
from model.Fingerprint import Fingerprint, FingerprintType
from .utils import average_matches


class MFCCEngine(Engine):
    def __init__(self, data_path, sample_size = 200, n_mfcc = 6, n_average = 1):
        self.data_path = data_path
        self.sample_size = sample_size
        self.n_mfcc = n_mfcc
        self.n_average = n_mfcc

    def extract_fingerprints(self, audiotrack, duration = 120.0):
        mfcc = self.__extract_mfcc(audiotrack.filename, duration)
        samples = self.__split_mfcc(mfcc)

        return [Fingerprint.create(FingerprintType.MFCC.value, audiotrack, sample) for sample in samples]

    def compare(self, lhs, rhs):
        dist, cost, acc_cost, path = dtw(
            lhs.T, rhs.T, dist=lambda x, y: norm(x - y, ord=1))
        return dist

    def find_matches(self, audiotrack, top_k):
        fingerprints = Fingerprint.objects(type=FingerprintType.MFCC.value)
        ref_mfcc = self.extract_fingerprints(audiotrack, 10.0)

        # Calculate top track matches for each reference mfcc and make an average from it
        total_matches = {}
        for i in range(len(ref_mfcc)):
            fragment = ref_mfcc[i]
            print("Processing fragment %i of %i" % (i, len(ref_mfcc)))

            sample_matches = self.__calc_fingerprints_distance(
                fragment.deserialize_data(), fingerprints)
            song_matches = average_matches(sample_matches, self.n_average)

            if not total_matches:
                total_matches = song_matches
            else:
                # Calcualte average from current and new matches
                total_matches = {
                    key: max(dist, total_matches[key]) for key, dist in song_matches.items()}

        # Sort by distance
        normalized_matches = self.__normalize_results(total_matches)
        sorted_matches = sorted(normalized_matches.items(), key=lambda x: x[1])
        return [{'filename': k, 'distance': v} for k, v in sorted_matches[:top_k]]
    
    def __normalize_results(self, results):
        # dict filename: distance
        sum_distance = sum(results.values())
        return { key: (distance / sum_distance) for key, distance in results.items() }

    def __calc_fingerprints_distance(self, ref_mfcc, fingerprints):
        "Loop over all samples in the database and find the best match"
        matches = []

        for fingerprint in fingerprints:
            dist = None
            mfcc = fingerprint.deserialize_data()

            # Align both samples to the same size
            if ref_mfcc.shape[1] == mfcc.shape[1]:
                dist = self.compare(ref_mfcc, mfcc)
            elif ref_mfcc.shape[1] < mfcc.shape[1]:
                dist = self.compare(ref_mfcc, mfcc[:, ref_mfcc.shape[1]])
            else:
                dist = self.compare(ref_mfcc[:, mfcc.shape[1]], mfcc)

            matches.append(
                {'filename': fingerprint.audiotrack.filename, 'distance': dist})

        return sorted(matches, key=lambda x: x['distance'])

    def __extract_mfcc(self, file_path, duration = 120.0):
        "Extracts MFCC descriptors from an audiotrack located in the file_path"
        signal, sr = librosa.load(
            path=self.data_path + file_path, duration=duration)
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
