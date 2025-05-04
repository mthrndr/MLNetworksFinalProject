from typing import Self

ALPHA = 0.5
QUEUE_TIME = 0


NODE_DICT = {}
CURR_MAX_INDEX = 0


class Node:
    """
    Nodes can receive and send packets to other nodes.
    Each node has a dictionary of its neighbors, where the keys are the
    neighbor class object, and the values are the "cost" to send a packet to
    that node.
    """
    def __init__(self, index: int) -> Self:
        """
        Note: You should ONLY instantiate a node using the create_node factory
        method
        """
        self.index = index
        self.neighbors = {}

    @classmethod
    def create_node(cls) -> Self:
        global CURR_MAX_INDEX
        ret = cls(CURR_MAX_INDEX)
        NODE_DICT[ret] = None
        CURR_MAX_INDEX += 1
        return ret

    @classmethod
    def clear_nodes(cls) -> None:
        global CURR_MAX_INDEX
        NODE_DICT.clear()
        CURR_MAX_INDEX = 0

    def get_index(self) -> int:
        return self.index

    def get_neighbors(self) -> dict:
        return self.neighbors

    def add_neighbor(self, neighbor: Self, cost: float) -> None:
        self.neighbors[neighbor] = cost

    def delete_neighbor(self, neighbor: Self) -> bool:
        if self.neighbors.get(neighbor) is not None:
            del self.neighbors[neighbor]
            return True
        else:
            raise ValueError(f"Node {self.index} does not have "
                             f"{neighbor.index} as a neighbor")

    def __eq__(self, other: Self) -> bool:
        """
        Nodes should have unique indexes
        """
        return self.index == other.index

    def __hash__(self) -> int:
        """
        Nodes should have unique indexes
        """
        return hash(self.index)


def get_nodes():
    return NODE_DICT
