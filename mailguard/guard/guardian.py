from mailguard.mail.errors.err import MailControlException


class Guardian:
    def __init__(self, mail_control, rule_container=None):
        self.mail_control = mail_control
        self.rule_container = rule_container

    def guard_mailbox(self):
        """
        main method to start logic of mailbox cleanup and management. Be aware that mail_control methods can
        raise an exception
        """
        try:
            self.mail_control.init()
            messages = self.mail_control.read_messages()
        except MailControlException:
            # TODO: set state in tasks table, maybe restart job?
            pass
