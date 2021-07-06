from mailguard.rules.graph.validation import graph_validation


@graph_validation
class RuleGraph:
    """
    TODO: serialization of graph
    TODO: get operator
    TODO: validation
    """

    def __init__(self, graph=None):
        if graph is None:
            self.graph = {}
        else:
            self.graph = graph

    def add_node(self, node):
        """validation: checks whether node has correct type, if not raises NodeTypeException"""
        self.graph[node] = set()

    def add_edge(self, first, second):
        self._add_if_missing(first)
        self._add_if_missing(second)

        self.graph[first].add(second)
        self.graph[second].add(first)

    def get_all_edges(self, node):
        return self.graph[node]

    def _add_if_missing(self, node):
        if not self._check_node_exists(node):
            self.add_node(node)

    def _check_node_exists(self, node):
        return node in self.graph
