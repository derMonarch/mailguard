from django.test import TestCase
from mailguard.registration.models.account_model import AccountModel
from mailguard.registration import controller


class ControllerTest(TestCase):
    account_id = "1234"
    wrong_account_id = "000"
    mail_address = "a@b"

    def setUp(self):
        AccountModel.objects.create(account_id=self.account_id, mail_address=self.mail_address)

    def test_get_account_data(self):
        account = controller.get_account_data(self.account_id)
        assert account.account_id == self.account_id
        assert account.mail_address == self.mail_address

    def test_get_account_data_negative(self):
        account = controller.get_account_data(self.wrong_account_id)
        assert account is None

    def tearDown(self):
        AccountModel.objects.all().delete()
