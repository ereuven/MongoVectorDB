import pymongo
from MongoVector.MongoVector import MongoVector

client = pymongo.MongoClient('localhost', 27017)
db = MongoVector(client, 'vecdb', 'vectors', 'centroids')

db.index([])
