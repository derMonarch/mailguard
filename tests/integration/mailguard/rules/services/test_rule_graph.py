from django.test import TestCase
from mailguard.tasks.models.task_model import TaskModel
from mailguard.rules.services import basic as rule_service
from mailguard.rules.models.rule_model import TaskToRuleModel
from mailguard.rules.services import rule_graph


class RuleGraphServiceTest(TestCase):
    account_id = "1234"

    def test_add_rules_to_task(self):
        task = TaskModel.objects.create(
            account_id=self.account_id,
            time_interval=5,
            priority=5
        )

        # TODO: use real rule data
        rule = rule_service.create_new_rule({'ruleId': None, 'something': 'data'})
        rule_two = rule_service.create_new_rule({'ruleId': None, 'something': 'another data'})

        TaskToRuleModel.objects.create(
            account_id=self.account_id,
            task_id=task.id,
            rule_id=rule['ruleId']
        )

        TaskToRuleModel.objects.create(
            account_id=self.account_id,
            task_id=task.id,
            rule_id=rule_two['ruleId']
        )

        rule_graph.add_rules_to_task(task)

        assert task.rules[0]['something'] in 'data'
        assert task.rules[1]['something'] in 'another data'
