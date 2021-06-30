import json


def get_dict(data):
    decoded_str = data.content.decode('utf8')
    return json.loads(decoded_str)
