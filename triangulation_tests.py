import unittest
from unittest import TestCase

from geometry import Point, Triangle
from triangulation import triangulate

class TriangulateTest(TestCase):
    def test_simple_triangulation(self):
        points = [
            Point(0, 0),
            Point(0, 1),
            Point(1, 0),
        ]
        triangles = triangulate(points)
        expected_triangles = [
            Triangle(Point(0, 0), Point(0, 1), Point(1, 0)),
        ]
        self.assertEqual(triangles[0], expected_triangles[0])


    def test_triangulation(self):
        points = [
            Point(0, 0),
            Point(0, 1),
            Point(1, 0),
            Point(1, 1)
        ]
        triangles = triangulate(points)
        expected_triangles = [
            Triangle(Point(0, 0), Point(0, 1), Point(1, 0)),
            Triangle(Point(0, 1), Point(1, 0), Point(1, 1))
        ]
        self.assertEqual(triangles, expected_triangles)

if __name__ == '__main__':
    unittest.main()
