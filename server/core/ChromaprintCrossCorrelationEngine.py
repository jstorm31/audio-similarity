import math
import numpy

from .ChromaprintEngine import ChromaprintEngine
from model.Fingerprint import Fingerprint, FingerprintType


class ChromaprintCrossCorrelationEngine(ChromaprintEngine):
    def __init__(self, data_path, span=150, step=1, min_overlap=20, treshold=0.5):
        super(ChromaprintCrossCorrelationEngine,
              self).__init__(data_path, None)
        self.span = span  # number of points to scan cross correlation over
        self.step = step  # step size (in points) of cross correlation
        # minimum number of points that must overlap in cross correlation
        self.min_overlap = min_overlap
        # report match when cross correlation has a peak exceeding threshold
        self.treshold = treshold

    def extract_fingerprints(self, audiotrack):
        path = self.data_path + audiotrack.filename
        chromaprint = self._fingerprint_audiotrack(path)

        return [Fingerprint.create(FingerprintType.CHROMAPRINT_CC.value, audiotrack, chromaprint)]

    def compare(self, lhs, rhs):
        """
        Calculates similarity between two chromaprints
        """
        cross_correlations = self.__compare(lhs, rhs)
        return self.__get_max_corr(cross_correlations, lhs, rhs)

    def find_matches(self, audiotrack, top_k):
        chromaprints = Fingerprint.objects(
            type=FingerprintType.CHROMAPRINT_CC.value)
        ref_chromaprints = self.extract_fingerprints(audiotrack)
        ref_samples = [sample.deserialize_data()
                       for sample in ref_chromaprints]

        avg_matches = []
        for sample in ref_samples:
            if len(sample) == 0:
                continue

            matches = self.__calc_chromaprints_similarity(sample, chromaprints)
            song_matches = average_matches(matches, 1)

            if not avg_matches:
                avg_matches = song_matches
            else:
                avg_matches = {
                    key: max(similarity, avg_matches[key]) for key, similarity in song_matches.items()}

        # Sort by similarity
        return [{'filename': k, 'similarity': v} for k, v in sorted(avg_matches.items(), key=lambda x: x[1], reverse=True)][:top_k]

    def __correlation(self, listx, listy):
        """
        Returns correlation between lists
        """
        if len(listx) == 0 or len(listy) == 0:
            raise Exception('Empty lists cannot be correlated.')

        covariance = 0
        for x, y in zip(listx, listy):
            covariance += 32 - bin(x ^ y).count("1")

        covariance = covariance / float(min(len(listx), len(list(y))))
        return covariance / 32

    def __cross_correlation(self, listx, listy, offset):
        """
        Returns cross correlation, with listy offset from listx
        """
        if offset > 0:
            listx = listx[offset:]
            listy = listy[:len(listx)]
        elif offset < 0:
            offset = -offset
            listy = listy[offset:]
            listx = listx[:len(listy)]

        if min(len(listx), len(listy)) < self.min_overlap:
            raise Exception(
                'Cross correlation error - overlap too small: %i' % min(len(listx), len(listy)))
        return self.__correlation(listx, listy)

    def __compare(self, listx, listy):
        """
        Cross correlate listx and listy with offsets from -span to span
        """
        min_len = min(len(listx), len(listy))
        if self.span > min_len:
            raise Exception('span >= sample size: %i >= %i\n' % (
                self.span, min_len + 'Reduce span, reduce crop or increase sample_time.'))

        corr_xy = []
        for offset in numpy.arange(-self.span, self.span + 1, self.step):
            corr_xy.append(self.__cross_correlation(listx, listy, offset))
        return corr_xy

    def __max_index(self, listx):
        max_index = 0
        max_value = listx[0]
        for i, value in enumerate(listx):
            if value > max_value:
                max_value = value
                max_index = i
        return max_index

    def __get_max_corr(self, corr, source, target):
        max_corr_index = self.__max_index(corr)
        max_corr_offset = -self.span + max_corr_index * self.step
        return corr[max_corr_index]
