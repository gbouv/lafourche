import unittest

from lafourche.model.geopoint import Geopoint
from lafourche.svg.geo.naiveprojection import NaiveProjection


class TestNaiveProjection(unittest.TestCase):

    def test_naive_projection_canvas_height(self):
        height = NaiveProjection.get_canvas_height(256, Geopoint(2.32544, 48.88745), Geopoint(2.32573, 48.88758))
        self.assertEqual(height, 115)

    def test_naive_projection(self):
        projection = NaiveProjection.create(256, Geopoint(2.32544, 48.88745), Geopoint(2.32573, 48.88758))
        self.assertEqual(projection.canvas_size(), (256, 115))
        self.assertEqual(projection.project(Geopoint(2.32544, 48.88745)), (0, 115))
        self.assertEqual(projection.project(Geopoint(2.32544, 48.88758)), (0, 0))
        self.assertEqual(projection.project(Geopoint(2.32573, 48.88745)), (256, 115))
        self.assertEqual(projection.project(Geopoint(2.32573, 48.88758)), (256, 0))
        self.assertEqual(projection.project(Geopoint(2.325585, 48.887515)), (128, 58))
