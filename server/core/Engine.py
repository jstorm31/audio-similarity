from abc import ABC, abstractmethod


class Engine(ABC):
    @abstractmethod
    def extract_fingerprints(self, audiotrack):
        """Extracts a feature from an audiotrack saved in file_path and returns an array of samples

        Parameters
        ----------
        audiotrack : Audiotrack
        """
        pass

    @abstractmethod
    def compare(self, lhs, rhs):
        pass

    @abstractmethod
    def find_matches(self, audiotrack, top_k):
        pass
