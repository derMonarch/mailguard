class RuleInterpreter:
    """
    TODO: tags filter and encryption not yet implemented
    """

    def __init__(self, mail_control, task, filter_check):
        self.mail_control = mail_control
        self.task = task
        self.filter_check = filter_check

    def interpret(self, mail):
        for rule in self.task.rules:
            self._check_filter(rule, mail)

    def _check_filter(self, rule, mail):
        filters = rule['rule']['filters']
        for key in filters.keys():
            if self.filter_check.check_filter(key, filters[key], mail):
                self._execute_action(rule, mail)

    def _execute_action(self, rule, mail):
        actions = rule['rule']['actions']
        for key in actions.keys():
            if key in 'delete':
                self.mail_control.delete_message(mail=mail)
            elif key in 'copy':
                pass
            elif key in 'moveTo':
                pass
            elif key in 'forward':
                pass
            elif key in 'encryption':
                pass
            else:
                pass
