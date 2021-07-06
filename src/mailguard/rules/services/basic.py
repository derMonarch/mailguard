from mailguard.rules.errors.services import WrongArgumentsException
from mailguard.rules.repositories import rule_repo


def create_new_rule(data):
    if not type(data) is dict:
        raise WrongArgumentsException(f"argument must be of type dict, got {type(data)}")

    return rule_repo.save_rule(data)
