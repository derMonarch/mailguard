from enum import Enum


class RuleType(Enum):
    RULE_ROOT = 1
    FILTER = 2
    TAG = 3
    ACTION = 4
    CONDITIONAL = 5


class Data:
    def __init__(self, rule_type, bool_and=False, bool_or=False, data=None):
        if data is None:
            data = []
        self.rule_type = rule_type
        self.bool_and = bool_and
        self.bool_or = bool_or
        self.data = data
