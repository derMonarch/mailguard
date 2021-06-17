from django.test import TestCase
from mailguard.registration.models.account_model import AccountModel
from mailguard.mail.mail_control import MailControl
from mailguard.mail.errors import err


class MailControlTest(TestCase):
    account_id = "1234"
    account_id_two = "0123"
    mail_address = "cloudified.test@gmx.de"
    wrong_mail_address = "a@b"
    password = "TestIsMyLife"
    provider = "gmx"
    imap = "imap.gmx.net"
    smtp = "mail.gmx.net"
    imap_port = 993
    smtp_port = 587

    def setUp(self):
        AccountModel.objects.create(account_id=self.account_id,
                                    mail_address=self.mail_address,
                                    password=self.password,
                                    provider=self.provider,
                                    imap=self.imap,
                                    smtp=self.smtp,
                                    imap_port=self.imap_port,
                                    smtp_port=self.smtp_port)

    def test_init_control(self):
        control = MailControl(self.account_id)
        control.init_control()

    def test_init_control_negative(self):
        AccountModel.objects.create(account_id=self.account_id_two,
                                    mail_address=self.wrong_mail_address,
                                    password=self.password,
                                    provider=self.provider,
                                    imap=self.imap,
                                    smtp=self.smtp,
                                    imap_port=self.imap_port,
                                    smtp_port=self.smtp_port)

        with self.assertRaises(err.MailControlException):
            control = MailControl(self.account_id_two)
            control.init_control()

    def test_mailbox_connection_state(self):
        """when root_mailbox from AccountModel has a wrong value connection will not move into state SELECTED"""
        AccountModel.objects.create(account_id=self.account_id_two,
                                    mail_address=self.mail_address,
                                    password=self.password,
                                    provider=self.provider,
                                    imap=self.imap,
                                    smtp=self.smtp,
                                    root_mailbox="nothing",
                                    imap_port=self.imap_port,
                                    smtp_port=self.smtp_port)

        with self.assertRaises(err.MailBoxConnectionStateException):
            control = MailControl(self.account_id_two)
            control.init_control()
            control.read_messages()

    def test_read_messages(self):
        control = MailControl(self.account_id)
        control.init_control()
        control.read_messages()

