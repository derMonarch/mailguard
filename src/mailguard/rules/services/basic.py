from mailguard.rules.repositories import rule_repo


def create_new_rule(data):
    return rule_repo.save_rule(data)
