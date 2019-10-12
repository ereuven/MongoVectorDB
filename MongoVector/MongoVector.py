from pymongo import MongoClient
from .helpers import *
from . import distance


class MongoVector:
    def __init__(self, mongo_client: MongoClient, db_name: str,
                 vectors_collection_name: str, centroids_collection_name: str):
        self.client = mongo_client
        self.db_name = db_name
        self.vectors_collection_name = vectors_collection_name
        self.centroids_collection_name = centroids_collection_name

        self.db = self.client[self.db_name]
        self.vectors_collection = self.db[self.vectors_collection_name]
        self.centroids_collection = self.db[self.centroids_collection_name]

    def index(self, vectors):
        with self._get_centroids() as centroids:
            print(f'found {centroids.count()} centroids')

            for c in centroids:
                print(c)

    def search(self, query_vector):
        pass

    def _get_centroids(self):
        return self.centroids_collection.find()
