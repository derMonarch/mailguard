from mailguard.rules.graph import graph
from mailguard.rules.models.rule_container import RuleType, Data


def test_rule_graph_nodes_first():
    node_one = graph.Node(Data(RuleType.TAG, data=[1]))
    node_two = graph.Node(Data(RuleType.CONDITIONAL))

    rgraph = graph.RuleGraph()
    rgraph.add_node(node_one)
    rgraph.add_node(node_two)

    _add_edge_and_assert(rgraph, node_one, node_two)


def test_rule_graph_edges_only():
    node_one = graph.Node(Data(RuleType.TAG, data=[1]))
    node_two = graph.Node(Data(RuleType.CONDITIONAL))

    rgraph = graph.RuleGraph()
    
    _add_edge_and_assert(rgraph, node_one, node_two)


def _add_edge_and_assert(rgraph, node_one, node_two):
    rgraph.add_edge(node_one, node_two)

    popped_node = rgraph.graph[node_two].pop()

    assert len(rgraph.graph) == 2
    assert rgraph.graph[node_one].pop().value.rule_type is RuleType.CONDITIONAL
    assert popped_node.value.rule_type is RuleType.TAG
    assert popped_node.value.data[0] == 1
