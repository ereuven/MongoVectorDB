__all__ = ['Vector']

from MongoVector.models.MongoModel import MongoModel
from MongoVector.helpers import nparray_to_bin, bin_to_nparray
import numpy as np


class Vector(MongoModel):
    _vector_field = 'vector'

    def set_vector(self, nparr: np.ndarray):
        self[self._vector_field] = nparray_to_bin(nparr)

    def get_vector(self) -> np.ndarray:
        v = self.get(self._vector_field, None)
        return bin_to_nparray(v) if v is not None else v

    def del_vector(self):
        del self[self._vector_field]
