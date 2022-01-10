

class Node:
    __node_id: int

    longitude: float
    latitude: float

    def __init__(self, node_id: int, longitude: float, latitude: float):
        self.__node_id = node_id
        self.__latitude = latitude
        self.__longitude = longitude
