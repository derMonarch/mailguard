import configparser

from django.test import TestCase

from mailguard.registration.models.account_model import AccountModel
from mailguard.tasks.models.task_model import TaskModel
from mailguard.mail.mail_control import MailControl
from mailguard.guard.guardian import Guardian
from mailguard.rules.services import task as task_rule

from tests.helper import rules


class GuardianTest(TestCase):
    config = configparser.ConfigParser()
    config.read('tests/resources/account.ini')

    account_id = "1234"
    account_id_two = "0123"
    mail_address = config['mail.account']['ADDRESS']
    wrong_mail_address = "a@b"
    password = config['mail.account']['PASSWORD']
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

        AccountModel.objects.create(account_id=self.account_id_two,
                                    mail_address=self.mail_address,
                                    password="wrong",
                                    provider=self.provider,
                                    imap=self.imap,
                                    smtp=self.smtp,
                                    imap_port=self.imap_port,
                                    smtp_port=self.smtp_port)

    def test_guard_mailbox(self):
        task = TaskModel.objects.create(account_id=self.account_id,
                                        time_interval=5,
                                        priority=5,
                                        active=0)

        rules.add_rules_to_task_db(self.account_id, task)
        task_rule.add_rules_to_task(task)

        mail_control = MailControl(self.account_id)
        guardian = Guardian(mail_control, task)
        guardian.guard_mailbox()

    def test_guard_mailbox_negative(self):
        task = TaskModel.objects.create(account_id=self.account_id_two,
                                        time_interval=5,
                                        priority=5,
                                        active=0)

        mail_control = MailControl(self.account_id_two)
        guardian = Guardian(mail_control, task)
        guardian.guard_mailbox()

        updated_task = TaskModel.objects.get(account_id=self.account_id_two)
        assert updated_task.state in "ERROR"

    def tearDown(self):
        AccountModel.objects.all().delete()
        TaskModel.objects.all().delete()
