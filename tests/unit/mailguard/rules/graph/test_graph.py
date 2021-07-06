from mailguard.rules.graph import graph
from mailguard.rules.graph.node import Node
from mailguard.rules.models.rule_container import RuleType, Data, SubRuleType
from mailguard.helper import serialization


def test_rule_graph_nodes_first():
    node_one = Node(Data(RuleType.FILTER, SubRuleType.CATEGORIES, data=[1]))
    node_two = Node(Data(RuleType.CONDITIONAL))

    rgraph = graph.RuleGraph(rule_id='12345')
    rgraph.add_node(node_one)
    rgraph.add_node(node_two)

    _add_edge_and_assert(rgraph, node_one, node_two)


def test_rule_graph_edges_only():
    node_one = Node(Data(RuleType.FILTER, SubRuleType.CATEGORIES, data=[1]))
    node_two = Node(Data(RuleType.CONDITIONAL))

    rgraph = graph.RuleGraph(rule_id='12345')
    
    _add_edge_and_assert(rgraph, node_one, node_two)


def test_rule_graph_serialization():
    node_one = Node(Data(RuleType.FILTER, SubRuleType.CATEGORIES, data=['gambling']))
    node_and = Node(Data(RuleType.CONDITIONAL, bool_and=True))
    node_two = Node(Data(RuleType.FILTER, SubRuleType.FROM_ADDRESS, data=['a@b']))
    node_or = Node(Data(RuleType.CONDITIONAL, bool_or=True))
    node_and_two = Node(Data(RuleType.CONDITIONAL, bool_and=True))
    node_three = Node(Data(RuleType.FILTER, SubRuleType.CATEGORIES, data=['insurance']))
    node_four = Node(Data(RuleType.FILTER, SubRuleType.FROM_ADDRESS, data=['yes@no']))

    rgraph = graph.RuleGraph(rule_id='12345')

    rgraph.add_edge(node_one, node_and)
    rgraph.add_edge(node_and, node_two)
    rgraph.add_edge(node_and, node_or)
    rgraph.add_edge(node_or, node_and_two)
    rgraph.add_edge(node_and_two, node_three)
    rgraph.add_edge(node_and_two, node_four)

    serialized = serialization.serialize_object(rgraph)
    print('YEES')


def _add_edge_and_assert(rgraph, node_one, node_two):
    rgraph.add_edge(node_one, node_two)

    popped_node = rgraph.graph[node_two].pop()

    assert len(rgraph.graph) == 2
    assert rgraph.graph[node_one].pop().value.rule_type is RuleType.CONDITIONAL
    assert popped_node.value.rule_type is RuleType.TAG
    assert popped_node.value.data[0] == 1
