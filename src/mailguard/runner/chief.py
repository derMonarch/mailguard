import logging

from apscheduler.schedulers.background import BackgroundScheduler

from mailguard.guard.guardian import Guardian
from mailguard.mail.mail_control import MailControl
from mailguard.rules.services import task as task_rules

logger = logging.getLogger(__name__)


class Runner:
    def __init__(self, task_service, scheduler):
        self._jobs = {}
        self.task_service = task_service
        self.scheduler = scheduler

        self.scheduler.start()

    def get_all_tasks(self):
        return self.task_service.get_all()

    def remove_task(self, task_id):
        self.task_service.remove_task(task_id)

    def add_scheduler_job(self, guardian, seconds):
        # TODO: may need to init connection once and then run scheduled guard on mailbox
        # TODO: what happens when second task (1 sec) is started besides old task sill running?
        self._jobs[str(guardian.task.id)] = self.scheduler.add_job(
            guardian.guard_mailbox, "interval", seconds=seconds
        )

    def add_manager_job(self, job, seconds):
        self._jobs["manager"] = self.scheduler.add_job(job, "interval", seconds=seconds)

    def remove_scheduled_job(self, task):
        self.scheduler.remove_job(self._jobs[str(task.id)].id)


class MainRunner(Runner):
    def __init__(self, task_service, scheduler=BackgroundScheduler()):
        super().__init__(task_service, scheduler)

    def run(self):
        tasks = self.get_all_tasks()
        for task in tasks:
            if task.active == 0:
                self._start_task(task)
                self.add_manager_job(job=self.check_on_runtime, seconds=30)

    def stop(self):
        pass

    def check_on_runtime(self):
        inactive_tasks = self.task_service.get_inactive_tasks()
        for task in inactive_tasks:
            self._start_task(task)

        error_tasks = self.task_service.get_state_error_tasks()
        for error_task in error_tasks:
            self.remove_scheduled_job(error_task)

    def _start_task(self, task):
        logger.info("runner.task.start", extra={"task_id": task.id})
        mail_control = MailControl(task.account_id)
        task_rules.add_rules_to_task(task)
        guardian = Guardian(mail_control, task)
        self.add_scheduler_job(guardian, task.time_interval)

        task.active = 1
        task.save()
