from random import randint

from geometry import Point, Triangle


def jarvis(points):
    """
    Finds the convex hull for a given set of sorted points. Loops through the
    points, building a Triangle ABC. If the triangle is Counter Clockwise,
    point C is more left of point B and is a better candidate for being a hull
    point.
    """
    n = len(points)
    hull = []

    start_point = 0
    A = 0  # The first point is guaranteed to be on the convex hull

    while True:
        hull.append(points[A])
        B = (A + 1) % n # Increases by 1 unless it's the final point in which case
                        # it loops around

        for C in range(n):
            clockwise = Triangle(points[A], points[B], points[C]).clockwise

            if clockwise == False:
                B = C

        # Now B is the most counter clockwise with respect to A
        # Set A as B for next iteration
        A = B

        if A == start_point:
            # Back at the start
            break

    return hull

