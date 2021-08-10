from mailguard.guard.errors.err import (NoRulesForTaskException,
                                        NoValidActionFoundException)
from mailguard.guard.rules import interpreter
from mailguard.guard.rules.filter import BaseFilterCheck
from mailguard.mail.errors.err import MailControlException


class Guardian:
    def __init__(self, mail_control, task):
        self.mail_control = mail_control
        self.task = task
        self.rule_interpreter = interpreter.RuleInterpreter(
            self.mail_control, self.task, BaseFilterCheck()
        )

    def guard_mailbox(self):
        """
        main method to start logic of mailbox cleanup and management. Be aware that mail_control methods can
        raise an exception
        """
        try:
            self.mail_control.init_control()
            mails = self.mail_control.read_messages(range=self.task.range)
            self.rule_interpreter.interpret(mails)
        except (
            MailControlException,
            NoRulesForTaskException,
            NoValidActionFoundException,
        ) as ex:
            self.task.state = "ERROR"
            self.task.message = ex.message
            self.task.save()

            if self.mail_control.mailbox_conn is not None:
                self.mail_control.close_mailbox()
