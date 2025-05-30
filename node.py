from random import randrange
from typing import (
    Any,
    NoReturn,
    Self,
)

import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx


from costs import (
    NOT_ACCESSIBLE_COST,
    SELF_COST,
)

mpl.use('QtAgg')

ALPHA = 0.5
QUEUE_TIME = 0.0
# Something really low so it gets picked.
INIT_COST = 0.0

# For use in the estimated cost tuple
ESTIMATED_NODE = 0
ESTIMATED_COST = 1


class Node:
    """
    Nodes can receive and send packets to other nodes.
    Each node has a dictionary of its neighbors, where the keys are the
    neighbor class object, and the values are the "cost" to send a packet to
    that node.
    """
    NODE_DICT = {}
    CURR_MAX_INDEX = 0
    COST_TABLE = []

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

    @staticmethod
    def print_nodes() -> NoReturn:
        COLS = 5
        ROWS = (Node.CURR_MAX_INDEX + 1)//COLS
        for dest_index in Node.NODE_DICT:
            G = nx.MultiDiGraph()
            dest = Node.get_node(dest_index)
            for index_i in Node.NODE_DICT:
                G.add_node(index_i)
            for index_i in Node.NODE_DICT:
                if index_i is not dest_index:
                    node_i = Node.get_node(index_i)
                    for node_j in node_i.get_neighbors():
                        index_j = node_j.get_index()
                        cost = node_i.get_cost_from_neighbor_to_dest(node_j,
                                                                     dest)
                        cost_2 = node_j.get_cost_from_neighbor_to_dest(node_i,
                                                                       dest)
                        if cost > cost_2:
                            G.add_edge(index_i, index_j, weight=cost)
                        else:
                            G.add_edge(index_j, index_i, weight=cost_2)
            plt.subplot(ROWS, COLS, dest_index + 1, title=dest_index)
            pos = nx.spring_layout(G, seed=7)
            nx.draw_networkx_nodes(G, pos)
            nx.draw_networkx_edges(
                G,
                pos,
                arrowstyle="->",
                arrowsize=10,
                width=2,
            )
            edge_labels = nx.get_edge_attributes(G, "weight")
            nx.draw_networkx_edge_labels(G, pos, edge_labels)
            nx.draw_networkx_labels(G, pos, font_size=20,
                                    font_family="sans-serif")
            ax = plt.gca()
            ax.set_axis_off()

        plt.tight_layout()
        plt.show(block=True)

    # Error methods:

    @staticmethod
    def raise_not_neighbors(main: Self, other: Self) -> NoReturn:
        """
        Note: Makes no assumption about the two nodes relation, just raises the
        error message with their indexes.
        """
        raise ValueError(f"Node {main.index} does not have "
                         f"{other.index} as a neighbor.")

    @staticmethod
    def raise_not_a_node(val: Any) -> NoReturn:
        """
        Note: Makes no assumption about the value passed in, just raises the
        error message.
        """
        raise ValueError(f"{val} is not a Node.")

    @staticmethod
    def is_node(val: Any) -> bool:
        return isinstance(val, Node)

    @staticmethod
    def is_node_check(val: Any) -> NoReturn:
        if not Node.is_node(val):
            Node.raise_not_a_node(val)

    def __init__(self, index: int) -> Self:
        """
        Note: You should ONLY instantiate a node using the create_node factory
        method.
        """
        self.index = index
        self.neighbors = {}

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

    def __str__(self) -> str:
        return f'Node {self.index}'

    def __repr__(self) -> str:
        return self.__str__()

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
    def clear_nodes(cls) -> NoReturn:
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
        Node.COST_TABLE = table
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

    def get_random_node_index() -> int:
        """
        Returns a value between 0 and n, where n is the index of the final
        node.
        """
        return randrange(Node.CURR_MAX_INDEX)

    def get_index(self) -> int:
        """
        Returns the node's index.
        """
        return self.index

    def get_queue_time(self) -> float:
        """
        Returns the node's queue time.
        Currently just returns a constant.
        """
        return QUEUE_TIME

    def get_neighbors(self) -> dict:
        """
        Returns the node's neighbors.
        """
        return self.neighbors

    def is_neighbors_with(self, neighbor: Self) -> bool:
        """
        Returns True if the provided neighbor is in the node's neighbors dict.
        """
        return neighbor in self.neighbors

    def is_neighbors_check(self, neighbor: Self) -> NoReturn:
        """
        Checks if the current node is neighbors with a node, if not raises
        a ValueError.
        """
        if not self.is_neighbors_with(neighbor):
            Node.raise_not_neighbors(self, neighbor)

    def add_neighbor(self, neighbor: Self, cost: float) -> NoReturn:
        """
        Adds a neighbor to the current node, with it's cost as a value. Then
        tries to add itself as a neighbor to the other node with the same cost.
        This cost is different then others as it is immutable, and is
        considered the transmission cost.
        """
        if not self.is_neighbors_with(neighbor):
            self.neighbors[neighbor] = {neighbor: cost}
        if not neighbor.is_neighbors_with(self):
            neighbor.add_neighbor(self, cost)

    def delete_neighbor(self, neighbor: Self) -> NoReturn:
        """
        Deletes a neighbor from the current node. Then tries to delete itself
        as a neighbor from the other node.
        """
        self.is_neighbors_check(neighbor)
        del self.neighbors[neighbor]
        if neighbor.is_neighbors_with(self):
            neighbor.delete_neighbor(self)

    def get_cost_from_neighbor_to_dest(self,
                                       neighbor: Self,
                                       dest: Self,
                                       ) -> float:
        """
        Returns the cost that the node believes it will take to go to a
        destination from one of it's neighbors.
        """
        self.is_neighbors_check(neighbor)
        Node.is_node_check(dest)

        cost = self.neighbors[neighbor].get(dest, None)

        if cost is None:
            self.neighbors[neighbor][dest] = INIT_COST
            return INIT_COST

        return cost

    def get_estimated_cost_to(self,
                              dest: Self,
                              callers: list[Self],
                              ) -> tuple[Self, float]:
        """
        Recursive function to get the estimated cheapest cost to get to a
        destination, and the node it would use to do so.
        Format of the return tuple is (node, cost).
        This method exclusively uses knowledge that the node already has, and
        thus SHOULD NOT call any other node's methods.
        """
        Node.is_node_check(dest)

        if self is dest:
            return (Self, SELF_COST)

        estimated_costs = {}
        for neighbor in self.neighbors:
            # We do not want to include the caller in order to prevent a
            # situation where two nodes both think they have the shortest
            # distance to the destination
            if neighbor not in callers:
                neighbors_cost = self.get_cost_from_neighbor_to_dest(neighbor,
                                                                     dest)
                estimated_costs[neighbor] = neighbors_cost

        # No neighbors: dest is not accessible, return NOT ACCESSIBLE which is
        # a very high cost
        if not estimated_costs:
            return (None, NOT_ACCESSIBLE_COST)

        min_neighbor, min_cost = min(estimated_costs.items(),
                                     key=lambda item: item[1])

        return (min_neighbor, min_cost)

    def get_transmission_cost(self, neighbor: Self) -> float:
        """
        Just calls the get_transmission_cost function from the costs module and
        passes the two nodes' indexes. The destination must be a neighbor.
        """
        return self.get_cost_from_neighbor_to_dest(neighbor, neighbor)

    def update_cost_to(self,
                       neighbor: Self,
                       dest: Self,
                       current_cost: float,
                       transmission_cost: float,
                       neighbors_estimated_cost: float,
                       ) -> float:
        """
        Implements the Q-Routing delay update function, then updates the node's
        cost table from it's neighbor to the destination.
        """
        queue_time = self.get_queue_time()
        new_cost = queue_time + transmission_cost + neighbors_estimated_cost
        updated_cost = ((1 - ALPHA) * current_cost) + (ALPHA * new_cost)
        self.neighbors[neighbor][dest] = updated_cost
        return updated_cost

    def route(self,
              dest: Self,
              callers: list[Self] = [],
              training: bool = True
              ) -> float:
        """
        Actually runs the Q-Routing protocol.
        If no caller is provided, it is assumed this is the first call.
        1. Finds out which neighbor it believes has the cheapest route to the
        destination
        2. Send the route to the neighbor, which returns it's initial estimated
        cost to reach the destination
        3. Update estimated cost based on neighbor's cost and transmission
        cost.
        4. Return your initial estimated cost to complete recursion. If the
        node who receives the route is the destination, they just return 0.
        """
        if self is dest:
            return SELF_COST
        (min_neighbor, min_cost) = self.get_estimated_cost_to(dest, callers)

        if not min_neighbor:
            return min_cost
        # We want this to be a shallow copy so that we are always referring to
        # the same nodes!

        new_callers = callers.copy()
        new_callers.append(self)
        neighbors_estimated_cost = min_neighbor.route(dest, new_callers)
        if training:
            transmission_cost = self.get_transmission_cost(min_neighbor)
            self.update_cost_to(min_neighbor,
                                dest,
                                min_cost,
                                transmission_cost,
                                neighbors_estimated_cost)
        # Note: An empty list has a boolean value of False
        if callers:
            return min_cost
        else:
            # First sender, return final cost
            return self.get_cost_from_neighbor_to_dest(min_neighbor, dest)
