import json


def serialize_object(obj):
    return json.dumps(obj, default=lambda o: o.__dict__)
