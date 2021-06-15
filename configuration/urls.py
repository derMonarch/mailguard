from django.urls import path
from .views import checks

urlpatterns = [
    # /api/v1/configurations/checks/
    path("checks/", checks.checks_handler, name="add mail account"),
]
