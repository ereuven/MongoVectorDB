import logging
import sys
import pymongo
from MongoVector.models.Vector import Vector
from MongoVector.MongoVectorDB import MongoVectorDB
from MongoVector.models.MongoModel import MongoModel
import numpy as np
from pprint import pprint

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# v = Vector()
# v.name=3
# pprint(v)
# pprint(v.get_vector())
# v.set_vector(np.asarray([1,2,3]))
# pprint(v)
# pprint(v.get_vector())
#
# print(np.asarray([v.get_vector(), v.get_vector()]))
# print('*')

client = pymongo.MongoClient('localhost', 27017)
db = MongoVectorDB(client, 'vecdb', 'vectors', 'centroids', 0.701, 'euclidean')

vectors = []
v = Vector({'name': 'vector 1'})
v.set_vector(np.asarray([1, 2, 3]))
vectors.append(v)

v = Vector({'name': 'vector 2'})
v.set_vector(np.asarray([4, 5, 6]))
vectors.append(v)

v = Vector({'name': 'vector 3'})
v.set_vector(np.asarray([40, 50, 60]))
vectors.append(v)
#
#print(db.index(vectors))

#q = np.asarray([1.0001, 2.00002, 3.00003])
q = np.asarray([40.5,50,60])
pprint(list(db.search(q)))


# class MyDoc(MongoModel):
#     def setv(self, value):
#         self['v'] = value + 1
#
#     def delv(self):
#         del self['v']
#
# col = client['testdb']['col1']
# d = MyDoc()
# d.setv(234.3)
# print(d._id)
# print(d)
# d.save(col)
# print(d)
# print(d._id)

# for doc in map(MyDoc, col.find()):
#     print(doc)


# d = MyDoc({'cddaa':22})
# print(d)
# d.load(col, '5da4294d45a68eaf9b5791fb')
# d.aa=123
# print(d)
# d.save(col)
# # print(d)
# # print(d.b)