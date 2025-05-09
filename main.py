from random import (
    random,
    randrange,
)

NUM_NODES = 10


SAMPLE_TABLE = [
    [0, 1, 0, 0],
    [1, 0, 1, 1],
    [0, 1, 0, 0],
    [0, 1, 0, 0],
]


def custom_table_print(table: list) -> bool:
    for row in table:
        for element in row:
            print(element, end=" ")
        print()
    return True


def get_init_cost() -> float:
    """
    Provides a random cost for a node to reach another node
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
                node_cost_table[i][j] = 0
            else:
                node_cost_table[i][j] = get_init_cost()
    return node_cost_table


def get_random_node() -> int:
    """
    Returns a value between 0 and n, where n is the index of the final node
    """
    return randrange(NUM_NODES)


def get_init_node_cost_table() -> list:
    """
    Creates a table NUM_NODES in height and width, with randomly assigned
    costs. Uses default values for size in function calls.
    """
    node_cost_table = gen_empty_table()
    fill_table_with_init_costs(node_cost_table)
    return node_cost_table


def main():
    tmp = get_init_node_cost_table()
    custom_table_print(tmp)


if __name__ == '__main__':
    main()
