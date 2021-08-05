from mailguard.rules.models.rule_task_model import TaskToRuleModel
from rest_framework import serializers


class TaskToRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskToRuleModel
        fields = [
            "account_id",
            "task_id",
            "rule_id",
        ]
