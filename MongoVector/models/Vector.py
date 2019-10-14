__all__ = ['Vector']

from MongoVector.models.MongoModel import MongoModel
from MongoVector.helpers import nparray_to_bin, bin_to_nparray
import numpy as np
from bson import ObjectId


class Vector(MongoModel):
    _closest_centroid_id_fieldname = 'closest_centroid_id_{}'

    @classmethod
    def closest_centroid_id_fieldname(cls, field_name: str) -> str:
        return cls._closest_centroid_id_fieldname.format(field_name)

    def set_vector(self, nparr: np.ndarray, vector_field: str):
        self[vector_field] = nparray_to_bin(nparr)

    def get_vector(self, vector_field: str) -> np.ndarray:
        v = self.get(vector_field, None)
        return bin_to_nparray(v) if v is not None else v

    def del_vector(self, vector_field):
        del self[vector_field]

    def set_closest_centroid(self, field_name: str, centroid_id: ObjectId):
        self[Vector.closest_centroid_id_fieldname(field_name)] = centroid_id

    def contains_fields(self, *field_names):
        for fn in field_names:
            if not self.__contains__(fn):
                return False

        return True
