from typing import Self

ALPHA = 0.5
QUEUE_TIME = 0


class Node:
    """
    Nodes can receive and send packets to other nodes.
    Each node has a dictionary of its neighbors, where the keys are the
    neighbor class object, and the values are the "cost" to send a packet to
    that node.
    """
    NODE_DICT = {}
    CURR_MAX_INDEX = 0

    @staticmethod
    def get_nodes() -> dict[int, Self]:
        """
        The node dict consists of the indexes of the nodes as keys, and the
        associated nodes as values.
        """
        return Node.NODE_DICT

    @staticmethod
    def get_node(index: int) -> Self:
        return Node.NODE_DICT[index]

    def __init__(self, index: int) -> Self:
        """
        Note: You should ONLY instantiate a node using the create_node factory
        method.
        """
        self.index = index
        self.neighbors = {}

    @classmethod
    def create_node(cls) -> Self:
        """
        Creates a new node, adds it to the NODE_DICT class variable, with the
        CURR_MAX_INDEX as it's index value and key in the NODE_DICT, then
        increments the CURR_MAX_INDEX.
        """
        new_node = cls(Node.CURR_MAX_INDEX)
        Node.NODE_DICT[Node.CURR_MAX_INDEX] = new_node
        Node.CURR_MAX_INDEX += 1
        return new_node

    @classmethod
    def clear_nodes(cls) -> None:
        """
        Clears out the NODE_DICT as well as reseting CURR_MAX_INDEX to 0.
        """
        Node.NODE_DICT.clear()
        Node.CURR_MAX_INDEX = 0

    @classmethod
    def create_nodes_from_table(cls, table: list[list[float]]) -> dict:
        """
        Takes in a table of nodes, and the cost to go to their neighbors.
        Clears out any current nodes, and then creates nodes based on the
        values in the table.
        """
        Node.clear_nodes()
        for node in table:
            Node.create_node()

        for node_index, node_costs in enumerate(table):
            curr_node = Node.get_node(node_index)
            for other_index, other_cost in enumerate(node_costs):
                if other_cost > 0:
                    curr_node.add_neighbor(Node.get_node(other_index),
                                           other_cost)
        return Node.NODE_DICT

    def get_index(self) -> int:
        return self.index

    def get_neighbors(self) -> dict:
        return self.neighbors

    def is_neighbors_with(self, neighbor: Self) -> bool:
        return neighbor in self.neighbors

    def add_neighbor(self, neighbor: Self, cost: float) -> None:
        """
        Adds a neighbor to the current node, with it's cost as a value. Then
        tries to add itself as a neighbor to the other node.
        """
        if not self.is_neighbors_with(neighbor):
            self.neighbors[neighbor] = cost
        if not neighbor.is_neighbors_with(self):
            neighbor.add_neighbor(self, cost)

    def delete_neighbor(self, neighbor: Self) -> None:
        """
        Deletes a neighbor from the current node. Then tries to delete itself
        as a neighbor from the other node.
        """
        if self.is_neighbors_with(neighbor):
            del self.neighbors[neighbor]
            if neighbor.is_neighbors_with(self):
                neighbor.delete_neighbor(self)
        else:
            raise ValueError(f"Node {self.index} does not have "
                             f"{neighbor.index} as a neighbor")

    def __eq__(self, other: Self) -> bool:
        """
        Nodes should have unique indexes.
        """
        return self.index == other.index

    def __hash__(self) -> int:
        """
        Nodes should have unique indexes.
        """
        return hash(self.index)
