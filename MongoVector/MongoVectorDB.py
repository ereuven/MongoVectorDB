import logging
from typing import List, Dict, Tuple
from pymongo import MongoClient
from bson import ObjectId
from scipy.spatial.distance import cdist
from MongoVector.helpers import *
from MongoVector.models.Vector import *
from MongoVector.models.Centroid import *
from MongoVector.models.VectorField import VectorField


class MongoVectorDB:
    @property
    def db_name(self) -> str:
        return self._db_name

    @property
    def centroids_collection_name(self) -> str:
        return self._centroids_collection_name

    @property
    def vectors_collection_name(self) -> str:
        return self._vectors_collection_name

    def __init__(self, mongo_client: MongoClient, db_name: str,
                 vectors_collection_name: str, centroids_collection_name: str,
                 vector_fields: Dict[str, VectorField]):

        self._logger = logging.getLogger(self.__class__.__name__)

        self._client = mongo_client
        self._db_name = db_name
        self._vectors_collection_name = vectors_collection_name
        self._centroids_collection_name = centroids_collection_name
        self._vector_fields = vector_fields

        self._init_assertions()
        self._init_collections()

    def _init_assertions(self):
        assert self._client is not None and isinstance(self._client, MongoClient), 'Client must be a MongoClient'
        assert self._db_name, 'DB name can\'t be empty'
        assert self._vectors_collection_name, 'Vectors collection name can\'t be empty'
        assert self._centroids_collection_name, 'Centroids collection name can\'t be empty'

        assert self._vector_fields is not None and len(self._vector_fields) > 0, 'Vector fields must be defined'

        for field_name, vf in self._vector_fields.items():
            assert field_name, 'Field name can\'t be empty (vector_fields[{}])'.format(field_name)
            assert vf.distance_threshold > 0, 'Distance threshold must be greater than 0 (vector_fields[{}])'.format(field_name)
            # todo: assert vf.distance_function_name in [], 'Distance function must be supported by scipy.spatial.distance.cdist (vector_fields[{}])'.format(field_name)

    def _init_collections(self):
        self._db = self._client[self._db_name]
        self._vectors_collection = self._db[self._vectors_collection_name]
        self._centroids_collection = self._db[self._centroids_collection_name]

    def index(self, vectors: List[Vector]) -> List[ObjectId]:
        for i, v in enumerate(vectors):
            assert v.contains_fields(*self._vector_fields.keys()), 'vectors[{}] does not contains all fields'.format(i)

        centroids_collection = self._get_all_centroids_by_fieldname()

        _ids = []

        for vec in vectors:
            for field_name in centroids_collection:
                vector = vec.get_vector(field_name)
                min_cidx = self._get_closest_centroid_idx(vector, centroids_collection[field_name][1], field_name)

                if min_cidx is None:
                    vec.set_closest_centroid(field_name, self._create_centroid(vector, field_name))
                    centroids_collection[field_name] = self._get_field_centroids(field_name)
                else:
                    vec.set_closest_centroid(field_name, centroids_collection[field_name][0][min_cidx]._id)

            vec.save(self._vectors_collection)
            _ids.append(vec._id)

        return _ids

    def search(self, field_name: str, query_vector: np.ndarray, n=10):
        assert field_name in self._vector_fields.keys(), "'{}' not in vector fields".format(field_name)

        centroids, centroids_vec_matrix = self._get_field_centroids(field_name)
        min_cidx = self._get_closest_centroid_idx(query_vector, centroids_vec_matrix, field_name)

        if min_cidx is None:
            return []
        else:
            vectors, vectors_matrix = self._get_centroid_vectors(centroids[min_cidx]._id, field_name)
            closest_vectors = self._get_closest_vectors(query_vector, vectors_matrix, n, field_name)
            return [{'vector': vectors[i], 'distance': d} for i, d in closest_vectors]

    def _get_field_centroids(self, field_name) -> (List[Centroid], np.matrix):
        with self._centroids_collection.find({Centroid.vector_field_fieldname: field_name}) as c:
            centroids = list(map(Centroid, c))
            return centroids, np.asmatrix([c.get_vector() for c in centroids])

    def _get_all_centroids_by_fieldname(self) -> Dict[str, Tuple[List[Centroid], np.matrix]]:
        res = {}

        for field_name in self._vector_fields.keys():
            res[field_name] = self._get_field_centroids(field_name)

        return res

    def _get_closest_centroid_idx(self, vector, centroids_vec_matrix, field_name):
        if centroids_vec_matrix.shape[1] == 0:
            return None

        distances = cdist(centroids_vec_matrix, vector.reshape((1, -1)), self._vector_fields[field_name].distance_function_name).reshape(-1)
        min_index = np.argmin(distances)
        min_distance = distances[min_index]

        return min_index if abs(min_distance) <= self._vector_fields[field_name].distance_threshold else None

    def _create_centroid(self, vec, field_name):
        c = Centroid()
        c.set_vector(vec)
        c.set_vector_field(field_name)
        c.save(self._centroids_collection)
        self._logger.info('Created centroid: {}'.format(c._id))
        return c._id

    def _get_centroid_vectors(self, centroid_id: ObjectId, field_name) -> (List[Vector], np.matrix):
        with self._vectors_collection.find({Vector.closest_centroid_id_fieldname(field_name): centroid_id}) as v:
            vectors = list(map(Vector, v))
            return vectors, np.asmatrix([v.get_vector(field_name) for v in vectors])

    def _get_closest_vectors(self, query_vector, vectors_matrix, n, field_name):
        if vectors_matrix.shape[1] == 0:
            return []

        distances = cdist(vectors_matrix, query_vector.reshape((1, -1)), self._vector_fields[field_name].distance_function_name).reshape(-1)
        indxs_min = np.argsort(distances)[:n]

        return zip(indxs_min, distances[indxs_min])
