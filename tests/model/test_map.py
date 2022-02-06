import logging
import unittest

from lafourche.model import Node, Edge, Map
from lafourche.model.geopoint import Geopoint


class TestMap(unittest.TestCase):
    logging.basicConfig(level=logging.DEBUG)
    node1 = Node(1, Geopoint(-1, 3))
    node2 = Node(2, Geopoint(3, 5))
    node3 = Node(3, Geopoint(100, -25))
    edge1 = Edge(node1, node2, 10)
    edge2 = Edge(node1, node3, 5)
    test_map = Map([edge1, edge2])

    def test_top_right(self):
        self.assertEqual(self.test_map.get_top_right(), Geopoint(100, 5), "Expected Node(None, 100, 5")

    def test_bottom_left(self):
        self.assertEqual(self.test_map.get_bottom_left(), Geopoint(-1, -25), "Expected Node(None, -1, -25")

    def test_center(self):
        self.assertEqual(self.test_map.get_center(), Geopoint(49.5, -10), "Expected Node(None, 49.5, -10)")
