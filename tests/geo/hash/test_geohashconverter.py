import logging
import unittest

from lafourche.geo.hash import GeohashConverter


class TestGeohashConverter(unittest.TestCase):
    logging.basicConfig(level=logging.DEBUG)

    def test_decode(self):
        geohash = "u09tvmm"
        converter = GeohashConverter()

        square = converter.decode(geohash)
        min_lon = square[0][0]
        min_lat = square[0][1]
        max_lon = square[1][0]
        max_lat = square[1][1]
        self.assertAlmostEqual(min_lon, 2.34695434, places=6)
        self.assertAlmostEqual(max_lon, 2.34832763, places=6)
        self.assertAlmostEqual(min_lat, 48.85208129, places=6)
        self.assertAlmostEqual(max_lat, 48.85345458, places=6)

    def test_decode_2(self):
        geohash = "1gub000"

        converter = GeohashConverter()

        square = converter.decode(geohash)
        min_lon = square[0][0]
        min_lat = square[0][1]
        max_lon = square[1][0]
        max_lat = square[1][1]
        self.assertAlmostEqual(min_lon, -94.57031250, places=6)
        self.assertAlmostEqual(max_lon, -94.56893920, places=6)
        self.assertAlmostEqual(min_lat, -68.90625000, places=6)
        self.assertAlmostEqual(max_lat, -68.90487670, places=6)

    def test_decode_invalid(self):
        geohash = "gui"
        converter = GeohashConverter()

        square = converter.decode(geohash)
        self.assertIsNone(square)
