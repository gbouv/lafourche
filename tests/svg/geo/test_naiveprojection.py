import unittest

from lafourche.model.geopoint import Geopoint
from lafourche.svg.geo.naiveprojection import NaiveProjection


class TestNaiveProjection(unittest.TestCase):

    def test_naive_projection_canvas_height(self):
        canvas_size = NaiveProjection.get_canvas_size(Geopoint(2.3254, 48.8874), Geopoint(2.3257, 48.88756))
        self.assertEqual(canvas_size, (20, 17))

    def test_naive_projection(self):
        projection = NaiveProjection.create(Geopoint(2.32544, 48.88745), Geopoint(2.32573, 48.88758))
        self.assertEqual(projection.canvas_size(), (20, 13))
        self.assertEqual(projection.project(Geopoint(2.32544, 48.88745)), (0, 13))
        self.assertEqual(projection.project(Geopoint(2.32544, 48.88758)), (0, 0))
        self.assertEqual(projection.project(Geopoint(2.32573, 48.88745)), (20, 13))
        self.assertEqual(projection.project(Geopoint(2.32573, 48.88758)), (20, 0))
        self.assertEqual(projection.project(Geopoint(2.325585, 48.887515)), (10, 6))
