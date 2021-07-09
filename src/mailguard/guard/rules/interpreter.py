class RuleInterpreter:
    """
    TODO: tags filter and encryption not yet implemented
    """

    def __init__(self, mail_control, task):
        self.mail_control = mail_control
        self.task = task

    def interpret(self, mail):
        for rule in self.task.rules:
            print('yeeelo')

    def _execute_action(self, rule):
        actions = rule['rule']['actions']
        for key in actions.keys():
            if key in 'delete':
                pass
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
