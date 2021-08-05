from mailguard.tasks.models.task_model import TaskModel
from rest_framework import serializers


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskModel
        fields = [
            "account_id",
            "time_interval",
            "priority",
            "active",
            "state",
            "range",
            "message",
        ]
