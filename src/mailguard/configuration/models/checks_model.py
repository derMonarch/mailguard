from django.db import models


class ChecksModel(models.Model):
    account_id = models.CharField(max_length=100)
    time_interval = models.IntegerField(default=0)

    class Meta:
        db_table = "checks"
