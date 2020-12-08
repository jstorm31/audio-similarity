import subprocess
import math

from .Engine import Engine
from model.Fingerprint import Fingerprint, FingerprintType
from .utils import average_matches


popcnt_table_8bit = [
    0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4, 1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5,
    1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5, 2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
    1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5, 2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
    2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6, 3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7,
    1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5, 2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
    2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6, 3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7,
    2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6, 3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7,
    3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7, 4, 5, 5, 6, 5, 6, 6, 7, 5, 6, 6, 7, 6, 7, 7, 8,
]


class ChromaprintEngine(Engine):
    def __init__(self, data_path, sample_size, n_average):
        self.data_path = data_path
        self.sample_size = sample_size
        self.n_average = n_average

    def extract_fingerprints(self, audiotrack):
        path = self.data_path + audiotrack.filename
        chromaprint = self._fingerprint_audiotrack(path)
        samples = self.__split_chromaprint(chromaprint)

        return [Fingerprint.create(FingerprintType.CHROMAPRINT.value, audiotrack, sample) for sample in samples]

    def compare(self, lhs, rhs):
        "Calculates similarity between two chromaprints"
        error = 0
        for x, y in zip(lhs, rhs):
            error += self.__popcnt(x ^ y)
        return 1.0 - error / 32.0 / min(len(lhs), len(rhs))

    def find_matches(self, audiotrack, top_k):
        chromaprints = Fingerprint.objects(
            type=FingerprintType.CHROMAPRINT.value)
        ref_chromaprints = self.extract_fingerprints(audiotrack)
        ref_samples = [sample.deserialize_data()
                       for sample in ref_chromaprints]

        avg_matches = []
        for sample in ref_samples:
            if len(sample) == 0:
                continue

            matches = self.__calc_chromaprints_similarity(sample, chromaprints)
            song_matches = average_matches(matches, self.n_average)

            if not avg_matches:
                avg_matches = song_matches
            else:
                avg_matches = {
                    key: max(similarity, avg_matches[key]) for key, similarity in song_matches.items()}

        # Sort by similarity
        return [{'filename': k, 'similarity': v} for k, v in sorted(avg_matches.items(), key=lambda x: x[1], reverse=True)[:top_k]]

    def _fingerprint_audiotrack(self, path):
        cmd = 'fpcalc %s -raw' % path
        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

        if error:
            raise Exception(error)
        return self.__parse_chromaprint_output(output)

    def __parse_chromaprint_output(self, output):
        output = output.decode('utf-8')

        if output == '':
            raise Exception("Error creating fingerprint")

        key = 'FINGERPRINT='
        strip_index = output.find(key) + len(key)
        raw_fingerprint = output[strip_index:-1]

        return list(map(int, raw_fingerprint.split(',')))

    def __split_chromaprint(self, chromaprint):
        "Splits chromaprint from a song into many short ones"
        size = len(chromaprint)
        n_samples = math.floor(size / self.sample_size)
        last_sample_size = size % self.sample_size

        samples = []
        for i in range(n_samples):
            samples.append(
                chromaprint[i*self.sample_size:(i+1)*self.sample_size])
        samples.append(chromaprint[n_samples*self.sample_size:])

        return samples

    def __calc_chromaprints_similarity(self, sample, chromaprints):
        "Loop over all chromaprints and calculate similarity with the given sample"
        matches = []
        sample_size = len(sample)

        for chromaprint in chromaprints:
            similarity = None
            chromaprint_data = chromaprint.deserialize_data()
            chromaprint_size = len(chromaprint_data)

            if chromaprint_size == 0 or sample_size == 0:
                continue

            # Align both samples to the same size
            if sample_size == chromaprint_size:
                similarity = self.compare(sample, chromaprint_data)
            elif sample_size < chromaprint_size:
                similarity = self.compare(
                    sample, chromaprint_data[:sample_size])
            else:
                similarity = self.compare(
                    sample[:chromaprint_size], chromaprint_data)

            matches.append(
                {'filename': chromaprint.audiotrack.filename, 'distance': similarity})

        return sorted(matches, key=lambda x: x['distance'], reverse=True)

    def __popcnt(self, x):
        """
        Count the number of set bits in the given 32-bit integer.
        """
        return (popcnt_table_8bit[(x >> 0) & 0xFF] +
                popcnt_table_8bit[(x >> 8) & 0xFF] +
                popcnt_table_8bit[(x >> 16) & 0xFF] +
                popcnt_table_8bit[(x >> 24) & 0xFF])
