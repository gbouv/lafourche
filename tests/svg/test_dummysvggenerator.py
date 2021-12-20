import unittest
import logging

from lafourche.model import Map
from lafourche.svg import DummySvgGenerator


class TestParser(unittest.TestCase):
    logging.basicConfig(level=logging.DEBUG)

    def test_generate(self):
        """Dummy test to generate a svg file"""
        generator = DummySvgGenerator.create()
        generator.generate(Map([]))
