from mailguard.rules.repositories import rule_repo


def create_new_rule(data):
    """TODO: check if instance is dict, else throw error"""
    return rule_repo.save_rule(data)
