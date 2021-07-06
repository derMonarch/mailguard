import networkx as nx


class RuleGraph:

    def __init__(self, rule_id, graph=None):
        if graph is None:
            self.graph = nx.Graph()
        else:
            self.graph = graph

        self.rule_id = rule_id

    def __getitem__(self, key):
        pass

    def add_node(self, node):
        pass

    def add_edge(self, first, second):
        pass

    def get_all_edges(self, node):
        pass

