import mailparser

from mailguard.mail.errors.err import MailControlException
from mailguard.guard.rules import interpreter


class Guardian:
    def __init__(self, mail_control, task):
        self.mail_control = mail_control
        self.task = task
        self.rule_interpreter = interpreter.RuleInterpreter(self.mail_control, self.task)

    def guard_mailbox(self):
        """
        main method to start logic of mailbox cleanup and management. Be aware that mail_control methods can
        raise an exception
        """
        try:
            self.mail_control.init_control()
            messages = self.mail_control.read_messages()
            for key, message in messages.items():
                mail = mailparser.parse_from_bytes(message)
                self.rule_interpreter.interpret(mail)
        except MailControlException:
            self.task.state = "ERROR"
            self.task.save()

            if self.mail_control.mailbox_conn is not None:
                self.mail_control.close_mailbox()
