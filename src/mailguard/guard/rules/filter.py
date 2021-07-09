from enum import Enum


class FilterType(str, Enum):
    from_address = 'fromAddress'
    words = 'words'
    links = 'links'
    tags = 'tags'


def from_address_check(mail):
    pass


class BaseFilterCheck:
    def __init__(self, from_address=from_address_check):
        self.from_address = from_address

    def check_filter(self, key, mail):
        if key is FilterType.from_address:
            return self.from_address(mail)
        else:
            return False
