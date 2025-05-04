from pytest import fixture

import node as nd

RAND_COST = 0.5


@fixture
def new_node():
    yield nd.Node.create_node
    nd.Node.clear_nodes()


def test_create_node(new_node):
    assert new_node()


def test_get_nodes(new_node):
    node_dict = nd.get_nodes()
    assert len(node_dict) == 0
    new_node()
    assert len(node_dict) == 1
    nd.Node.clear_nodes()
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
