from lafourche.model.geopoint import Geopoint


class Node:
    __node_id: int
    coord: Geopoint

    def __init__(self, node_id: int, coord: Geopoint):
        self.__node_id = node_id
        self.coord = coord

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Node):
            return False
        return o.coord == self.coord and o.__node_id == self.__node_id

    def __str__(self) -> str:
        return "Node(id: " + str(self.__node_id) + ", coord: " + str(self.coord) + ")"

    def __repr__(self) -> str:
        return self.__str__()
