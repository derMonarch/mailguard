from .mail_account import MailAccount
from mailguard.mail.errors import err
from . import commands


class MailControl:

    def __init__(self, account_id):
        self.account_id = account_id
        self.account = None
        self.mailbox_conn = None

    def init_control(self):
        try:
            self.account = MailAccount.create(self.account_id)
            connect = commands.MailBoxConnect(self.account)
            connect.execute()
            self.mailbox_conn = connect.get_data()

        except (err.CouldNotGetAccountException, err.MailBoxConnectionException) as ex:
            raise err.MailControlException(message=ex.message)

    def read_messages(self):
        if self.mailbox_conn is None:
            raise err.MailControlException(message="connection to mailbox needs to be established first")
        try:
            reader = commands.ReadMessages(self.mailbox_conn)
            reader.execute()
        except err.MailBoxConnectionStateException as ex:
            raise err.MailControlException(message=ex.message)

    def close_mailbox(self):
        closer = commands.MailBoxCloseConn(self.mailbox_conn)
        closer.execute()
