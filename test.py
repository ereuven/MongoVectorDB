import logging
import sys
import pymongo
from MongoVector.models.Vector import Vector
from MongoVector.MongoVectorDB import MongoVectorDB
from MongoVector.models.MongoModel import MongoModel
from MongoVector.models.VectorField import VectorField
import numpy as np
from pprint import pprint
from timeit import timeit

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

client = pymongo.MongoClient('localhost', 27017)

vf1 = 'res111'
vf2 = 'res222'

db = MongoVectorDB(client, 'vecdb', 'vectors', 'centroids', {
    vf1: VectorField('euclidean', 0.701),
    vf2: VectorField('cosine', 0.001)
})

vectors = []
v = Vector({'name': 'vector 1'})
v.set_vector(np.asarray([1, 2, 3]), vf1)
v.set_vector(np.asarray([1, 2, 3]), vf2)
vectors.append(v)

v = Vector({'name': 'vector 2'})
v.set_vector(np.asarray([4, 5, 6]), vf1)
v.set_vector(np.asarray([4, 5, 6]), vf2)
vectors.append(v)

v = Vector({'name': 'vector 3'})
v.set_vector(np.asarray([40, 50, 60]), vf1)
v.set_vector(np.asarray([40, 50, 60]), vf2)
vectors.append(v)

v = Vector({'name': 'vector 4'})
v.set_vector(np.asarray([40.2, 49.5, 60.3]), vf1)
v.set_vector(np.asarray([40.2, 49.5, 60.3]), vf2)
vectors.append(v)

# v = Vector({'name': 'vector 5'})
# v.set_vector(np.asarray([42, 5, 63]), vf1)
# vectors.append(v)

print(db.index(vectors))

#q = np.asarray([40.5, 50, 60])
q = np.asarray([40, 50, 60])
res = db.search(vf2, q, 100000)
pprint(res)
print('total:', len(res))

