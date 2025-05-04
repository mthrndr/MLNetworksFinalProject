from typing import Self

ALPHA = 0.5


class Node:
    """
    Nodes can receive and send packets to other nodes.
    Each node has a dictionary of its neighbors, where the keys are the
    neighbor class object, and the values are the "cost" to send a packet to
    that node.
    """
    def __init__(self, index: int) -> None:
        self.index = index
        self.neighbors = {}

    def get_index(self) -> int:
        return self.index

    def add_neighbor(self, neighbor: Self, cost: float) -> None:
        self.neighbors[neighbor] = cost

    def delete_neighbor(self, neighbor: Self) -> bool:
        if self.neighbors.get(neighbor):
            del self.neighbors[neighbor]
            return True
        else:
            raise ValueError(f"Node {self.index} does not have "
                             "{neighbor.index} as a neighbor")
