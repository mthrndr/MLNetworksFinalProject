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
    def __init__(self, index: int) -> None:
        self.index = index
        self.neighbors = {}

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
        return self.index == other.index

    def __hash__(self) -> int:
        return hash(self.index)
