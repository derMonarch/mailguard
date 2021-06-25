from django.urls import path
from .views import rule

urlpatterns = [
    # /api/v1/rules/tasks
    path("tasks/", rule.rules_handler, name="manage rules of task"),
]
