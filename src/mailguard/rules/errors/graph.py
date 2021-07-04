class NodeTypeException(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class EdgeException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)