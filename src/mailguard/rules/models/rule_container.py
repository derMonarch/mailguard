from enum import Enum


class RuleType(Enum):
    FILTER = 1
    CONDITIONAL = 2


class SubRuleType(Enum):
    FROM_ADDRESS = 1
    WORDS = 2
    LINKS = 3
    CATEGORIES = 4
    SUBJECTS = 5
    SENTIMENT = 6
    BUZZWORDS = 7
    SUMMARY = 8


class Data:
    def __init__(self, rule_type, sub_rule_type=None, bool_and=False, bool_or=False, data=None):
        if data is None:
            data = []
        self.node_id = None
        self.rule_type = rule_type
        self.sub_rule_type = sub_rule_type
        self.bool_and = bool_and
        self.bool_or = bool_or
        self.data = data
