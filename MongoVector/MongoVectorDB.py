import logging
from typing import List
from pymongo import MongoClient
from bson import ObjectId
from scipy.spatial.distance import cdist
from MongoVector.helpers import *
from MongoVector.models.Vector import *
from MongoVector.models.Centroid import *


class MongoVectorDB:
    _closest_centroid_id_fieldname = 'closest_centroid_id'

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
                 distance_threshold: float, distance_function_name: str):

        self._logger = logging.getLogger(self.__class__.__name__)

        self._client = mongo_client
        self._db_name = db_name
        self._vectors_collection_name = vectors_collection_name
        self._centroids_collection_name = centroids_collection_name
        self._distance_threshold = distance_threshold
        self._distance_function_name = distance_function_name

        self._init_assertions()
        self._init_collections()

    def _init_assertions(self):
        assert self._client is not None and isinstance(self._client, MongoClient), 'Client must be a MongoClient'
        assert self._db_name, 'DB name can\'t be empty'
        assert self._vectors_collection_name, 'Vectors collection name can\'t be empty'
        assert self._centroids_collection_name, 'Centroids collection name can\'t be empty'
        assert self._distance_threshold > 0, 'Distance threshold must be greater than 0'
        #todo: assert self._distance_function_name in [], 'Distance function must be supported by scipy.spatial.distance.cdist'

    def _init_collections(self):
        self._db = self._client[self._db_name]
        self._vectors_collection = self._db[self._vectors_collection_name]
        self._centroids_collection = self._db[self._centroids_collection_name]

    def index(self, vectors: List[Vector]):
        centroids, centroids_vec_matrix = self._get_centroids()

        _ids = []

        for vec in vectors:
            min_cidx = self._get_closest_centroid_idx(vec.get_vector(), centroids_vec_matrix)

            if min_cidx is None:
                vec[self._closest_centroid_id_fieldname] = self._create_centroid(vec.get_vector())
                centroids, centroids_vec_matrix = self._get_centroids()
            else:
                vec[self._closest_centroid_id_fieldname] = centroids[min_cidx]._id

            vec.save(self._vectors_collection)
            _ids.append(vec._id)

        return _ids

    def search(self, query_vector: np.ndarray, n=10):
        centroids, centroids_vec_matrix = self._get_centroids()
        min_cidx = self._get_closest_centroid_idx(query_vector, centroids_vec_matrix)

        if min_cidx is None:
            return []
        else:
            vectors, vectors_matrix = self._get_centroid_vectors(centroids[min_cidx]._id)
            closest_vectors = self._get_closest_vectors(query_vector, vectors_matrix, n)
            return [(vectors[i], i, d) for i, d in closest_vectors]

    def _get_centroids(self) -> [Centroid]:
        with self._centroids_collection.find() as c:
            centroids = list(map(Centroid, c))
            return centroids, np.asmatrix([c.get_vector() for c in centroids])

    def _get_closest_centroid_idx(self, vector, centroids_vec_matrix):
        if centroids_vec_matrix.shape[1] == 0:
            return None

        distances = cdist(centroids_vec_matrix, vector.reshape((1, -1)), self._distance_function_name).reshape(-1)
        min_index = np.argmin(distances)
        min_distance = distances[min_index]

        return min_index if abs(min_distance) <= self._distance_threshold else None

    def _create_centroid(self, vec):
        c = Centroid()
        c.set_vector(vec)
        c.save(self._centroids_collection)
        self._logger.info('Created centroid: {}'.format(c._id))
        return c._id

    def _get_centroid_vectors(self, centroid_id: ObjectId) -> (List[Vector], np.matrix):
        with self._vectors_collection.find({self._closest_centroid_id_fieldname: centroid_id}) as v:
            vectors = list(map(Vector, v))
            return vectors, np.asmatrix([v.get_vector() for v in vectors])

    def _get_closest_vectors(self, query_vector, vectors_matrix, n):
        if vectors_matrix.shape[1] == 0:
            return None

        distances = cdist(vectors_matrix, query_vector.reshape((1, -1)), self._distance_function_name).reshape(-1)
        indxs_min = np.argsort(distances)[:n]

        return list(zip(indxs_min, distances[indxs_min]))
