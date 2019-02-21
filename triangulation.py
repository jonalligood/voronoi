from copy import copy

from convex_hull import ConvexHull
from geometry import sort_points, Point, Triangle


def find_difference(old_points, new_points):
    """
    Determines what elements in old_points are missing in new_points
    Note: Does not include new elements from new_points
    """
    return set(old_points) - set(new_points)


def triangulate(points):
    points = sort_points(points)
    triangles = []

    # Form a triangle and convex hull from the first 3 points
    starter_hull = [points.pop(0) for i in range(3)]
    convex_hull = ConvexHull(starter_hull)
    first_triangle = Triangle(*starter_hull)
    if first_triangle.is_collinear():
        # The points are on the same line
        # Continue adding points to the convex hull until we get a non
        # collinear point
        while True:
            new_point = points.pop(0)
            new_triangle = Triangle(new_point, *convex_hull.hull_points[-2:])
            # We add the point to the convex hull regardless

            if not new_triangle.is_collinear():
                triangles = build_triangles(new_point, convex_hull.hull_points)
                break
            convex_hull.add_point(new_point)
        else:
            convex_hull.add_point(new_point)
    else:
        triangles.append(Triangle(*starter_hull))

    # Do
    for point in points:
        # Copy convex hull point list
        old_convex_hull = copy(convex_hull.hull_points)
        # Add new point to convex hull
        convex_hull.add_point(point)

        points_to_connect = []
        # Find any displaced points
        displaced = find_difference(old_convex_hull, convex_hull.hull_points)
        # If points were displaced
        if displaced:
            # add to points_to_connect
            points_to_connect.append(displaced)

        # Add the two points next to new_point in convex hull new_point
        new_point_index = convex_hull.hull_points.index(point)
        points_to_connect.append(convex_hull.hull_points[new_point_index-1])
        points_to_connect.append(convex_hull.hull_points[new_point_index+1])

        # Sort points_to_connect on x, y
        points_to_connect = sort_points(points_to_connect)

        # Create triangles and add to triangle_list
        new_triangles = build_triangles(point, points_to_connect)
        triangles += new_triangles
    return triangles


def build_triangles(point, points_to_connect):
    triangle_list = []
    n = len(points_to_connect)
    for i in range(n-1):
        triangle_list.append(
            Triangle(point, points_to_connect[i], points_to_connect[i+1])
        )
    return triangle_list
