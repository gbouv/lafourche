import os
import unittest

from lafourche.parser import OsmParser
from lafourche.svg import SimpleSvgGenerator


class E2eTest(unittest.TestCase):

    def test_big_map(self):
        input_osm_file = os.path.join(os.path.dirname(__file__), "resources/big.osm")
        output_svg_file = os.path.join(os.path.dirname(__file__), "e2e_test.svg")

        parser = OsmParser()
        internal_map = parser.parse(input_osm_file)

        svg_writer = SimpleSvgGenerator()
        output_file = svg_writer.generate(internal_map)

        os.rename(output_file, output_svg_file)

        self.assertIsNotNone(os.path.exists(output_svg_file))
