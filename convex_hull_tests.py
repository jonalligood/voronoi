import unittest
from unittest import TestCase

from geometry import Point
from convex_hull import ConvexHull


class ConvexHullTest(TestCase):
    def setUp(self):
        self.point_list = [
            Point(0, 0),
            Point(0, 2),
            Point(0.75, 1.75),
            Point(2, 0),
            Point(2, 2)
        ]
        self.expected_hull = [
            Point(0, 0),
            Point(0, 2),
            Point(2, 2),
            Point(2, 0)
        ]


    def test_convex_hull(self):
        hull = ConvexHull(self.point_list)
        self.assertEqual(hull.hull_points, self.expected_hull)

    def test_convex_hull_unsorted_points(self):
        """
        ConvexHull should be able to handle being passed unsorted points.
        """
        unsorted_points = [
            Point(2, 2),
            Point(0.75, 1.75),
            Point(2, 0),
            Point(0, 0),
            Point(0, 2)
        ]
        hull = ConvexHull(unsorted_points)
        self.assertEqual(hull.hull_points, self.expected_hull)


if __name__ == '__main__':
    unittest.main()
