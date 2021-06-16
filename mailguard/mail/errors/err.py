class CouldNotCreateAccountException(Exception):

    def __init__(self, message="unable to get account"):
        super().__init__(message)
        self.message = message
