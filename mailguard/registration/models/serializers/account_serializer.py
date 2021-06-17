from rest_framework import serializers

from ..account_model import AccountModel


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountModel
        fields = ["account_id",
                  "mail_address",
                  "password",
                  "provider",
                  "imap",
                  "smtp",
                  "root_mailbox",
                  "sub_mailboxes",
                  "imap_port",
                  "smtp_port"]
