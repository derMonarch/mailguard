from mailguard.rules.errors.graph import NodeTypeException, EdgeException
from mailguard.rules.graph.node import Node
from mailguard.rules.models.rule_container import RuleType


def graph_validation(graph_class):
    """
        TODO: check for functions not yet validated
    """
    add_node = graph_class.add_node
    add_edge = graph_class.add_edge
    get_all_edges = graph_class.get_all_edges

    def _add_node(self, *args):
        _check_node_instance(args[0])
        return add_node(self, *args)

    def _add_edge(self, *args):
        _check_node_instance(*args)
        _check_node_edges(*args)

        return add_edge(self, *args)

    def _get_all_edges(self, *args):

        return get_all_edges(self, *args)

    def _check_not_yet_validated_functions():
        pass

    graph_class.add_node = _add_node
    graph_class.add_edge = _add_edge
    graph_class.get_all_edges = _get_all_edges

    return graph_class


def _check_node_instance(*args):
    if len(args) == 1:
        if not isinstance(args[0], Node):
            raise NodeTypeException(f'passed node needs to be of type Node, got {type(args[0])}')
    elif len(args) == 2:
        if not isinstance(args[0], Node) or not isinstance(args[1], Node):
            raise NodeTypeException(f'passed nodes needs to be of type Node, got {type(args[0])} and {type(args[1])}')


def _check_node_edges(*args):
    first = args[0]
    second = args[1]
    if first.value.rule_type is not RuleType.CONDITIONAL:
        _check_non_conditional(second)


def _check_non_conditional(second):
    if second.value.rule_type is not RuleType.CONDITIONAL:
        raise EdgeException('Non conditional node can only be connected to conditional node')

