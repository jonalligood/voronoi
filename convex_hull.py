from random import randint

from geometry import sort_points, Point, Triangle


class ConvexHull(object):
    """
    A polygon that wraps around a given set of points.
    """
    def __init__(self, points):
        # Sort the points first on x, then on y
        sorted_points = sort_points(points)
        self.points = sorted_points
        self.hull_points = []
        self.build()

    def build(self):
        """
        Loops through self.points, building a Triangle ABC. If the triangle is
        Counter Clockwise, point C is more left of point B and is a better
        candidate for being a hull point
        """
        n = len(self.points)
        start_point = 0
        A = 0

        while True:
            self.hull_points.append(self.points[A])
            B = (A + 1) % n  # Loops back around when we get to the last item
                             # in self.points

            for C in range(n):
                clockwise = Triangle(self.points[A], self.points[B], self.points[C]).clockwise

                if clockwise == False:
                    B = C

            # Now B is the point most left with respect to A and is a new
            # hull point.
            A = B

            if A == start_point:
                # We've looped back around and are finished.
                break

    def add_point(self, point):
        """
        Given a point, add it to the list of points and rebuild the hull
        """
        self.points.append(point)
        # The point might already be in the hull
        self.points = sort_points(self.points)

        self.hull_points = []
        self.build()
