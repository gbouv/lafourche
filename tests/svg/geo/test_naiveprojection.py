import unittest

from lafourche.svg.geo.naiveprojection import NaiveProjection


class TestNaiveProjection(unittest.TestCase):

    def test_naive_projection_canvas_height(self):
        height = NaiveProjection.get_canvas_height(256, (2.32544, 48.88745), (2.32573, 48.88758))
        self.assertEqual(height, 115)

    def test_naive_projection(self):
        projection = NaiveProjection.create(256, (2.32544, 48.88745), (2.32573, 48.88758))
        self.assertEqual(projection.canvas_size(), (256, 115))
        self.assertEqual(projection.project(2.32544, 48.88745), (-128, -58))
        self.assertEqual(projection.project(2.32544, 48.88758), (-128, 58))
        self.assertEqual(projection.project(2.32573, 48.88745), (128, -58))
        self.assertEqual(projection.project(2.32573, 48.88758), (128, 58))
        self.assertEqual(projection.project(2.325585, 48.887515), (0, 0))
