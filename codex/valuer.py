from enum import Enum


class Nucleotides(Enum):
    T = 'T'
    C = 'C'
    A = 'A'
    G = 'G'

    @classmethod
    def to_name(cls):
        return cls()


def init():
    print(Nucleotides.G.name)
