import numpy as np
from bson.binary import Binary
import pickle


def nparray_to_bin(nparr: np.ndarray, protocl=pickle.HIGHEST_PROTOCOL) -> Binary:
    return Binary(pickle.dumps(nparr, protocol=protocl))


def bin_to_nparray(binary: Binary) -> np.ndarray:
    return pickle.loads(binary)
