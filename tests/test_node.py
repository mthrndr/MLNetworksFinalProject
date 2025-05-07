from pytest import fixture

from node import Node

RAND_COST = 0.5


@fixture
def new_node():
    yield Node.create_node
    Node.clear_nodes()


def test_create_node(new_node):
    assert new_node()


def test_get_nodes(new_node):
    node_dict = Node.get_nodes()
    assert len(node_dict) == 0
    new_node()
    assert len(node_dict) == 1
    Node.clear_nodes()
    assert len(node_dict) == 0


def test_get_index(new_node):
    assert new_node().get_index() == 0


def test_add_neighbor(new_node):
    node_1 = new_node()
    node_2 = new_node()
    node_1.add_neighbor(node_2, RAND_COST)
    ret = node_1.get_neighbors()
    assert ret
    assert node_2 in ret


def test_delete_neighbor(new_node):
    node_1 = new_node()
    node_2 = new_node()
    node_1.add_neighbor(node_2, RAND_COST)
    ret = node_1.get_neighbors()
    assert node_2 in ret
    node_1.delete_neighbor(node_2)
    ret = node_1.get_neighbors()
    assert node_2 not in ret


SAMPLE_TABLE = [
    [0, 1, 0, 0],
    [1, 0, 1, 1],
    [0, 1, 0, 0],
    [0, 1, 0, 0],
]


def test_create_nodes_from_table():
    Node.create_nodes_from_table(SAMPLE_TABLE)
    nodes = Node.get_nodes()
    assert len(nodes) == len(SAMPLE_TABLE)
    assert nodes[0].is_neighbors_with(nodes[1])
    assert nodes[1].is_neighbors_with(nodes[0])
    assert nodes[1].is_neighbors_with(nodes[2])
    assert nodes[1].is_neighbors_with(nodes[3])
    assert nodes[2].is_neighbors_with(nodes[1])
    assert nodes[3].is_neighbors_with(nodes[1])
