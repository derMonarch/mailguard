from enum import Enum


class RuleActionTypes(str, Enum):
    delete = "delete"
    copy = "copy"
    move_to = "moveTo"
    forward = "forward"
    encryption = "encryption"


class RuleFilterTypes(str, Enum):
    from_address = "fromAddress"
    words = "words"
    links = "links"
    tags = "tags"
