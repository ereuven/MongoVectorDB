__all__ = ['MongoModel']

from bson import ObjectId


class MongoModel(dict):
    """
    A simple model that wraps mongodb document
    """
    __getattr__ = dict.get
    __delattr__ = dict.__delitem__
    __setattr__ = dict.__setitem__

    def load(self, collection, object_id, clear=True):
        oid = object_id
        if not isinstance(oid, ObjectId):
            oid = ObjectId(oid)

        if clear:
            self.clear()

        self.update(collection.find_one({"_id": oid}))

    def save(self, collection):
        if not self._id:
            collection.insert(self)
        else:
            collection.update(
                { "_id": ObjectId(self._id) }, self)

    def reload(self, collection):
        if self._id:
            self.update(collection.find_one({"_id": ObjectId(self._id)}))

    def remove(self, collection):
        if self._id:
            collection.remove({"_id": ObjectId(self._id)})
            self.clear()
