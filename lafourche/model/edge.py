from .node import Node


class Edge:
    node1: Node
    node2: Node
    weight: int

    def __init__(self, node1: Node, node2: Node, weight: int):
        self.node1 = node1
        self.node2 = node2
        self.weight = weight
