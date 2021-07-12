import mailparser

from mailguard.mail.errors.err import MailControlException
from mailguard.guard.rules import interpreter
from mailguard.guard.rules.filter import BaseFilterCheck


class Guardian:
    def __init__(self, mail_control, task):
        self.mail_control = mail_control
        self.task = task
        self.rule_interpreter = interpreter.RuleInterpreter(self.mail_control, self.task, BaseFilterCheck())

    def guard_mailbox(self):
        """
        main method to start logic of mailbox cleanup and management. Be aware that mail_control methods can
        raise an exception
        """
        try:
            # TODO: need to act chunk wise, not per email
            # TODO: move into action/filter chunks and execute only once on all mails in chunk
            self.mail_control.init_control()
            messages = self.mail_control.read_messages()
            for key, message in messages.items():
                mail = mailparser.parse_from_bytes(message)
                mail.num = key
                self.rule_interpreter.interpret(mail)
        except MailControlException:
            self.task.state = "ERROR"
            self.task.save()

            if self.mail_control.mailbox_conn is not None:
                self.mail_control.close_mailbox()
