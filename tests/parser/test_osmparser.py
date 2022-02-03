import logging
import os.path
import unittest

from lafourche.parser import OsmParser


class TestOsmParser(unittest.TestCase):
    logging.basicConfig(level=logging.DEBUG)

    def test_parse(self):
        osm_map = os.path.join(os.path.dirname(__file__), "../resources/small.osm")

        parser = OsmParser.create()
        map_result = parser.parse(osm_map)

        self.assertEqual(map_result.__len__(), 0, "Expected N edges on the map")
        # TODO(mv): add test for each edge
