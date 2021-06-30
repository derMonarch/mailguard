import uuid
import json

from mailguard.rules.database.redis import redis


def save_rule(rule):
    rule_id = uuid.uuid4().__str__()
    rule['ruleId'] = rule_id

    redis.set(rule_id, json.dumps(rule).encode('utf-8'))

    return rule


def get_rule(rule_id):
    return redis.get(rule_id)
