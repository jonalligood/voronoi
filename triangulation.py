from copy import copy

from convex_hull import ConvexHull
from geometry import sort_points, Point, Triangle


def find_difference(old_points, new_points):
    """
    Determines what elements in old_points are missing in new_points
    Note: Does not include new elements from new_points
    """
    return set(old_points) - set(new_points)


class Delaunay(object):
    """
    Creates the triangulation using a sweep line approach.
    """
    def __init__(self, points):
        self.points = sort_points(points)
        self.triangles = []
        self.convex_hull = None
        self.degenerate = False

        self.build_initial()
        self.triangulate()

    def build_initial(self):
        """
        Creates the starter Triangle object(s). Built to handle collinearity in
        the starting points. In such a case, the produced triangles will be
        degenerate.
        """
        # Form a triangle and convex hull from the first 3 points
        starter_hull = [self.points.pop(0) for i in range(3)]
        self.convex_hull = ConvexHull(starter_hull)
        first_triangle = Triangle(*starter_hull)
        if first_triangle.is_collinear():
            self.degenerate = True
            self.get_collinear_triangles()
        else:
            self.triangles.append(Triangle(*starter_hull))

    def get_collinear_triangles(self):
        """
        In the case of the initial points being on the same line, continue
        adding points to the convex hull until we get the first non-collinear
        point.
        """
        while True:
            if not self.points:
                # All the points are collinear
                raise ValueError("All points provided are collinear and a ",
                                 "triangulation could not be formed.")

            new_point = self.points.pop(0)
            new_triangle = Triangle(new_point, *self.convex_hull.hull_points[-2:])
            # We add the point to the convex hull regardless

            if not new_triangle.is_collinear():
                self.triangles = self.build_triangles(new_point, self.convex_hull.hull_points)
                break
            self.convex_hull.add_point(new_point)
        else:
            self.convex_hull.add_point(new_point)

    def triangulate(self):
        """
        Builds a list of Triangle objects based on the triangles created in
        build_initial.
        """
        for point in self.points:
            # Copy convex hull point list
            old_convex_hull = copy(self.convex_hull.hull_points)
            # Add new point to convex hull
            self.convex_hull.add_point(point)

            points_to_connect = []

            points_to_connect += self.get_displaced_points(old_convex_hull)

            points_to_connect += self.get_neighboring_points(point)

            # Sort points_to_connect on x, y
            points_to_connect = sort_points(points_to_connect)

            # Create triangles and add to triangle_list
            new_triangles = self.build_triangles(point, points_to_connect)
            self.triangles += new_triangles

    def build_triangles(self, point, points_to_connect):
        """
        Creates a list of triangles using point as a corner in every triangle.
        """
        triangle_list = []
        n = len(points_to_connect)
        for i in range(n-1):
            triangle_list.append(
                Triangle(point, points_to_connect[i], points_to_connect[i+1])
            )
        return triangle_list

    def get_displaced_points(self, old_convex_hull):
        """
        Find the points that are no longer part of the convex hull. These will
        form triangles with the newly added point.
        """
        return find_difference(old_convex_hull, self.convex_hull.hull_points)

    def get_neighboring_points(self, point):
        """
        Find the two hull points next to the newly added point in the convex hull
        """
        # Add the two points next to new_point in convex hull new_point
        new_point_index = self.convex_hull.hull_points.index(point)
        return [
            self.convex_hull.hull_points[new_point_index-1],
            self.convex_hull.hull_points[new_point_index+1]
        ]

