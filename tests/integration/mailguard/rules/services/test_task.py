from django.test import TestCase
from mailguard.tasks.models.task_model import TaskModel
from mailguard.rules.services import basic as rule_service
from mailguard.rules.models.rule_task_model import TaskToRuleModel
from mailguard.rules.services import task
from tests.helper import rules


class RuleGraphServiceTest(TestCase):
    account_id = "1234"

    def test_add_rules_to_task(self):
        created_task = TaskModel.objects.create(
            account_id=self.account_id,
            time_interval=5,
            priority=5
        )

        rule = rule_service.create_new_rule(rules.new_rule(priority=1))
        rule_two = rule_service.create_new_rule(rules.new_rule(priority=3))
        rule_three = rule_service.create_new_rule(rules.new_rule(priority=5))

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

        TaskToRuleModel.objects.create(
            account_id=self.account_id,
            task_id=created_task.id,
            rule_id=rule_three['ruleId']
        )

        task.add_rules_to_task(created_task)

        assert created_task.rules[0]['ruleId'] is not None
        assert created_task.rules[0]['priority'] == 1
        assert created_task.rules[1]['ruleId'] is not None
        assert created_task.rules[1]['priority'] == 3
        assert created_task.rules[2]['ruleId'] is not None
        assert created_task.rules[2]['priority'] == 5
