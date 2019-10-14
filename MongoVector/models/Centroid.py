__all__ = ['Centroid']

from MongoVector.models.MongoModel import MongoModel
from MongoVector.helpers import nparray_to_bin, bin_to_nparray
import numpy as np


class Centroid(MongoModel):
    vector_fieldname = 'vector'
    vector_field_fieldname = 'vector_field'

    def set_vector(self, nparr: np.ndarray):
        self[self.vector_fieldname] = nparray_to_bin(nparr)

    def get_vector(self) -> np.ndarray:
        v = self.get(self.vector_fieldname, None)
        return bin_to_nparray(v) if v is not None else v

    def del_vector(self):
        del self[self.vector_fieldname]

    def set_vector_field(self, fieldname: str):
        self[self.vector_field_fieldname] = fieldname

    def get_vector_field(self) -> str:
        return self[self.vector_field_fieldname]
