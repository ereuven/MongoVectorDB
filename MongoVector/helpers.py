import numpy as np
from bson.binary import Binary
import pickle


def normalize_num(x, min_val, max_val):
    return (x - min_val) / (max_val - min_val)


def normalize_vec(vec):
    return vec / np.linalg.norm(vec)


def nparray_to_bin(nparr):
    return Binary(pickle.dumps(nparr, protocol=2), subtype=128)


def bin_to_nparray(binary):
    return pickle.loads(binary)
