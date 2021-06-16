from django.urls import path

from .views import account

urlpatterns = [
    # /api/v1/registrations/accounts
    path("accounts/", account.account_handler, name="add mail account"),
]
