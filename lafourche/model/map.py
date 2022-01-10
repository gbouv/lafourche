from .edge import Edge
from .node import Node


class Map:
    __edges: [Edge]

    def __init__(self, edges: [Edge]):
        self.__edges = edges

    def __iter__(self):
        return iter(self.__edges)

    def __len__(self):
        return self.__edges.__len__()

    def get_bottom_left(self) -> Node:
        """Return the bottom right node of the map"""
        # TODO(mv): implement
        pass

    def get_top_right(self) -> Node:
        """Return the top left node of the map"""
        # TODO(mv): implement
        pass

    def get_center(self) -> Node:
        """Return a fictive node corresponding to center of the map"""
        # TODO(mv): implement
        pass
