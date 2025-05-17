from random import random

NUM_NODES = 10


SAMPLE_TABLE = [
    [0, 1, 0, 0],
    [1, 0, 1, 1],
    [0, 1, 0, 0],
    [0, 1, 0, 0],
]

MAX_COST = 1.00
NOT_ACCESSIBLE_COST = MAX_COST + 1.00
# How much it costs a node to access itself
SELF_COST = 0.00


def custom_table_print(table: list) -> bool:
    for row in table:
        for element in row:
            print(element, end=" ")
        print()
    return True


def get_init_cost() -> float:
    """
    Provides a random cost between 0 and 1 for a node to reach another node
    """
    return random()


def gen_empty_table(size: int = NUM_NODES) -> list:
    """
    Generates a size*size table of 0s.
    """
    node_table = [0] * size
    for i in range(size):
        node_table[i] = [0] * size
    return node_table


def fill_table_with_init_costs(
    node_cost_table: list,
    size: int = NUM_NODES,
) -> list:
    """
    Receives a table and fills it with cost values.
    For a node i, it's cost for itself, ie [i][i] will be 0, meaning it is
    unaccessible.
    """
    for i in range(NUM_NODES):
        for j in range(NUM_NODES):
            if i == j:
                node_cost_table[i][j] = SELF_COST
            else:
                node_cost_table[i][j] = get_init_cost()
    return node_cost_table


def get_init_node_cost_table() -> list:
    """
    Creates a table NUM_NODES in height and width, with randomly assigned
    costs. Uses default values for size in function calls.
    """
    node_cost_table = gen_empty_table()
    fill_table_with_init_costs(node_cost_table)
    return node_cost_table
