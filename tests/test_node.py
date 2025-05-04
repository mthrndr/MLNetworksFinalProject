import node as nd
from pytest import fixture

TMP_NODE_INDEX = 0


@fixture
def tmp_node():
    return nd.Node(TMP_NODE_INDEX)


def test_create_node(tmp_node):
    assert tmp_node


def test_get_index(tmp_node):
    assert tmp_node.get_index() == 0
