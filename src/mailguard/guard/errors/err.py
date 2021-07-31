class NoRulesForTaskException(Exception):
    def __init__(self, message="at least one rule needs to be defined for task"):
        super().__init__(message)
        self.message = message


class NoValidActionFoundException(Exception):
    def __init__(self, message="rule at least has to have one valid action"):
        super().__init__(message)
        self.message = message
