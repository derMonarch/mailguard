import configparser
import time

from django.test import TransactionTestCase
from mailguard.registration.models.account_model import AccountModel
from mailguard.tasks.models.task_model import TaskModel
from mailguard.runner.chief import MainRunner
from mailguard.tasks.services import tasks

from tests.helper import rules


class MainRunnerTest(TransactionTestCase):
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

    runner = MainRunner(tasks)

    def test_run(self):
        AccountModel.objects.create(account_id=self.account_id,
                                    mail_address=self.mail_address,
                                    password=self.password,
                                    provider=self.provider,
                                    imap=self.imap,
                                    smtp=self.smtp,
                                    imap_port=self.imap_port,
                                    smtp_port=self.smtp_port)

        created_task = TaskModel.objects.create(account_id=self.account_id,
                                                time_interval=3,
                                                priority=5,
                                                range='ALL')

        rules.add_rules_to_task_db(self.account_id, created_task)

        self.runner.run()
        time.sleep(6)

        updated_task = TaskModel.objects.get(account_id=self.account_id)

        assert updated_task.active == 1
        assert updated_task.state in "OK"

    def test_run_no_rules_found_for_task(self):
        AccountModel.objects.create(account_id=self.account_id_two,
                                    mail_address=self.mail_address,
                                    password=self.password,
                                    provider=self.provider,
                                    imap=self.imap,
                                    smtp=self.smtp,
                                    imap_port=self.imap_port,
                                    smtp_port=self.smtp_port)

        TaskModel.objects.create(account_id=self.account_id_two,
                                 time_interval=3,
                                 priority=5,
                                 range='ALL')

        self.runner.run()

        time.sleep(5)
        updated_task = TaskModel.objects.get(account_id=self.account_id_two)

        assert updated_task.state in 'ERROR'
        assert updated_task.message in 'at least one rule needs to be defined for task'

    def test_run_stop_error_jobs(self):
        pass

    def test_run_add_job_on_runtime(self):
        pass

    def tearDown(self):
        AccountModel.objects.all().delete()
        TaskModel.objects.all().delete()
