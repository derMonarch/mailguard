class CouldNotGetAccountException(Exception):
    def __init__(self, message="unable to get account"):
        super().__init__(message)
        self.message = message


class MailControlException(Exception):
    def __init__(self, message="error in MailControl"):
        super().__init__(message)
        self.message = message


class MailBoxConnectionException(Exception):
    def __init__(self, message="MailBox connection error"):
        super().__init__(message)
        self.message = message


class MailBoxConnectionStateException(Exception):
    def __init__(self, message="MailBox connection should be in state SELECTED"):
        super().__init__(message)
        self.message = message


class MailMoveException(Exception):
    def __init__(self, message="could not move mail into folder"):
        super().__init__(message)
        self.message = message
