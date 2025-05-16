import costs as costs
from node import Node


def initialize_sim():
    table = costs.get_init_node_cost_table()
    Node.create_nodes_from_table(table)
    for i in range(100):
        node_start = Node.get_node(Node.get_random_node_index())
        node_dest = Node.get_node(Node.get_random_node_index())
        time = node_start.route(node_dest, training=True)
        print(time)


def main():
    initialize_sim()


if __name__ == '__main__':
    main()
