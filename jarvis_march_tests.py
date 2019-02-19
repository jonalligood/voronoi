import unittest
from unittest import TestCase

from geometry import Point
from jarvis_march import ConvexHull


class JarvisMarchTest(TestCase):
    def setUp(self):
        self.point_list = [
            Point(0, 0),
            Point(0, 2),
            Point(0.75, 1.75),
            Point(2, 0),
            Point(2, 2)
        ]

    def test_jarvis_march(self):
        hull = ConvexHull(self.point_list)
        expected_hull = [
            Point(0, 0),
            Point(0, 2),
            Point(2, 2),
            Point(2, 0)
        ]
        self.assertEqual(hull.hull_points, expected_hull)

if __name__ == '__main__':
    unittest.main()
