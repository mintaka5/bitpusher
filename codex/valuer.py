import itertools
import os
import random
import time
from enum import Enum


class PBaseTypes(Enum):
    A = 0
    G = 1


class PyBaseTypes(Enum):
    C = 1
    T = 0


def form_base_pair(rand_num, interval):
    if rand_num > 0.5:
        pbase_type = PBaseTypes.G
    else:
        pbase_type = PBaseTypes.A
    if pbase_type == PBaseTypes.A:
        pybase_type = PyBaseTypes.T
    elif pbase_type == PBaseTypes.G:
        pybase_type = PyBaseTypes.C
    base_pair = [pbase_type, pybase_type]
    random.shuffle(base_pair)
    return base_pair


def is_valid_base_pair(p, py):
    if p is PBaseTypes.A.name and py is PyBaseTypes.T.name \
            or p is PyBaseTypes.T.name and py is PBaseTypes.A.name:
        return True
    elif p is PBaseTypes.G and py is PyBaseTypes.C \
            or p is PyBaseTypes.C.name and py is PBaseTypes.G.name:
        return True

    return False


def ensurer(seq, length):
    if len(seq[0]) != length or len(seq[1]) != length:
        return False

    for i, base in enumerate(seq[0]):
        is_ok = is_valid_base_pair(base, seq[1][i])
        if is_ok:
            return True

    return False


def generate_base_pair(limit=8):
    '''
    generate a random base type
    '''
    i = 0
    pseq = []
    pyseq = []
    while i < limit:
        rand_decimal = int.from_bytes(
            os.urandom(8),
            byteorder="big"
        ) / ((1 << 64) - 1)
        base_pair = form_base_pair(rand_decimal, i)
        pseq.append(base_pair[0].name)
        pyseq.append(base_pair[1].name)
        i += 1
    seq = (tuple(pseq), tuple(pyseq))
    is_good = ensurer(seq, limit)
    if is_good:
        [print(x, end="") for x in seq[0]]
        print("")
        [print(y, end="") for y in seq[1]]


def init():
    generate_base_pair(64)
