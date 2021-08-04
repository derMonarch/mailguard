from mailguard.mail import commands
from mailguard.mail.errors import err
from mailguard.mail.mail_account import MailAccount


class MailControl:
    def __init__(
        self,
        account_id,
        connect_command=commands.MailBoxConnect,
        read_messages_command=commands.ReadMessages,
        delete_message_command=commands.DeleteMessage,
        move_message_command=commands.MoveMessage,
        close_conn_command=commands.MailBoxCloseConn,
    ):
        self.account_id = account_id
        self.account = None
        self.mailbox_conn = None
        self.connect_command = connect_command
        self.read_messages_command = read_messages_command
        self.delete_message_command = delete_message_command
        self.move_message_command = move_message_command
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
        self._check_connection()
        try:
            reader = self.read_messages_command(self.mailbox_conn)
            reader.execute(*args, **kwargs)
            return reader.get_data()
        except err.MailBoxConnectionStateException as ex:
            raise err.MailControlException(message=ex.message)

    def delete_message(self, *args, **kwargs):
        self._check_connection()
        self.delete_message_command(self.mailbox_conn).execute(*args, **kwargs)

    def move_message(self, *args, **kwargs):
        self._check_connection()
        mover = self.move_message_command(self.mailbox_conn)
        deleter = self.delete_message_command(self.mailbox_conn)
        try:
            if "copy" in kwargs and kwargs["copy"] is True:
                mover.execute(*args, **kwargs)
            else:
                mover.execute(*args, **kwargs)
                deleter.execute(*args, **kwargs)
        except err.MailMoveException as ex:
            raise err.MailControlException(message=ex.message)

    def forward_message(self, *args, **kwargs):
        """TODO: smtp"""

    def encrypt_message(self, *args, **kwargs):
        pass

    def close_mailbox(self, *args, **kwargs):
        self.close_conn_command(self.mailbox_conn).execute(*args, **kwargs)

    def _check_connection(self):
        if self.mailbox_conn is None:
            raise err.MailControlException(
                message="connection to mailbox needs to be established first"
            )
