import math
import numpy

from .ChromaprintEngine import ChromaprintEngine
from model.Fingerprint import Fingerprint, FingerprintType

class OverlapException(Exception):
    pass


class ChromaprintCrossCorrelationEngine(ChromaprintEngine):
    def __init__(self, data_path, span=40, step=1, min_overlap=8):
        super(ChromaprintCrossCorrelationEngine,
              self).__init__(data_path, None, 1)
        self.span = span  # number of points to scan cross correlation over
        self.step = step  # step size (in points) of cross correlation
        # minimum number of points that must overlap in cross correlation
        self.min_overlap = min_overlap

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
        chromaprints = Fingerprint.objects(type=FingerprintType.CHROMAPRINT_CC.value)
        ref_chromaprint = self.extract_fingerprints(audiotrack)[0]

        if len(ref_chromaprint) == 0:
            raise Exception("Empty reference audiotrack")

        matches = []
        for chromaprint in chromaprints:
            if len(chromaprint) == 0:
                continue

            sim = self.compare(ref_chromaprint.deserialize_data(), chromaprint.deserialize_data())
            matches.append({ 'filename': chromaprint.audiotrack.filename, 'similarity': sim })

        return sorted(matches, key=lambda x: x['similarity'], reverse=True)[:top_k]

    def __correlation(self, listx, listy):
        """
        Returns correlation between lists
        """
        if len(listx) == 0 or len(listy) == 0:
            raise Exception('Empty lists cannot be correlated.')

        covariance = 0
        for x, y in zip(listx, listy):
            covariance += 32 - bin(x ^ y).count("1")

        covariance = covariance / float(min(len(listx), len(listy)))
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
            raise OverlapException()
        return self.__correlation(listx, listy)

    def __compare(self, listx, listy):
        """
        Cross correlate listx and listy with offsets from -span to span
        """
        min_len = min(len(listx), len(listy))
        span = self.span if self.span <= min_len else min_len

        corr_xy = []
        for offset in numpy.arange(-span, span + 1, self.step):
            try:
                corr_xy.append(self.__cross_correlation(listx, listy, offset))
            except OverlapException:
                continue
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
