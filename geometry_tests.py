import unittest
from unittest import TestCase

from geometry import Point, LineSegment, ContinuousLine, Triangle


class PointTest(TestCase):
    def setUp(self):
        self.point = Point(1, 1)

    def test_distance(self):
        another_point = Point(3, 1)
        distance = self.point.distance(another_point)
        self.assertEqual(distance, 2)


class LineSegmentTest(TestCase):
    def setUp(self):
        self.A = Point(0, 0)
        self.B = Point(1, 1)
        C = Point(0, 1)
        D = Point(1, 0)
        self.line_1 = LineSegment(self.A, self.B)
        self.line_2 = LineSegment(C, D)

    def test_get_min_max_points(self):
        """
        Make sure even if the line has a negative slope, max_y > min_y
        """
        min_x, max_x, min_y, max_y = self.line_2.get_min_max_points()
        self.assertEqual(min_x, 0)
        self.assertEqual(max_x, 1)
        self.assertEqual(min_y, 0)
        self.assertEqual(max_y, 1)

    def test_has_point(self):
        valid_point = Point(0.5, 0.5)
        invalid_point = Point(1.1, 1)
        self.assertTrue(self.line_1.has_point(valid_point))
        self.assertFalse(self.line_1.has_point(invalid_point))

    def test_intersect(self):
        intersect_point = LineSegment.intersect(self.line_1, self.line_2)
        self.assertEqual(intersect_point.x, 0.5)
        self.assertEqual(intersect_point.y, 0.5)

    def test_get_midpoint(self):
        midpoint = self.line_1.get_midpoint()
        self.assertEqual(midpoint.x, 0.5)
        self.assertEqual(midpoint.y, 0.5)

    def test_get_perpendicular_bisector(self):
        """
        With a line being represented by Ax + By = C,
        the perpendicular bisector would be -Bx + Ay = D
        """
        midpoint = self.line_1.get_midpoint()
        line = self.line_1.get_perpendicular_bisector(midpoint)
        self.assertEqual(line.A, 1)
        self.assertEqual(line.B, 1)
        self.assertEqual(line.C, 1)


class ContinuousLineTest(TestCase):
    def setUp(self):
        self.line = ContinuousLine(A=1.0, B=-1.0, C=0.0)

    def test_get_y(self):
        x = 1.0
        y = self.line.get_y(x)
        self.assertEqual(y, 1.0)

    def test_intersect(self):
        intersecting_line = ContinuousLine(A=-1.0, B=-1.0, C=-1.0)
        point = ContinuousLine.intersect(self.line, intersecting_line)
        self.assertEqual(point.x, 0.5)
        self.assertEqual(point.y, 0.5)


class TriangleTest(TestCase):
    def setUp(self):
        self.A = Point(0, 0)
        self.B = Point(1, 1)
        self.C = Point(0, 2)
        self.line_1 = LineSegment(self.A, self.B)
        self.line_2 = LineSegment(self.B, self.C)
        self.line_3 = LineSegment(self.C, self.A)

    def test_circumcircle(self):
        center, radius = Triangle.get_circumcircle(self.line_1, self.line_2)
        self.assertEqual(center.x, 0)
        self.assertEqual(center.y, 1)
        self.assertEqual(radius, 1)


if __name__ == '__main__':
    unittest.main()
