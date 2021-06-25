from django.db import models


class TaskToRuleModel(models.Model):
    account_id = models.CharField(max_length=100)
    task_id = models.IntegerField(default=0)
    rule_id = models.CharField(max_length=50, default="N/A")

    class Meta:
        db_table = "task_rules"
        app_label = 'mailguard.rules'
