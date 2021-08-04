import logging
import imaplib

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
        """
        TODO: may need to init connection once and then run scheduled guard on mailbox
        TODO: what happens when same task is started again besides old task sill running?
        """
        self._jobs[str(guardian.task.id)] = self.scheduler.add_job(
            guardian.guard_mailbox, "interval", seconds=seconds
        )

    def add_manager_job(self, job, seconds):
        self._jobs["manager"] = self.scheduler.add_job(job, "interval", seconds=seconds)

    def remove_scheduled_job(self, task):
        self.scheduler.remove_job(self._jobs[str(task.id)].id)
        del self._jobs[str(task.id)]

    def clear_job_overview(self):
        self._jobs.clear()


class MainRunner(Runner):
    def __init__(self, task_service, scheduler=BackgroundScheduler()):
        super().__init__(task_service, scheduler)
        self.guardians = []

    def run(self, manager_job_interval=30):
        self.clear_job_overview()
        self.guardians.clear()

        tasks = self.get_all_tasks()
        for task in tasks:
            if task.active == 0:
                self._start_task(task)

        self.add_manager_job(job=self.check_on_runtime, seconds=manager_job_interval)

    def stop(self):
        # noinspection PyBroadException
        try:
            for guard in self.guardians:
                guard.mail_control.close_mailbox()
        except imaplib.IMAP4.error:
            pass

        self.scheduler.shutdown()

    def check_on_runtime(self):
        inactive_tasks = self.task_service.get_inactive_tasks()
        for task in inactive_tasks:
            self._start_task(task)

        error_tasks = self.task_service.get_state_error_tasks()
        for error_task in error_tasks:
            if error_task.active == 1:
                self.remove_scheduled_job(error_task)
                error_task.active = 0
                error_task.save()

    def _start_task(self, task):
        logger.info("runner.task.start", extra={"task_id": task.id})
        mail_control = MailControl(task.account_id)
        task_rules.add_rules_to_task(task)
        guardian = Guardian(mail_control, task)
        self.guardians.append(guardian)
        self.add_scheduler_job(guardian, task.time_interval)

        task.active = 1
        task.save()
