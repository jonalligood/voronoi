from math import sqrt


class Point:
    def __init__(self, x, y):
        # Float the points to ensure Python2 arithmetic
        self.x = float(x)
        self.y = float(y)

    def distance(self, point):
        """
        Determine the euclidean distance between this point and another
        """
        return sqrt((point.x - self.x)**2 + (point.y - self.y)**2)


class Line:
    """
    Parent of LineSegment and ContinuousLine.
    """
    @classmethod
    def intersect(cls, line_1, line_2):
        """
        Determines if two lines intersect, returns None if not found.
        """
        det = line_1.A * line_2.B - line_2.A*line_1.B

        if det == 0:
            # Lines are parallel (same slope)
            return None

        x = (line_2.B*line_1.C - line_1.B*line_2.C)/det
        y = (line_1.A*line_2.C - line_2.A*line_1.C)/det

        intersect_point = Point(x, y)
        return intersect_point

    def get_perpendicular_bisector(self, point):
        """
        With a line being represented by Ax + By = C,
        the line that perpendicularly bisects this line
        would be -Bx + Ay = D

        returns :: ContinousLine
        """
        D = (-1 * self.B * point.x) + (self.A * point.y)
        # Translate -Bx + Ay = D -> Ax + By = C form
        A = -1 * self.B
        B = self.A
        C = D
        return ContinuousLine(A=A, B=B, C=C)


class LineSegment(Line):
    def __init__(self, point_1=None, point_2=None, A=None, B=None, C=None):
        """
        Lines are represented with Ax+By=C
        """
        self.point_1 = point_1
        self.point_2 = point_2

        # Given two points, we can determine A, B, and C
        # A = y2 - y1
        self.A = self.point_2.y - self.point_1.y
        # B = x1 - x2
        self.B = self.point_1.x - self.point_2.x
        # C = A*x1 + B*y1
        self.C = self.A * self.point_1.x + self.B * self.point_1.y

    @classmethod
    def intersect(cls, line_1, line_2):
        intersect_point = super().intersect(line_1, line_2)

        # Check to make sure the point is on both lines
        if line_1.has_point(intersect_point) and line_2.has_point(intersect_point):
            return intersect_point
        else:
            return None

    def has_point(self, point):
        """
        Given a line, and a point, determines if the point is on the line.
        """
        min_x, max_x, min_y, max_y = self.get_min_max_points()

        if not (min_x <= point.x <= max_x):
            # Intersection point isn't on line
            return False

        if not (min_y <= point.y <= max_y):
            # Intersection point isn't on line
            return False

        return True

    def get_min_max_points(self):
        """
        Given a line composed of point_1 and point_2,
        return the min_x, max_x, min_y, max_y
        """
        sorted_x = sorted([self.point_1.x, self.point_2.x])
        sorted_y = sorted([self.point_1.y, self.point_2.y])
        min_x = sorted_x[0]
        max_x = sorted_x[1]
        min_y = sorted_y[0]
        max_y = sorted_y[1]
        return min_x, max_x, min_y, max_y

    def get_midpoint(self):
        scalar_mid_x = (self.point_2.x - self.point_1.x)/2
        x = self.point_1.x + scalar_mid_x
        scalar_mid_y = (self.point_2.y - self.point_1.y)/2
        y = self.point_1.y + scalar_mid_y
        return Point(x, y)


class ContinuousLine(Line):
    """
    With a line being represented by Ax + By = C, this is an
    infinitely continuous line
    """
    def __init__(self, A, B, C):
        self.A = A
        self.B = B
        self.C = C

    def get_y(self, x):
        """Given x, we can calculate y"""
        return (self.C - self.A * x)/self.B


class Triangle:
    def __init__(self, point_1, point_2, point_3):
        self.point_1 = point_1
        self.point_2 = point_2
        self.point_3 = point_3

        self.line_1 = LineSegment(self.point_1, self.point_2)
        self.line_2 = LineSegment(self.point_2, self.point_3)
        self.line_3 = LineSegment(self.point_3, self.point_1)

    @classmethod
    def get_circumcircle(cls, line_1, line_2):
        """
        The three points of a triangle form a circle. The center of
        the circle can be found via the point where the two perpendicular
        bisectors meet.

        returns :: center, radius of the circle
        """
        midpoint_1 = line_1.get_midpoint()
        perpendicular_line_1 = line_1.get_perpendicular_bisector(midpoint_1)

        midpoint_2 = line_2.get_midpoint()
        perpendicular_line_2 = line_2.get_perpendicular_bisector(midpoint_2)

        center = ContinuousLine.intersect(perpendicular_line_1,
                                          perpendicular_line_2)
        radius = center.distance(line_1.point_1)
        return center, radius
