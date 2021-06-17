from mailguard.registration import controller as reg_controller
from .errors.err import CouldNotGetAccountException


class MailAccount:
    def __init__(self,
                 mail_address,
                 password,
                 imap,
                 smtp,
                 root_mailbox="INBOX",
                 sub_mailboxes=None,
                 imap_port=143,
                 smtp_port=465):

        self.mail_address = mail_address
        self.password = password
        self.imap = imap
        self.smtp = smtp
        self.root_mailbox = root_mailbox
        self.sub_mailboxes = sub_mailboxes
        self.imap_port = imap_port
        self.smtp_port = smtp_port

    @staticmethod
    def create(account_id):
        account = reg_controller.get_account_data(account_id)
        if account is None:
            raise CouldNotGetAccountException()
        return MailAccount(mail_address=account.mail_address,
                           password=account.password,
                           imap=account.imap,
                           smtp=account.smtp,
                           root_mailbox=account.root_mailbox,
                           sub_mailboxes=account.sub_mailboxes,
                           imap_port=account.imap_port,
                           smtp_port=account.smtp_port)
