

class Node:
    __node_id: int

    longitude: float
    latitude: float

    def __init__(self, node_id: int, longitude: float, latitude: float):
        self.__node_id = node_id
        self.latitude = latitude
        self.longitude = longitude

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Node):
            return False
        return o.latitude == self.latitude and o.longitude == self.longitude and o.__node_id == self.__node_id

    def __str__(self) -> str:
        return "Node(" + str(self.__node_id) + ", " + str(self.longitude) + ", " + str(self.latitude) + ")"

    def __repr__(self) -> str:
        return self.__str__()


