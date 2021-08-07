import mailparser

from mailguard.guard.rules.constants import RuleActionTypes
from mailguard.guard.errors.err import (NoRulesForTaskException,
                                        NoValidActionFoundException)


class RuleInterpreter:
    """
    TODO: only mail address filter implemented yet
    """

    def __init__(self, mail_control, task, filter_check):
        self.mail_control = mail_control
        self.task = task
        self.filter_check = filter_check
        self.action_chunks = {
            'delete': set(),
            'move': set(),
            'move_copy': set(),
            'copy': set()
        }

    def interpret(self, mails):
        self._clear_chunks()

        if not self.task.rules:
            raise NoRulesForTaskException()

        # TODO: performance bottleneck
        for rule in self.task.rules:
            for key, mail_bytes in mails.items():
                mail = mailparser.parse_from_bytes(mail_bytes)
                mail.num = key

                self._check_filter(rule, mail)

        return self.action_chunks

    def _check_filter(self, rule, mail):
        filters = rule["rule"]["filters"]
        for key in filters.keys():
            if self.filter_check.check_filter(key, filters[key], mail):
                self._execute_action(rule, mail)

    def _execute_action(self, rule, mail):
        self._fill_action_chunks(rule, mail)

    def _fill_action_chunks(self, rule, mail):
        actions = rule["rule"]["actions"]

        for key in actions.keys():
            if key in RuleActionTypes.delete.value:
                delete_fn = self.mail_control.delete_message()
                self.action_chunks['delete'].add(delete_fn)
            elif key in RuleActionTypes.move_to.value:
                for move_to in actions[key]:
                    if "copy" in actions and actions["copy"] is True:
                        move_fn = self.mail_control.move_message(
                           dest=move_to, copy=True
                        )
                        self.action_chunks['move_copy'].add(move_fn)
                    else:
                        move_fn = self.mail_control.move_message(dest=move_to)
                        self.action_chunks['move'].add(move_fn)
            elif key in RuleActionTypes.copy.value:
                copy_fn = self.mail_control.move_message(mail=mail, dest="inbox", copy=True)
                self.action_chunks['copy'].add(copy_fn)
            elif key in RuleActionTypes.forward.value:
                pass
            elif key in RuleActionTypes.encryption.value:
                pass
            else:
                raise NoValidActionFoundException()

    def _clear_chunks(self):
        for value in self.action_chunks.values():
            value.clear()
