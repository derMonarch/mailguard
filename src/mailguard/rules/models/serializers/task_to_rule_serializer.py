from rest_framework import serializers
from mailguard.rules.models.rule_model import TaskToRuleModel


class TaskToRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskToRuleModel
        fields = [
            "account_id",
            "task_id",
            "rule_id",
        ]
