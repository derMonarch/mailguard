import imaplib
import logging
import mailparser

from apscheduler.schedulers.background import BackgroundScheduler
from mailguard.guard.guardian import Guardian
from mailguard.mail.mail_control import MailControl
from mailguard.rules.services import task as task_rules
from mailguard.mail.errors import err

logger = logging.getLogger(__name__)


class Runner:
    def __init__(self, task_service, scheduler):
        self._jobs = {}
        self.task_service = task_service
        self.scheduler = scheduler

    def add_scheduler_job(self, guardian, seconds):
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

    @property
    def manager_active(self):
        return "manager" in self._jobs.keys()

    @property
    def jobs(self):
        return self._jobs


class MainRunner(Runner):
    def __init__(self, task_service, scheduler=BackgroundScheduler()):
        super().__init__(task_service, scheduler)
        self.guardians = []

    def run(self, manager_job_interval=30):
        self.clear_job_overview()
        self.guardians.clear()

        if not self.scheduler.running:
            self.scheduler.start()
            self.add_manager_job(
                job=self.check_on_runtime, seconds=manager_job_interval
            )

        if not self.manager_active:
            self.add_manager_job(
                job=self.check_on_runtime, seconds=manager_job_interval
            )

        tasks = self.task_service.get_inactive_tasks()
        for task in tasks:
            self._start_task(task)

    def stop(self):
        # noinspection PyBroadException
        try:
            for guard in self.guardians:
                guard.mail_control.close_mailbox()
        except imaplib.IMAP4.error:
            pass

        for active_task in self.task_service.get_all_active_tasks():
            active_task.active = 0
            active_task.save()

        self.scheduler.shutdown()

    @staticmethod
    def add_rules_on_runtime(task):
        """
        TODO: update rules in database (check if there are any updates)
              and set task to restart (if there are any updates, if not dont restart)
        """
        try:
            mail_control = MailControl(task.account_id)
            mail_control.init_control(folder="mailguard")

            mails = mail_control.read_messages(range="ALL")
            for mail in mails.values():
                parsed_mail = mailparser.parse_from_bytes(mail)
                if parsed_mail.mail["from"] and len(parsed_mail.mail["from"][0]) > 1:
                    mail_address = parsed_mail.mail["from"][0][1]
                print("YEELO")
        except err.MailControlException as ex:
            print(ex.message)

    def check_on_runtime(self):
        """TODO: get state restart tasks, remove them from scheduler and add again"""
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
