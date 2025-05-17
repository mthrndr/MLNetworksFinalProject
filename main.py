import costs as costs
from node import Node

TIMESTEPS = 100


def initialize_sim():
    # table = costs.get_init_node_cost_table()
    table = costs.SAMPLE_TABLE
    Node.create_nodes_from_table(table)
    Node.print_nodes()
    for i in range(TIMESTEPS):
        node_start = Node.get_node(Node.get_random_node_index())
        node_dest = Node.get_node(Node.get_random_node_index())
        node_start.route(node_dest, training=True)
    Node.print_nodes()
    for i in range(TIMESTEPS):
        node_start = Node.get_node(Node.get_random_node_index())
        node_dest = Node.get_node(Node.get_random_node_index())
        node_start.route(node_dest, training=True)
    Node.print_nodes()


def main():
    initialize_sim()


if __name__ == '__main__':
    main()
