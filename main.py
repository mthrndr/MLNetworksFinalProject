from random import random
from pprint import pprint

NUM_NODES = 10

def custom_table_print(table: list) -> bool:
    for row in table:
        for element in row:
            print(element, end=" ")
        print()

def get_cost():
    """
    Provides a random cost for a node to reach another node
    """
    return random()


def gen_empty_table(size: int) -> list:
    node_table = [0] * size
    for i in range(size):
        node_table[i] = [0] * NUM_NODES
    return node_table


def fill_table_with_init_costs(node_list: list, size: int):
    for i in range(NUM_NODES):
        for j in range(NUM_NODES):
            if i == j:
                node_list[i][j] = 0
            else:
                node_list[i][j] = get_cost()


def gen_node_table():
    """
    Creates a table NUM_NODES in height and width, with randomly assigned
    costs.
    """
    node_table = gen_empty_table(NUM_NODES)
    fill_table_with_init_costs(node_table, NUM_NODES)
    return node_table



def main():
    tmp = gen_node_table()
    custom_table_print(tmp)

if __name__ == '__main__':
    main()
