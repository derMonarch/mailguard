from mailguard.rules.repositories import rule_repo
from mailguard.rules.errors.services import WrongArgumentsException


def create_new_rule(data):
    if not type(data) is dict:
        raise WrongArgumentsException(f'argument must be of type dict, got {type(data)}')

    return rule_repo.save_rule(data)
