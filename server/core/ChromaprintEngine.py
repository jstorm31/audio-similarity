import subprocess

from .Engine import Engine
from model.Fingerprint import Fingerprint

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
    def __init__(self, data_path):
        self.data_path = data_path

    def extract_fingerprints(self, audiotrack):
        path = self.data_path + audiotrack.filename
        chromaprint = self.__fingerprint_audiotrack(path)

        # TODO: Split to many smaller samples

        return [Fingerprint.create('chromaprint', audiotrack, chromaprint)]

    def compare(self, lhs, rhs):
        "Calculates similarity between two chromaprints"
        error = 0
        for x, y in zip(lhs, rhs):
            error += self.__popcnt(x ^ y)
        return 1.0 - error / 32.0 / min(len(lhs), len(rhs))

    def find_matches(self, audiotrack, top_k):
        chromaprints = Fingerprint.objects(type='chromaprint')
        ref_chromaprint = self.extract_fingerprints(audiotrack)[0]

        matches = []
        for chromaprint in chromaprints:
            similarity = self.compare(
                chromaprint.deserialize_data(), ref_chromaprint.deserialize_data())
            matches.append(
                {'filename': chromaprint.audiotrack.filename, 'similarity': similarity})

        # TODO: sort by similarity

        return matches

    def __fingerprint_audiotrack(self, path):
        cmd = 'fpcalc %s -raw' % path
        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

        if error:
            raise Exception(error)
        return self.__parse_chromaprint_output(output)

    def __parse_chromaprint_output(self, output):
        output = output.decode('utf-8')
        key = 'FINGERPRINT='
        strip_index = output.find(key) + len(key)
        raw_fingerprint = output[strip_index:-1]

        return list(map(int, raw_fingerprint.split(',')))

    def __popcnt(self, x):
        """
        Count the number of set bits in the given 32-bit integer.
        """
        return (popcnt_table_8bit[(x >> 0) & 0xFF] +
                popcnt_table_8bit[(x >> 8) & 0xFF] +
                popcnt_table_8bit[(x >> 16) & 0xFF] +
                popcnt_table_8bit[(x >> 24) & 0xFF])
