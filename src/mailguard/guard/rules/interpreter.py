class RuleInterpreter:
    """
    1. check filter in rules (rules sorted by priority)
    2. execute action in rule which applies first
    TODO: tags filter not yet implemented
    """

    def __init__(self, mail_control, task):
        self.mail_control = mail_control
        self.task = task

    def execute(self, message):
        pass

    def _get_action_by_filter(self, message):
        pass
