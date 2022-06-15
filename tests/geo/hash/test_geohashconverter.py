import logging
import unittest

from lafourche.geo.hash import GeohashConverter
from lafourche.model.geopoint import Geopoint


class TestGeohashConverter(unittest.TestCase):
    logging.basicConfig(level=logging.DEBUG)

    def test_decode(self):
        geohash = "u09tvmm"
        converter = GeohashConverter()

        square = converter.decode(geohash)
        bottom_left = square[0]
        top_right = square[1]
        self.assertAlmostEqual(bottom_left.lon, 2.34695434, places=6)
        self.assertAlmostEqual(top_right.lon, 2.34832763, places=6)
        self.assertAlmostEqual(bottom_left.lat, 48.85208129, places=6)
        self.assertAlmostEqual(top_right.lat, 48.85345458, places=6)

    def test_decode_2(self):
        geohash = "1gub000"

        converter = GeohashConverter()

        square = converter.decode(geohash)
        bottom_left = square[0]
        top_right = square[1]
        self.assertAlmostEqual(bottom_left.lon, -94.57031250, places=6)
        self.assertAlmostEqual(top_right.lon, -94.56893920, places=6)
        self.assertAlmostEqual(bottom_left.lat, -68.90625000, places=6)
        self.assertAlmostEqual(top_right.lat, -68.90487670, places=6)

    def test_decode_invalid(self):
        geohash = "gui"
        converter = GeohashConverter()

        square = converter.decode(geohash)
        self.assertIsNone(square)

    def test_encode_1(self):
        converter = GeohashConverter()

        geohash = converter.encode(Geopoint(2.3475, 48.8525), 6)
        self.assertEqual(geohash, "u09tvm")

    def test_encode_2(self):
        converter = GeohashConverter()

        geohash = converter.encode(Geopoint(-94.5695, -68.9055), 6)
        self.assertEqual(geohash, "1gub00")
