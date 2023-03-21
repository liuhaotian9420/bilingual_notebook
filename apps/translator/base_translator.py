import itertools
from abc import ABC, abstractmethod


class baseTranslator(ABC):
    def __init__(self, key, src_language, target_language):

        self.keys = itertools.cycle(key.split(","))
        self.source_language = src_language
        self.target_language = target_language

    @abstractmethod
    def rotate_key(self):
        pass

    @abstractmethod
    def translate(self, text):
        pass