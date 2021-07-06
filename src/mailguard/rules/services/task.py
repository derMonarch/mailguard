from mailguard.helper import binary
from mailguard.rules.models.rule_model import TaskToRuleModel
from mailguard.rules.repositories import rule_repo


def add_rules_to_task(task):
    task_rules = TaskToRuleModel.objects.filter(account_id=task.account_id, task_id=task.id).all()
    task.rules = binary.decode_binary_dict_list(rule_repo.get_all_rules_for_task(task_rules))
