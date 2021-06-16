from .mail_account import MailAccount


class MailControl:

    def __init__(self, account_id):
        self.account_id = account_id
        self.account = None

    def init_control(self):
        self.account = MailAccount.create(self.account_id)
