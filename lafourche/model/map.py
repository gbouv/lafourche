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
        lat = 90
        lon = 180
        for edge in self.__edges:
            for node in [edge.node1, edge.node2]:
                lat = min(lat, node.latitude)
                lon = min(lon, node.longitude)
        return Node(None, lon, lat)

    def get_top_right(self) -> Node:
        """Return the top left node of the map"""
        lat = -90
        lon = -180
        for edge in self.__edges:
            for node in [edge.node1, edge.node2]:
                lat = max(lat, node.latitude)
                lon = max(lon, node.longitude)
        return Node(None, lon, lat)

    def get_center(self) -> Node:
        """Return a fictive node corresponding to center of the map"""
        bottom_left = self.get_bottom_left()
        top_right = self.get_top_right()
        min_lat = bottom_left.latitude
        max_lat = top_right.latitude
        min_lon = bottom_left.longitude
        max_lon = top_right.longitude
        return Node(None, (max_lon + min_lon) / 2, (max_lat + min_lat) / 2)
