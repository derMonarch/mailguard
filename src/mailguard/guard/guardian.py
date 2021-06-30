import mailparser

from mailguard.mail.errors.err import MailControlException


class Guardian:
    def __init__(self, mail_control, task, rule_container=None):
        self.mail_control = mail_control
        self.task = task
        self.rule_container = rule_container

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
                print("WOOOW")
        except MailControlException:
            self.task.state = "ERROR"
            self.task.save()

            if self.mail_control.mailbox_conn is not None:
                self.mail_control.close_mailbox()
