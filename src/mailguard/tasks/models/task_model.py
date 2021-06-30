from django.db import models


class TaskModel(models.Model):
    account_id = models.CharField(max_length=100)
    time_interval = models.IntegerField(default=0)
    priority = models.IntegerField(default=10)
    active = models.BooleanField(default=0)
    state = models.CharField(max_length=50, default="OK")

    class Meta:
        db_table = "tasks"
