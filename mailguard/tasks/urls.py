from django.urls import path
from .views import tasks


urlpatterns = [
    # /api/v1/tasks
    path("", tasks.tasks_handler, name="manage tasks"),
]
