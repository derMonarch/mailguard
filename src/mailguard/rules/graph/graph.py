from mailguard.rules.graph.validation import graph_validation


@graph_validation
class RuleGraph:
    def __init__(self):
        self.graph = {}

    def add_node(self, node):
        self.graph[node] = set()

    def add_edge(self, first, second):
        first.next = second
        second.previous = first
        self._add_if_missing(first)
        self._add_if_missing(second)

        self.graph[first].add(second)
        self.graph[second].add(first)

    def _add_if_missing(self, node):
        if not self._check_node_exists(node):
            self.add_node(node)

    def _check_node_exists(self, node):
        return node in self.graph
