from django.test import TestCase
from mailguard.tasks.models.task_model import TaskModel
from mailguard.rules.services import basic as rule_service
from mailguard.rules.models.rule_task_model import TaskToRuleModel
from mailguard.rules.services import task


class RuleGraphServiceTest(TestCase):
    account_id = "1234"

    def test_add_rules_to_task(self):
        created_task = TaskModel.objects.create(
            account_id=self.account_id,
            time_interval=5,
            priority=5
        )

        # TODO: use real rule data
        rule = rule_service.create_new_rule({'ruleId': None, 'something': 'data'})
        rule_two = rule_service.create_new_rule({'ruleId': None, 'something': 'another data'})

        TaskToRuleModel.objects.create(
            account_id=self.account_id,
            task_id=created_task.id,
            rule_id=rule['ruleId']
        )

        TaskToRuleModel.objects.create(
            account_id=self.account_id,
            task_id=created_task.id,
            rule_id=rule_two['ruleId']
        )

        task.add_rules_to_task(created_task)

        assert created_task.rules[0]['something'] in 'data'
        assert created_task.rules[1]['something'] in 'another data'
