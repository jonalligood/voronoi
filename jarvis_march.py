from random import randint

from geometry import Point, Triangle


def jarvis(points):
    n = len(points)
    hull = []

    l = 0
    p = 0 # Position of the start_point

    while True:
        hull.append(points[p])
        q = (p + 1) % n # Increases by 1 unless it's the final point in which case
                    # it loops around

        for i in range(n):
            if Triangle(points[p], points[i], points[q]).clockwise == False:
                q = i

        # Now q is the most counter clockwise with respect to p
        # Set p as q for next iteration
        p = q

        if p == l:
            # Back at the start
            break

    return hull


if __name__ == '__main__':
    point_list = []
    for i in range(1000):
        point_list.append(Point(randint(0, 100), randint(0, 100)))
    # Sort the list
    sorted_points = sorted(point_list, key=lambda p: (p.x, p.y))
    jarvis(sorted_points)

