#import monary
import pymongo
import numpy as np
from bson.binary import Binary
import pickle
from pprint import pprint


def to_bin(nparr):
    return Binary(pickle.dumps(nparr, protocol=2), subtype=128)

def to_np(binary):
    return pickle.loads(binary)


# vec = np.random.random((2048))
# print(vec)
# bv = to_bin(vec)
# print(bv)
# print(to_np(bv))

client = pymongo.MongoClient('localhost', 27017)
db = client['mydb']
collection = db['mycol']

# collection.insert({
#     'a': 1, 'vec': bv
# })

cursor = collection.find(sort=[('_id', -1)], limit=100)
try:
    for doc in cursor:
        print(doc['_id'].generation_time)
        pprint(doc)
        print()

finally:
    cursor.close()
