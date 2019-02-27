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

    def test_triangulation_handles_same_points(self):
        """
        Ensure any duplicate points are removed.
        """
        points = [
            Point(0, 0),
            Point(1, 1),
            Point(1, 1),
            Point(2, 0)
        ]
        delaunay = Delaunay(points)
        expected_triangles = [
            Triangle(Point(0, 0), Point(1, 1), Point(2, 0))
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
        expected_hull =  [
            Point(0, 0),
            Point(0, 1),
            Point(0, 2),
            Point(0, 3),
            Point(1, 0)
        ]
        expected_triangles = [
            Triangle(Point(0, 0), Point(0, 1), Point(1, 0)),
            Triangle(Point(0, 1), Point(0, 2), Point(1, 0)),
            Triangle(Point(0, 2), Point(0, 3), Point(1, 0))
        ]
        self.assertEqual(delaunay.convex_hull.hull_points, expected_hull)
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

    def test_get_neighboring_points(self):
        """
        If the newly added point neighbors the convex hull start point,
        make sure the neighboring points includes the start point.
        """
        points = [
            Point(0, 0),
            Point(0, 2),
            Point(1, 2),
        ]
        delaunay = Delaunay(points)

        new_point = Point(2, 1)
        delaunay.convex_hull.add_point(new_point)

        left_point, right_point = delaunay.get_neighboring_points(new_point)

        self.assertEqual(left_point, Point(1, 2))
        self.assertEqual(right_point, Point(0, 0))


if __name__ == '__main__':
    unittest.main()
