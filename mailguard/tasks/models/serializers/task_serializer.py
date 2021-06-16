from rest_framework import serializers
from ..task_model import TaskModel


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskModel
        fields = ["account_id", "time_interval", "priority"]
