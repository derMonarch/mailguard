from mailguard.rules.errors.graph import NodeTypeException
from mailguard.rules.graph.node import Node


def graph_validation(graph_class):
    add_node = graph_class.add_node
    add_edge = graph_class.add_edge

    def _add_node(self, *args):
        _check_node_instance(args[0])
        return add_node(self, *args)

    def _add_edge(self, *args):
        _check_node_instance(*args)

        return add_edge(self, *args)

    graph_class.add_node = _add_node
    graph_class.add_edge = _add_edge

    return graph_class


def _check_node_instance(*args):
    if len(args) == 1:
        if not isinstance(args[0], Node):
            raise NodeTypeException(f'passed node needs to be of type Node, got {type(args[0])}')
    elif len(args) == 2:
        if not isinstance(args[0], Node) or not isinstance(args[1], Node):
            raise NodeTypeException(f'passed nodes needs to be of type Node, got {type(args[0])} and {type(args[1])}')
