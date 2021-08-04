import configparser

from django.test import TestCase

from mailguard.registration.models.account_model import AccountModel
from mailguard.tasks.models.task_model import TaskModel
from mailguard.mail.mail_control import MailControl
from mailguard.guard.guardian import Guardian
from mailguard.rules.services import task as task_rule

from tests.helper import rules


class GuardianTest(TestCase):
    """
    TODO: need to setup mails in mailaccount before tests (automated)
    TODO: or need mocked imap server
    TODO: need correct assertions
    """
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

    task = None

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

        self.task = TaskModel.objects.create(account_id=self.account_id,
                                             time_interval=5,
                                             priority=5,
                                             active=0)

    def test_guard_mailbox(self):
        task = TaskModel.objects.create(account_id=self.account_id,
                                        time_interval=5,
                                        priority=5,
                                        active=0)

        rules.add_rules_to_task_db(self.account_id, task)
        task_rule.add_rules_to_task(task)

        self._guard_mailbox(task)

    def test_guard_mailbox_delete_message(self):
        test_rule = {'ruleId': '1234',
                     'accountId': self.account_id,
                     'priority': 2,
                     'rule': {
                         'filters': {
                             'fromAddress': [
                                 'spam@yahoo.de',
                                 'mailings@produkt.gmx.net'
                             ]
                         },
                         'actions': {
                             'delete': True
                         }
                     }}

        rules.add_rules_to_task_db(self.account_id, self.task)
        rules.add_rule_to_task_db(self.account_id, self.task, test_rule)
        task_rule.add_rules_to_task(self.task)

        self._guard_mailbox(self.task)

    def test_guard_mailbox_move_message(self):
        """TODO: test for move message with copy and without delete"""
        test_rule = {'ruleId': '1234',
                     'accountId': self.account_id,
                     'priority': 2,
                     'rule': {
                         'filters': {
                             'fromAddress': [
                                 'spam@yahoo.de',
                                 'martin.weygandt@gmx.de'
                             ]
                         },
                         'actions': {
                             'moveTo': [
                                 'Firma'
                             ]
                         }
                     }}

        rules.add_rules_to_task_db(self.account_id, self.task)
        rules.add_rule_to_task_db(self.account_id, self.task, test_rule)
        task_rule.add_rules_to_task(self.task)

        self._guard_mailbox(self.task)

    def test_guard_mailbox_copy_message(self):
        test_rule = {'ruleId': '1234',
                     'accountId': self.account_id,
                     'priority': 2,
                     'rule': {
                         'filters': {
                             'fromAddress': [
                                 'spam@yahoo.de',
                                 'martin.weygandt@gmx.de'
                             ]
                         },
                         'actions': {
                             'copy': True
                         }
                     }}

        rules.add_rules_to_task_db(self.account_id, self.task)
        rules.add_rule_to_task_db(self.account_id, self.task, test_rule)
        task_rule.add_rules_to_task(self.task)

        self._guard_mailbox(self.task)

    def test_guard_mailbox_move_message_negative(self):
        test_rule = {'ruleId': '1234',
                     'accountId': self.account_id,
                     'priority': 2,
                     'rule': {
                         'filters': {
                             'fromAddress': [
                                 'spam@yahoo.de',
                                 'martin.weygandt@gmx.de'
                             ]
                         },
                         'actions': {
                             'moveTo': [
                                 'Nothing'
                             ]
                         }
                     }}

        rules.add_rules_to_task_db(self.account_id, self.task)
        rules.add_rule_to_task_db(self.account_id, self.task, test_rule)
        task_rule.add_rules_to_task(self.task)

        self._guard_mailbox(self.task)

        updated_task = TaskModel.objects.get(account_id=self.account_id)
        assert updated_task.state in "ERROR"
        assert updated_task.message in 'unable to move mail into folder: Nothing'

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

    def _guard_mailbox(self, task):
        mail_control = MailControl(self.account_id)
        guardian = Guardian(mail_control, task)
        guardian.guard_mailbox()

    def tearDown(self):
        AccountModel.objects.all().delete()
        TaskModel.objects.all().delete()
