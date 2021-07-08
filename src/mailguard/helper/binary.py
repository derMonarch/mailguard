import json


def decode_binary_to_dict(data):
    decoded_str = data.decode("utf8")
    return json.loads(decoded_str)


def decode_binary_dict_rule_list(items):
    rules_list = [decode_binary_to_dict(item) for item in items]
    return sorted(rules_list, key=lambda rule: rule["priority"])
