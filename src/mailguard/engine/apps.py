from django.apps import AppConfig

from mailguard.runner.chief import MainRunner
from mailguard.tasks.services import tasks


class EngineConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "mailguard.engine"

    def ready(self):
        runner = MainRunner(tasks)
        runner.run()
