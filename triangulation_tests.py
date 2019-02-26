import unittest
from unittest import TestCase

from geometry import Point, Triangle
from triangulation import Delaunay

class TriangulateTest(TestCase):
    def test_simple_triangulation(self):
        points = [
            Point(0, 0),
            Point(0, 1),
            Point(1, 0),
        ]
        delaunay = Delaunay(points)
        expected_triangles = [
            Triangle(Point(0, 0), Point(0, 1), Point(1, 0)),
        ]
        self.assertEqual(delaunay.triangles, expected_triangles)


    def test_triangulation(self):
        points = [
            Point(0, 0),
            Point(0, 1),
            Point(1, 0),
            Point(1, 1)
        ]
        delaunay = Delaunay(points)
        expected_triangles = [
            Triangle(Point(0, 0), Point(0, 1), Point(1, 0)),
            Triangle(Point(0, 1), Point(1, 0), Point(1, 1))
        ]
        self.assertEqual(delaunay.triangles, expected_triangles)

    def test_triangulation_collinearity_case(self):
        """
        Ensure in the case of the first 3+ points are collinear, it will
        skip until it reaches a non collinear point and begin connecting.
        """
        points = [
            Point(0, 0),
            Point(0, 1),
            Point(0, 2),
            Point(0, 3),
            Point(1, 0)
        ]
        delaunay = Delaunay(points)
        expected_triangles = [
            Triangle(Point(0, 0), Point(0, 1), Point(1, 0)),
            Triangle(Point(0, 1), Point(0, 2), Point(1, 0)),
            Triangle(Point(0, 2), Point(0, 3), Point(1, 0))
        ]
        self.assertEqual(delaunay.triangles, expected_triangles)
        self.assertTrue(delaunay.degenerate)

    def test_triangulation_all_collinear(self):
        """
        A triangulation cannot be produced if all the lines are collinear.
        """
        points = [
            Point(0, 0),
            Point(1, 1),
            Point(2, 2)
        ]
        with self.assertRaises(ValueError):
            delaunay = Delaunay(points)


if __name__ == '__main__':
    unittest.main()
