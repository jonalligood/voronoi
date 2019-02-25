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
    def __init__(self, points):
        self.points = sort_points(points)
        self.triangles = []
        self.convex_hull = None

        self.build_initial()
        self.triangulate()

    def build_initial(self):
        """
        Creates the starter Triangle object(s). Built to handle collinearity in
        the starting points.
        """
        # Form a triangle and convex hull from the first 3 points
        starter_hull = [self.points.pop(0) for i in range(3)]
        self.convex_hull = ConvexHull(starter_hull)
        first_triangle = Triangle(*starter_hull)
        if first_triangle.is_collinear():
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
            # Find any displaced points
            displaced = find_difference(old_convex_hull, self.convex_hull.hull_points)
            # If points were displaced
            if displaced:
                # add to points_to_connect
                points_to_connect.append(displaced)

            # Add the two points next to new_point in convex hull new_point
            new_point_index = self.convex_hull.hull_points.index(point)
            points_to_connect.append(self.convex_hull.hull_points[new_point_index-1])
            points_to_connect.append(self.convex_hull.hull_points[new_point_index+1])

            # Sort points_to_connect on x, y
            points_to_connect = sort_points(points_to_connect)

            # Create triangles and add to triangle_list
            new_triangles = self.build_triangles(point, points_to_connect)
            self.triangles += new_triangles

    def build_triangles(self, point, points_to_connect):
        triangle_list = []
        n = len(points_to_connect)
        for i in range(n-1):
            triangle_list.append(
                Triangle(point, points_to_connect[i], points_to_connect[i+1])
            )
        return triangle_list
