from apscheduler.schedulers.background import BackgroundScheduler
from mailguard.guard.guardian import Guardian
from mailguard.mail.mail_control import MailControl


class Runner:

    def __init__(self, task_controller, scheduler=BackgroundScheduler()):
        self._task_list = []
        self._guardians = []
        self.task_controller = task_controller
        self.scheduler = scheduler

        self.scheduler.start()

    def get_all_tasks(self):
        return self.task_controller.get_all()

    def remove_task(self, task_id):
        self.task_controller.remove(task_id)

    def add_scheduler_job(self, guardian, seconds):
        self._guardians.append(guardian)
        self.scheduler.add_job(guardian.guard_mailbox, 'interval', seconds=seconds)


class MainRunner(Runner):

    def __init__(self, task_controller):
        super().__init__(task_controller)

    def run(self):
        tasks = self.get_all_tasks()
        for task in tasks:
            mail_control = MailControl(task.account_id)
            guardian = Guardian(mail_control)
            self.add_scheduler_job(guardian, task.time_interval)
