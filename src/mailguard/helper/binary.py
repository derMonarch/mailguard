import json


def decode_binary_to_dict(data):
    decoded_str = data.decode("utf8")
    return json.loads(decoded_str)


def decode_binary_dict_list(items):
    return [decode_binary_to_dict(item) for item in items]
