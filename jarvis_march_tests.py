import unittest
from unittest import TestCase

from geometry import Point
from jarvis_march import jarvis


class JarvisMarchTest(TestCase):
    def setUp(self):
        self.point_list = [
            Point(0, 0),
            Point(0, 2),
            Point(1, 1),
            Point(2, 0),
            Point(2, 2)
        ]

    def test_jarvis_march(self):
        hull = jarvis(self.point_list)
        expected_hull = [
            Point(0, 0),
            Point(2, 0),
            Point(2, 2),
            Point(0, 2)
        ]
        self.assertEqual(hull, expected_hull)

if __name__ == '__main__':
    unittest.main()
