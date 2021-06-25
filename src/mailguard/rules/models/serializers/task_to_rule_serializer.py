from rest_framework import serializers
from ..task_to_rule_model import TaskToRuleModel


class TaskToRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskToRuleModel
        fields = [
            "account_id",
            "task_id",
            "rule_id",
        ]
