from mailguard.registration.models.account_model import AccountModel


def get_account_data(account_id):
    """registered Account
    :arg account_id: str
    :return AccountModel or None
    """
    try:
        account = AccountModel.objects.get(account_id=account_id)
        return account
    except AccountModel.DoesNotExist:
        return None
