import json

from mailguard.rules.graph import graph
from mailguard.rules.models.rule_container import RuleType, SubRuleType, Data
from networkx.readwrite import json_graph


def test_graph_representation():
    """TODO: may use only dict for graph representation"""
    rules = graph.RuleGraph('1234')

    node_one = Data(RuleType.FILTER, SubRuleType.FROM_ADDRESS, data=['a@b'])
    node_and = Data(RuleType.CONDITIONAL, bool_and=True)
    node_two = Data(RuleType.FILTER, SubRuleType.CATEGORIES, data=['gambling'])
    node_or = Data(RuleType.CONDITIONAL, bool_or=True)
    node_and_two = Data(RuleType.CONDITIONAL, bool_and=True)
    node_three = Data(RuleType.FILTER, SubRuleType.FROM_ADDRESS, data=['b@a'])
    node_four = Data(RuleType.FILTER, SubRuleType.BUZZWORDS, data=['win'])

    rules.add_edge(node_and, node_one)
    rules.add_edge(node_and, node_two)
    rules.add_edge(node_and, node_or)
    rules.add_edge(node_or, node_and_two)
    rules.add_edge(node_and_two, node_three)
    rules.add_edge(node_and_two, node_four)

    edges = rules.get_all_edges()

    assert len(edges) == 6
    assert edges[0][0].node_id is not None
    assert edges[0][0].bool_and is True
    assert edges[0][0].rule_type is RuleType.CONDITIONAL
    assert edges[0][1].node_id is not None
    assert edges[0][1].rule_type is RuleType.FILTER
    assert edges[0][1].sub_rule_type is SubRuleType.FROM_ADDRESS
    assert edges[1][0].node_id is not None
    assert edges[1][0].bool_and is True
    assert edges[1][0].rule_type is RuleType.CONDITIONAL
    assert edges[1][1].node_id is not None
    assert edges[1][1].rule_type is RuleType.FILTER
    assert edges[1][1].sub_rule_type is SubRuleType.CATEGORIES


def test_graph_serialization():
    rules = graph.RuleGraph('1234')

    node_one = Data(RuleType.FILTER, SubRuleType.FROM_ADDRESS, data=['a@b'])
    node_and = Data(RuleType.CONDITIONAL, bool_and=True)
    node_two = Data(RuleType.FILTER, SubRuleType.CATEGORIES, data=['gambling'])

    rules.add_edge(node_and, node_one)
    rules.add_edge(node_and, node_two)

    serialized = json_graph.node_link_data(rules.graph)
    serialized_graph = json.dumps(serialized, default=lambda o: o.__dict__)

    expected_graph = json.loads(serialized_graph)
    assert expected_graph['links'][0]['source']['rule_type'] == 2
    assert expected_graph['links'][0]['source']['bool_and'] is True
    assert expected_graph['links'][0]['target']['rule_type'] == 1
    assert expected_graph['links'][0]['target']['data'][0] in 'a@b'
