from .node import Node


class Edge:
    node1: Node
    node2: Node

    weight: int

    def __init__(self, node1: Node, node2: Node, weight: int):
        self.__node1 = node1
        self.__node2 = node2
        self.__weight = weight
