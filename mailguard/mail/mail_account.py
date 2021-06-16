from mailguard.registration import controller as reg_controller
from .errors.err import CouldNotCreateAccountException


class MailAccount:
    def __init__(self, mail_address, password, imap, smtp):
        self.mail_address = mail_address
        self.password = password
        self.imap = imap
        self.smtp = smtp

    @staticmethod
    def create(account_id):
        account = reg_controller.get_account_data(account_id)
        if account is None:
            raise CouldNotCreateAccountException()
        return MailAccount(mail_address=account.mail_address,
                           password=account.password,
                           imap=account.imap,
                           smtp=account.smtp)
