class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class RuleGraph:
    def __init__(self):
        self.graph = {}

    def add_node(self, node):
        """TODO: check for node type"""
        self.graph[node] = set()

    def add_edge(self, first, second):
        """TODO: check for node type"""
        first.next = second
        second.next = first
        self._add_if_missing(first)
        self._add_if_missing(second)

        self.graph[first].add(second)
        self.graph[second].add(first)

    def _add_if_missing(self, node):
        if not self._check_node_exists(node):
            self.add_node(node)

    def _check_node_exists(self, node):
        return node in self.graph
