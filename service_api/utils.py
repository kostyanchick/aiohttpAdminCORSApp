from bson.objectid import ObjectId
from json import JSONEncoder


class CustomJSONEncoder(JSONEncoder):

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return JSONEncoder.default(self, o)
