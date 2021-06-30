import imaplib
from abc import ABC, abstractmethod

from .errors import err


class MailCommand(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def get_data(self):
        pass


class MailBoxConnect(MailCommand):
    def __init__(self, mail_account):
        self.mail_account = mail_account
        self.connection = None

    def execute(self):
        # noinspection PyBroadException
        try:
            mailbox = imaplib.IMAP4_SSL(
                host=self.mail_account.imap, port=self.mail_account.imap_port
            )
            mailbox.login(self.mail_account.mail_address, self.mail_account.password)
            if self.mail_account.root_mailbox is None or self.mail_account.root_mailbox in "N/A":
                mailbox.select()
            else:
                mailbox.select(mailbox=self.mail_account.root_mailbox)

            self.connection = mailbox

        except imaplib.IMAP4.error:
            raise err.MailBoxConnectionException("unable to connect to MailAccount")

    def get_data(self):
        return self.connection


class ReadMessages(MailCommand):
    def __init__(self, mailbox_conn):
        self.mailbox_conn = mailbox_conn
        self.messages = {}

    def execute(self):
        self.messages.clear()
        if self._check_connection_state():
            # TODO: what can I search?
            typ, data = self.mailbox_conn.search(None, "ALL")
            for num in data[0].split():
                typ, data = self.mailbox_conn.fetch(num, "(RFC822)")
                if typ in "OK":
                    self.messages[num] = data[0][1]
        else:
            raise err.MailBoxConnectionStateException()

    def get_data(self):
        return self.messages

    def _check_connection_state(self):
        if self.mailbox_conn.state in "SELECTED":
            return True


class MailBoxCloseConn(MailCommand):
    def __init__(self, mailbox_conn):
        self.mailbox_conn = mailbox_conn

    def execute(self):
        self.mailbox_conn.close()
        self.mailbox_conn.logout()

    def get_data(self):
        pass