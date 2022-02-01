from .node import Node


class Edge:
    node1: Node
    node2: Node
    weight: int

    def __init__(self, node1: Node, node2: Node, weight: int):
        self.node1 = node1
        self.node2 = node2
        self.weight = weight

    def __str__(self) -> str:
        return "Edge(" + str(self.node1) + ", " + str(self.node2) + ", " + str(self.weight) + ")"