import uuid

from mailguard.helper import serialization
from mailguard.rules.database.redis import redis


def save_rule(rule):
    rule_id = uuid.uuid4().__str__()
    rule["ruleId"] = rule_id

    redis.set(rule_id, serialization.serialize_object(rule))

    return rule


def get_rule(rule_id):
    return redis.get(rule_id)


def get_all_rules_for_task(task_to_rules):
    pipe = redis.pipeline()
    for task_rule in task_to_rules:
        pipe.get(task_rule.rule_id)

    return pipe.execute()
