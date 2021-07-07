import json

import networkx as nx

from mailguard.helper import id as id_generator


def generate_node_id(func):
    def wrapper(*args):
        for arg in args:
            arg.node_id = id_generator.get_uuid_as_str()
        func(*args)
        return args

    return wrapper


class RuleGraph:
    def __init__(self, rule_id=None, graph=None):
        if graph is None:
            self.graph = nx.Graph()
        else:
            self.graph = graph

        self.rule_id = rule_id

    def __getitem__(self, key):
        return self.graph[key]

    @generate_node_id
    def add_node(self, node):
        self.graph.add_node(node)

    @generate_node_id
    def add_edge(self, first, second):
        self.graph.add_edge(first, second)

    def get_all_edges(self):
        return list(self.graph.edges)

    def remove_node(self, node):
        self.graph.remove_node(node)

    def remove_edge(self, first, second):
        self.graph.remove_edge(first, second)
