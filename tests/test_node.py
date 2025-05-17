from pytest import (
    fixture,
    raises,
)
from typing import Callable

from node import (
    ALPHA,
    ESTIMATED_COST,
    INIT_COST,
    Node,
)

from costs import (
    NOT_ACCESSIBLE_COST,
    SELF_COST,
)

RAND_COST = 0.5


@fixture
def new_node():
    yield Node.create_node
    Node.clear_nodes()


def create_neighbor_nodes(new_node: Callable,
                          cost: float = RAND_COST,
                          ) -> tuple[Node, Node]:
    node_1 = new_node()
    node_2 = new_node()
    node_1.add_neighbor(node_2, cost)
    return (node_1, node_2)


def test_create_node(new_node: Callable):
    assert new_node()


def test_get_nodes(new_node: Callable):
    node_dict = Node.get_nodes()
    assert len(node_dict) == 0
    new_node()
    assert len(node_dict) == 1
    Node.clear_nodes()
    assert len(node_dict) == 0


def test_get_index(new_node: Callable):
    assert new_node().get_index() == 0


def test_get_queue_time(new_node: Callable):
    assert isinstance(new_node().get_queue_time(), float)


def test_index_to_str(new_node: Callable):
    assert isinstance(str(new_node()), str)


def test_index_repr(new_node: Callable):
    assert isinstance(str([new_node()]), str)


def test_add_neighbor(new_node: Callable):
    node_1, node_2 = create_neighbor_nodes(new_node)
    ret = node_1.get_neighbors()
    assert ret
    assert node_2 in ret


def test_delete_neighbor(new_node: Callable):
    node_1, node_2 = create_neighbor_nodes(new_node)
    ret = node_1.get_neighbors()
    assert node_2 in ret
    node_1.delete_neighbor(node_2)
    ret = node_1.get_neighbors()
    assert node_2 not in ret


def test_delete_neighbor_not_neighbors(new_node: Callable):
    node_1 = new_node()
    node_2 = new_node()
    with raises(ValueError):
        node_1.delete_neighbor(node_2)


def test_raise_not_neighbors(new_node: Callable):
    node_1 = new_node()
    node_2 = new_node()
    with raises(ValueError):
        Node.raise_not_neighbors(node_1, node_2)


def test_raises_not_a_node():
    with raises(ValueError):
        Node.raise_not_a_node('something!')


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
    Node.clear_nodes()


def test_get_cost_from_neighbor_to_dest(new_node: Callable):
    """
    The reason the correct cost is INIT_COST and not whatever we set the value
    between node 2 and node 3 to be is that node_1 does not yet know the
    expected value from node_2 to node_3 so it must initialize it.
    """
    node_1, node_2 = create_neighbor_nodes(new_node)
    node_3 = new_node()
    node_2.add_neighbor(node_3, '0.8')
    assert node_1.get_cost_from_neighbor_to_dest(node_2, node_3) == INIT_COST


def test_get_cost_from_neighbor_to_dest_not_neighbors(new_node: Callable):
    """
    The reason the correct cost is INIT_COST and not whatever we set the value
    between node 2 and node 3 to be is that node_1 does not yet know the
    expected value from node_2 to node_3 so it must initialize it.
    """
    node_1 = new_node()
    node_2 = new_node()
    with raises(ValueError):
        assert node_1.get_cost_from_neighbor_to_dest(node_2, node_2)


def test_get_estimated_cost_to(new_node: Callable):
    node_1, node_2 = create_neighbor_nodes(new_node)
    ret = node_1.get_estimated_cost_to(node_2, [node_1])
    assert ret[ESTIMATED_COST] == RAND_COST


def test_get_estimated_cost_to_self(new_node: Callable):
    node_1 = new_node()
    ret = node_1.get_estimated_cost_to(node_1, [])
    assert ret[ESTIMATED_COST] == SELF_COST


def test_get_estimated_cost_to_not_neighbors(new_node: Callable):
    node_1 = new_node()
    node_2 = new_node()
    ret = node_1.get_estimated_cost_to(node_2, [node_1])
    assert ret[ESTIMATED_COST] == NOT_ACCESSIBLE_COST


def test_get_estimated_cost_to_not_a_node(new_node: Callable):
    node_1 = new_node()
    with raises(ValueError):
        node_1.get_estimated_cost_to('something', [node_1])


def test_get_random_node(new_node: Callable):
    TEST_SIZE = 10
    for i in range(TEST_SIZE):
        new_node()
    assert 0 <= Node.get_random_node_index() < TEST_SIZE


def test_get_transmission_cost(new_node: Callable):
    TEST_COST = 0.8
    node_1, node_2 = create_neighbor_nodes(new_node, TEST_COST)
    assert node_1.get_transmission_cost(node_2) == TEST_COST


def test_get_transmission_cost_not_a_node(new_node: Callable):
    node_1 = new_node()
    with raises(ValueError):
        node_1.get_transmission_cost('not a node')


def test_get_transmission_cost_not_neighbors(new_node: Callable):
    node_1 = new_node()
    node_2 = new_node()
    with raises(ValueError):
        node_1.get_transmission_cost(node_2)


def test_update_cost_to(new_node: Callable):
    TEST_COST = 0.8
    node_1, node_2 = create_neighbor_nodes(new_node, TEST_COST)
    node_3 = new_node()
    node_2.add_neighbor(node_3, TEST_COST)
    curr_cost = node_1.get_cost_from_neighbor_to_dest(node_2, node_3)
    assert curr_cost == INIT_COST
    transmission_cost = node_1.get_transmission_cost(node_2)
    assert transmission_cost == TEST_COST
    assert node_2.get_transmission_cost(node_3) == TEST_COST
    new_cost = node_1.update_cost_to(node_2,
                                     node_3,
                                     curr_cost,
                                     transmission_cost,
                                     TEST_COST)
    assert new_cost == TEST_COST
    curr_cost = node_1.get_cost_from_neighbor_to_dest(node_2, node_3)
    new_cost = node_1.update_cost_to(node_2,
                                     node_3,
                                     curr_cost,
                                     transmission_cost,
                                     TEST_COST)
    expected = (((1 - ALPHA) * TEST_COST) +
                (ALPHA * (TEST_COST + TEST_COST + node_1.get_queue_time())))
    assert new_cost == expected
