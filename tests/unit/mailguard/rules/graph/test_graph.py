import pytest

from mailguard.rules.graph import graph
from mailguard.rules.graph.node import Node
from mailguard.rules.models.rule_container import RuleType, Data
from mailguard.rules.errors.graph import NodeTypeException, EdgeException


def test_rule_graph_nodes_first():
    node_one = Node(Data(RuleType.TAG, data=[1]))
    node_two = Node(Data(RuleType.CONDITIONAL))

    rgraph = graph.RuleGraph()
    rgraph.add_node(node_one)
    rgraph.add_node(node_two)

    _add_edge_and_assert(rgraph, node_one, node_two)


def test_rule_graph_edges_only():
    node_one = Node(Data(RuleType.TAG, data=[1]))
    node_two = Node(Data(RuleType.CONDITIONAL))

    rgraph = graph.RuleGraph()
    
    _add_edge_and_assert(rgraph, node_one, node_two)


def test_rule_graph_node_type_error():
    rgraph = graph.RuleGraph()

    with pytest.raises(NodeTypeException):
        rgraph.add_node('wrong')


def test_rule_graph_edge_type_error():
    rgraph = graph.RuleGraph()

    with pytest.raises(NodeTypeException):
        rgraph.add_edge(Node(Data(RuleType.CONDITIONAL)), 'wrong')


def test_rule_graph_non_conditional_edge_error():
    rgraph = graph.RuleGraph()

    with pytest.raises(EdgeException) as ex:
        rgraph.add_edge(Node(Data(RuleType.TAG)), Node(Data(RuleType.TAG)))

        assert 'Non conditional node can only be connected to conditional node' in str(ex.value)


def _add_edge_and_assert(rgraph, node_one, node_two):
    rgraph.add_edge(node_one, node_two)

    popped_node = rgraph.graph[node_two].pop()

    assert len(rgraph.graph) == 2
    assert rgraph.graph[node_one].pop().value.rule_type is RuleType.CONDITIONAL
    assert popped_node.value.rule_type is RuleType.TAG
    assert popped_node.value.data[0] == 1
