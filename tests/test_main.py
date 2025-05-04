import main as mn
from main import NUM_NODES


def test_custom_table_print():
    """
    Just making sure nothing breaks
    """
    assert mn.custom_table_print([[0, 0], [1, 1]])


def test_get_init_cost():
    assert isinstance(mn.get_init_cost(), float)


def test_gen_empty_table():
    TEST_SIZE = 5
    table = mn.gen_empty_table(TEST_SIZE)
    assert len(table) == TEST_SIZE
    assert len(table[0]) == TEST_SIZE
    for i in range(TEST_SIZE):
        for j in range(TEST_SIZE):
            assert table[i][j] == 0


def test_fill_table_with_init_costs():
    table = mn.fill_table_with_init_costs(mn.gen_empty_table())
    assert len(table) == NUM_NODES
    assert len(table[0]) == NUM_NODES
    assert table[1][1] == 0


def test_get_random_node():
    assert 0 <= mn.get_random_node() < NUM_NODES


def test_gen_init_node_cost_table():
    table = mn.get_init_node_cost_table()
    assert len(table) == NUM_NODES
    assert len(table[0]) == NUM_NODES
    assert table[1][1] == 0
