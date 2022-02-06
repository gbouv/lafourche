from .edge import Edge
from .geopoint import Geopoint


class Map:
    __edges: [Edge]

    def __init__(self, edges: [Edge]):
        self.__edges = edges

    def __iter__(self):
        return iter(self.__edges)

    def __len__(self):
        return self.__edges.__len__()

    def get_bottom_left(self) -> Geopoint:
        """Return the bottom right node of the map"""
        lat = 90
        lon = 180
        for edge in self.__edges:
            for node in [edge.node1, edge.node2]:
                lat = min(lat, node.coord.lat)
                lon = min(lon, node.coord.lon)
        return Geopoint(lon, lat)

    def get_top_right(self) -> Geopoint:
        """Return the top left node of the map"""
        lat = -90
        lon = -180
        for edge in self.__edges:
            for node in [edge.node1, edge.node2]:
                lat = max(lat, node.coord.lat)
                lon = max(lon, node.coord.lon)
        return Geopoint(lon, lat)

    def get_center(self) -> Geopoint:
        """Return a fictive node corresponding to center of the map"""
        bottom_left = self.get_bottom_left()
        top_right = self.get_top_right()
        min_lat = bottom_left.lat
        max_lat = top_right.lat
        min_lon = bottom_left.lon
        max_lon = top_right.lon
        return Geopoint((max_lon + min_lon) / 2, (max_lat + min_lat) / 2)
