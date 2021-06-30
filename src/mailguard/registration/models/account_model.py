from django.db import models


class AccountModel(models.Model):
    account_id = models.CharField(max_length=100)
    mail_address = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    provider = models.CharField(max_length=100)
    imap = models.CharField(max_length=50)
    smtp = models.CharField(max_length=50)
    root_mailbox = models.CharField(max_length=100, default="N/A")
    sub_mailboxes = models.CharField(max_length=400, default="N/A")
    imap_port = models.IntegerField(default=143)
    smtp_port = models.IntegerField(default=465)

    class Meta:
        db_table = "account"