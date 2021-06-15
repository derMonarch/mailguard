from rest_framework import serializers
from ..checks_model import ChecksModel


class ChecksSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChecksModel
        fields = ["account_id", "time_interval"]
