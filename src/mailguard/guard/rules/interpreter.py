import mailparser
from mailguard.guard.errors.err import (NoRulesForTaskException,
                                        NoValidActionFoundException)
from mailguard.guard.rules import executor
from mailguard.guard.rules.chunks import ChunksManager
from mailguard.guard.rules.constants import RuleActionTypes


class RuleInterpreter:
    """
    TODO: only mail address filter implemented yet
    """

    def __init__(self, mail_control, task, filter_check, action_executor=executor):
        self.mail_control = mail_control
        self.task = task
        self.filter_check = filter_check
        self.action_executor = action_executor
        self.action_chunks = ChunksManager()

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

        self.action_executor.execute_from_chunks(self.action_chunks)

    def _check_filter(self, rule, mail):
        filters = rule["rule"]["filters"]
        for key in filters.keys():
            if self.filter_check.check_filter(key, filters[key], mail):
                self._fill_action_chunks(rule, mail)

    def _fill_action_chunks(self, rule, mail):
        actions = rule["rule"]["actions"]

        for key in actions.keys():
            if key in RuleActionTypes.delete.value:
                delete_fn = self.mail_control.delete_message()
                self.action_chunks.delete.mails.append(mail.num)
                self.action_chunks.delete.action_fn = delete_fn
            elif key in RuleActionTypes.move_to.value:
                for move_to in actions[key]:
                    if "copy" in actions and actions["copy"] is True:
                        move_key = f"move_{move_to}"
                        move_fn = self.mail_control.move_message(
                            dest=move_to, copy=True
                        )
                        self._add_move_chunk(move_key, move_fn, mail)
                    else:
                        move_key = f"move_{move_to}"
                        move_fn = self.mail_control.move_message(dest=move_to)
                        self._add_move_chunk(move_key, move_fn, mail)
            elif key in RuleActionTypes.copy.value:
                copy_fn = self.mail_control.move_message(dest="inbox", copy=True)
                self.action_chunks.copy.mails.append(mail.num)
                self.action_chunks.copy.action_fn = copy_fn
            elif key in RuleActionTypes.forward.value:
                pass
            elif key in RuleActionTypes.encryption.value:
                pass
            else:
                raise NoValidActionFoundException()

    def _clear_chunks(self):
        return self.action_chunks.clear()

    def _add_move_chunk(self, move_key, move_fn, mail):
        self.action_chunks.add_move(move_key)
        self.action_chunks.move[move_key].mails.append(mail.num)
        self.action_chunks.move[move_key].action_fn = move_fn
