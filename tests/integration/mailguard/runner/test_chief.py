import configparser

from django.test import TestCase
from mailguard.registration.models.account_model import AccountModel
from mailguard.tasks.models.task_model import TaskModel
from mailguard.runner.chief import MainRunner
from mailguard.tasks.services import tasks

from tests.helper import rules


class MainRunnerTest(TestCase):
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

    # TODO: tests need to check if rules have been added to task, and task is in right state

    def setUp(self):
        AccountModel.objects.create(account_id=self.account_id,
                                    mail_address=self.mail_address,
                                    password=self.password,
                                    provider=self.provider,
                                    imap=self.imap,
                                    smtp=self.smtp,
                                    imap_port=self.imap_port,
                                    smtp_port=self.smtp_port)

        created_task = TaskModel.objects.create(account_id=self.account_id,
                                                time_interval=5,
                                                priority=5)

        rules.add_rules_to_task_db(self.account_id, created_task)

    def test_run(self):
        runner = MainRunner(tasks)
        runner.run()

        updated_task = TaskModel.objects.get(account_id=self.account_id)
        assert updated_task.active == 1
        assert updated_task.state in "OK"

    def tearDown(self):
        AccountModel.objects.all().delete()
        TaskModel.objects.all().delete()
