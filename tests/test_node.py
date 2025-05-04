from pytest import fixture

import node as nd


CURR_NODE = 0


@fixture
def new_node():
    global CURR_NODE

    def create_node(index: int = None):
        global CURR_NODE
        if index:
            new_index = index
        else:
            new_index = CURR_NODE
            CURR_NODE += 1
        return nd.Node(new_index)

    yield create_node
    CURR_NODE = 0


def test_create_node(new_node):
    assert new_node()


def test_get_index(new_node):
    assert new_node().get_index() == 0


def test_add_neighbor(new_node):
    node_1 = new_node()
    node_2 = new_node()
    node_1.add_neighbor(node_2, 0)
    ret = node_1.get_neighbors()
    assert ret
    assert node_2 in ret


def test_delete_neighbor(new_node):
    node_1 = new_node()
    node_2 = new_node()
    node_1.add_neighbor(node_2, 0)
    ret = node_1.get_neighbors()
    assert node_2 in ret
    node_1.delete_neighbor(node_2)
    ret = node_1.get_neighbors()
    assert node_2 not in ret
