import logging
import unittest

from lafourche.model import Node, Edge, Map


class TestMap(unittest.TestCase):
    logging.basicConfig(level=logging.DEBUG)

    def test_top_right(self):
        node1 = Node(1, -1, 3)
        node2 = Node(2, 3, 5)
        node3 = Node(3, 100, -25)

        edge1 = Edge(node1, node2, 10)
        edge2 = Edge(node1, node3, 5)

        map = Map([edge1, edge2])

        self.assertEqual(map.get_top_right(), Node(None, 100, 5), "Expected Node(None, 100, 5")

    def test_bottom_left(self):
        node1 = Node(1, -1, 3)
        node2 = Node(2, 3, 5)
        node3 = Node(3, 100, -25)

        edge1 = Edge(node1, node2, 10)
        edge2 = Edge(node1, node3, 5)

        map = Map([edge1, edge2])

        self.assertEqual(map.get_bottom_left(), Node(None, -1, -25), "Expected Node(None, -1, -25")

    def test_center(self):
        node1 = Node(1, -1, 3)
        node2 = Node(2, 3, 5)
        node3 = Node(3, 100, -25)

        edge1 = Edge(node1, node2, 10)
        edge2 = Edge(node1, node3, 5)

        map = Map([edge1, edge2])

        self.assertEqual(map.get_center(), Node(None, 49.5, -10), "Expected Node(None, 49.5, -10)")
