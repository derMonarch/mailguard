class ChunksManager:
    def __init__(self):
        self.delete = MailsToAction()
        self.move = {"N/A": MailsToAction()}
        self.copy = MailsToAction()

    def clear(self):
        self.delete.clear()
        self.copy.clear()
        self.move.clear()
        self.move["N/A"] = MailsToAction()

    def add_move(self, move_key):
        if move_key not in self.move:
            self.move[move_key] = MailsToAction()


class MailsToAction:
    def __init__(self):
        self.mails = []
        self.action_fn = None

    def clear(self):
        self.mails.clear()
        self.action_fn = None
