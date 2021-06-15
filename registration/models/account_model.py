from django.db import models


class AccountModel(models.Model):
    account_id = models.CharField(max_length=100)
    mail_address = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    provider = models.CharField(max_length=100)
    imap = models.CharField(max_length=50)
    smtp = models.CharField(max_length=50)

    class Meta:
        db_table = "account"
