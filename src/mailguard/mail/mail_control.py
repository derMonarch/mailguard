from mailguard.mail.errors import err

from .commands import MailBoxCloseConn, MailBoxConnect, ReadMessages
from .mail_account import MailAccount


class MailControl:
    def __init__(
        self,
        account_id,
        connect_command=MailBoxConnect,
        read_messages_command=ReadMessages,
        close_conn_command=MailBoxCloseConn,
    ):
        self.account_id = account_id
        self.account = None
        self.mailbox_conn = None
        self.connect_command = connect_command
        self.read_messages_command = read_messages_command
        self.close_conn_command = close_conn_command

    def init_control(self, *args, **kwargs):
        try:
            self.account = MailAccount.create(self.account_id)
            connect = self.connect_command(self.account)
            connect.execute(*args, **kwargs)
            self.mailbox_conn = connect.get_data()

        except (err.CouldNotGetAccountException, err.MailBoxConnectionException) as ex:
            raise err.MailControlException(message=ex.message)

    def read_messages(self, *args, **kwargs):
        if self.mailbox_conn is None:
            raise err.MailControlException(
                message="connection to mailbox needs to be established first"
            )
        try:
            reader = self.read_messages_command(self.mailbox_conn)
            reader.execute(*args, **kwargs)
            return reader.get_data()
        except err.MailBoxConnectionStateException as ex:
            raise err.MailControlException(message=ex.message)

    def delete_message(self, *args, **kwargs):
        pass

    def move_message(self, *args, **kwargs):
        pass

    def forward_message(self, *args, **kwargs):
        pass

    def encrypt_message(self, *args, **kwargs):
        pass

    def close_mailbox(self, *args, **kwargs):
        closer = self.close_conn_command(self.mailbox_conn)
        closer.execute(*args, **kwargs)
