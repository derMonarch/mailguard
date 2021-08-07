from mailguard.guard.rules.constants import RuleFilterTypes


def from_address_check(filter_value, mail):
    """TODO: switch to regex"""
    from_address = mail.headers["From"]
    start_address = from_address.find("<") + 1
    end_address = from_address.find(">")

    address = from_address[start_address:end_address]

    return address in filter_value


class BaseFilterCheck:
    def __init__(self, from_address=from_address_check):
        self.from_address = from_address

    def check_filter(self, key, filter_value, mail):
        if key in RuleFilterTypes.from_address.value:
            return self.from_address(filter_value, mail)
        else:
            return False
