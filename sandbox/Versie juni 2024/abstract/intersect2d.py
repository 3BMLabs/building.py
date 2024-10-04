# [included in BP singlefile]
# [!not included in BP singlefile - start]
# -*- coding: utf8 -*-
# ***************************************************************************
# *   Copyright (c) 2024 Maarten Vroegindeweij & Jonathan van der Gouwe      *
# *   maarten@3bm.co.nl & jonathan@3bm.co.nl                                *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with this program; if not, write to the Free Software   *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************


"""This module provides tools for intersects
"""

__title__ = "intersect"
__author__ = "Maarten & Jonathan"
__url__ = "./abstract/intersect.py"

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from packages.helper import *
from geometry.geometry2d import *

# [!not included in BP singlefile - end]

#intersect class?
def perp(a):
    """Calculates a perpendicular vector to the given vector `a`.
    This function calculates a vector that is perpendicular to the given 2D vector `a`. The returned vector is in the 2D plane and rotated 90 degrees counterclockwise.

    #### Parameters:
    - `a` (list[float]): A 2D vector represented as a list of two floats, `[x, y]`.

    #### Returns:
    `list[float]`: A new 2D vector that is perpendicular to `a`.

    #### Example usage:
    ```python
    vector_a = [1, 0]
    perp_vector = perp(vector_a)
    # Expected output: [0, 1], representing a vector perpendicular to `vector_a`.
    ```
    """
    b = [None] * len(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b


def get_line_intersect(line_1: 'Line2D', line_2: 'Line2D') -> 'Point2D':
    """Calculates the intersection point of two lines if they intersect.
    This function computes the intersection point of two lines defined by `line_1` and `line_2`. If the lines are parallel or coincide, the function returns `None`.

    #### Parameters:
    - `line_1` (Line2D): The first line, represented by its start and end points.
    - `line_2` (Line2D): The second line, represented by its start and end points.

    #### Returns:
    `Point2D` or `None`: The intersection point of `line_1` and `line_2` if they intersect; otherwise, `None`.

    #### Example usage:
    ```python
    line_1 = Line2D(Point2D(0, 0), Point2D(1, 1))
    line_2 = Line2D(Point2D(1, 0), Point2D(0, 1))
    intersection = get_line_intersect(line_1, line_2)
    # Expected output: Point2D(0.5, 0.5), the intersection point.
    ```
    """

    if line_1.start == line_1.end or line_2.start == line_2.end:
        return None

    p1, p2 = line_1.start, line_1.end
    p1X, p1Y = p1.x, p1.y
    p2X, p2Y = p2.x, p2.y

    p3, p4 = line_2.start, line_2.end
    p3X, p3Y = p3.x, p3.y
    p4X, p4Y = p4.x, p4.y

    da = [p2X - p1X, p2Y - p1Y]
    db = [p4X - p3X, p4Y - p3Y]
    dp = [p1X - p3X, p1Y - p3Y]
    dap = perp(da)
    denom = dap[0] * db[0] + dap[1] * db[1]
    if abs(denom) < 1e-6:
        return None
    num = dap[0] * dp[0] + dap[1] * dp[1]
    t = num / denom
    nX, nY = p3X + t * db[0], p3Y + t * db[1]

    return Point2D(nX, nY)


def get_multi_lines_intersect(lines: list[Line2D]) -> list[Point2D]:
    """Finds intersection points between multiple Line2D objects.
    This function iterates through a list of Line2D objects, calculates intersections between each pair of lines, and returns a list of unique intersection points. If a line does not intersect or the intersection point is not on the line segment, it is ignored.

    #### Parameters:
    - `lines` (list[Line2D]): A list of Line2D objects.

    #### Returns:
    `list[Point2D]`: A list of Point2D objects representing the intersection points.

    #### Example usage:
    ```python
    line1 = Line2D(Point2D(0, 0), Point2D(10, 10))
    line2 = Line2D(Point2D(0, 10), Point2D(10, 0))
    lines = [line1, line2]
    intersections = get_multi_lines_intersect(lines)
    # Expected output: [Point2D(5, 5)], the intersection point of the two lines.
    ```
    """

    pts = []
    for i in range(len(lines)):
        line1 = lines[i]
        for j in range(i+1, len(lines)):
            line2 = lines[j]
            intersection = get_line_intersect(line1, line2)
            if intersection not in pts and intersection != None and is_point_on_line_segment(intersection, line2) == True:
                pts.append(intersection)
    return pts


def get_intersect_polycurve_lines(polycurve: PolyCurve2D, lines: list[Line2D], split: bool = False, stretch: bool = False):
    """Calculates intersections between a PolyCurve2D and multiple Line2D objects, with options to split and stretch lines.
    This function identifies intersection points between a PolyCurve2D and a list of Line2D objects. It supports stretching lines to intersect across the entire polycurve and splitting lines at intersection points. The function returns a dictionary containing intersection points, split lines, and categorized lines as either inner or outer grid lines based on their location relative to the polycurve.

    #### Parameters:
    - `polycurve` (PolyCurve2D): The PolyCurve2D object to test for intersections.
    - `lines` (list[Line2D]): A list of Line2D objects to test for intersections with the polycurve.
    - `split` (bool): If True, splits lines at their intersection points. Defaults to False.
    - `stretch` (bool): If True, extends lines to calculate intersections across the entire polycurve. Defaults to False.

    #### Returns:
    `dict`: A dictionary containing:
    - `IntersectGridPoints`: A list of intersection points.
    - `SplittedLines`: A list of Line2D objects, split at intersection points if `split` is True.
    - `InnerGridLines`: Lines fully contained within the polycurve.
    - `OuterGridLines`: Lines extending outside the polycurve.

    #### Example usage:
    ```python
    polycurve = PolyCurve2D.by_points([Point2D(0, 0), Point2D(10, 0), Point2D(10, 10), Point2D(0, 10)])
    line = Line2D(Point2D(5, -5), Point2D(5, 15))
    results = get_intersect_polycurve_lines(polycurve, [line], split=True)
    # Expected output: A dictionary with lists of intersection points, split lines, inner and outer grid lines.
    ```
    """
    dict = {}
    intersectionsPointsList = []
    splitedLinesList = []
    InnerGridLines = []
    OuterGridLines = []
    if isinstance(lines, Line2D):
        lines = [lines]
    elif lines.type == "Line":
        print("Convert Line(s) to Line2D")
        sys.exit()
    else:
        print(f"Incorrect input: {lines}")
    for line in lines:
        IntersectGridPoints = []
        for i in range(len(polycurve.points2D) - 1):
            genLine = Line2D(polycurve.points2D[i], polycurve.points2D[i+1])
            checkIntersect = get_line_intersect(genLine, line)
            if stretch == False:
                if checkIntersect != None:
                    if is_point_on_line_segment(checkIntersect, line) == False:
                        checkIntersect = None
                    else:
                        minX = min(
                            polycurve.points2D[i].x, polycurve.points2D[i+1].x)
                        maxX = max(
                            polycurve.points2D[i].x, polycurve.points2D[i+1].x)
                        minY = min(
                            polycurve.points2D[i].y, polycurve.points2D[i+1].y)
                        maxY = max(
                            polycurve.points2D[i].y, polycurve.points2D[i+1].y)
                    if checkIntersect != None:
                        if minX <= checkIntersect.x <= maxX and minY <= checkIntersect.y <= maxY:
                            intersectionsPointsList.append(checkIntersect)
                            IntersectGridPoints.append(checkIntersect)

            elif stretch == True:
                minX = min(polycurve.points2D[i].x, polycurve.points2D[i+1].x)
                maxX = max(polycurve.points2D[i].x, polycurve.points2D[i+1].x)
                minY = min(polycurve.points2D[i].y, polycurve.points2D[i+1].y)
                maxY = max(polycurve.points2D[i].y, polycurve.points2D[i+1].y)
                if checkIntersect != None:
                    if minX <= checkIntersect.x <= maxX and minY <= checkIntersect.y <= maxY:
                        intersectionsPointsList.append(checkIntersect)
                        IntersectGridPoints.append(checkIntersect)

        if split == True:
            if len(IntersectGridPoints) > 0:
                splitedLinesList.append(line.split(IntersectGridPoints))

    for splittedLines in splitedLinesList:
        for line in splittedLines:
            centerLinePoint = line.point_at_parameter(0.5)
            if is_point_in_polycurve(centerLinePoint, polycurve) == True:
                InnerGridLines.append(line)
            else:
                OuterGridLines.append(line)

    dict["IntersectGridPoints"] = intersectionsPointsList
    dict["SplittedLines"] = flatten(splitedLinesList)
    dict["InnerGridLines"] = InnerGridLines
    dict["OuterGridLines"] = OuterGridLines

    return dict


def is_point_on_line_segment(point: 'Point2D', line: 'Line2D') -> 'bool':
    """Checks if a Point2D is on a Line2D segment.
    This function determines whether a given Point2D lies on a specified Line2D segment. It checks if the point is within the line segment's bounding box and calculates its distance from the line to verify its presence on the line.

    #### Parameters:
    - `point` (Point2D): The Point2D object to check.
    - `line` (Line2D): The Line2D object on which the point's presence is to be checked.

    #### Returns:
    `bool`: True if the point lies on the line segment; otherwise, False.

    #### Example usage:
    ```python
    point = Point2D(5, 5)
    line = Line2D(Point2D(0, 0), Point2D(10, 10))
    is_on_segment = is_point_on_line_segment(point, line)
    # Expected output: True, since the point lies on the line segment.
    ```
    """
    x_min = min(line.start.x, line.end.x)
    x_max = max(line.start.x, line.end.x)
    y_min = min(line.start.y, line.end.y)
    y_max = max(line.start.y, line.end.y)

    if x_min <= point.x <= x_max and y_min <= point.y <= y_max:
        try:
            distance = abs((line.end.y - line.start.y) * point.x
                           - (line.end.x - line.start.x) * point.y
                           + line.end.x * line.start.y
                           - line.end.y * line.start.x) \
                / line.length
            return distance < 1e-9
        except:
            return False
    return False


def get_intersection_polycurve_polycurve(polycurve_1: 'PolyCurve2D', polycurve_2: 'PolyCurve2D') -> 'list[Point2D]':
    """Finds intersection points between two PolyCurve2D objects.
    This function calculates the intersection points between all line segments of two PolyCurve2D objects. It iterates through each line segment of the first polycurve and checks for intersections with each line segment of the second polycurve. Intersection points that lie on both line segments are added to the result list.

    #### Parameters:
    - `polycurve_1` (PolyCurve2D): The first polycurve.
    - `polycurve_2` (PolyCurve2D): The second polycurve to intersect with the first one.

    #### Returns:
    `list[Point2D]`: A list of Point2D objects representing the intersection points between the two polycurves.

    #### Example usage:
    ```python
    polycurve1 = PolyCurve2D.by_points([Point2D(0, 0), Point2D(10, 10)])
    polycurve2 = PolyCurve2D.by_points([Point2D(0, 10), Point2D(10, 0)])
    intersections = get_intersection_polycurve_polycurve(polycurve1, polycurve2)
    # Expected output: [Point2D(5, 5)], the intersection point of the two polycurves.
    ```
    """
    points = []
    for i in range(len(polycurve_1.points2D) - 1):
        line1 = Line2D(polycurve_1.points2D[i], polycurve_1.points2D[i+1])
        for j in range(len(polycurve_2.points2D) - 1):
            line2 = Line2D(polycurve_2.points2D[j], polycurve_2.points2D[j+1])
            intersection = get_line_intersect(line1, line2)
            if intersection and is_point_on_line_segment(intersection, line1) and is_point_on_line_segment(intersection, line2):
                points.append(intersection)
    return points


def split_polycurve_at_intersections(polycurve: 'PolyCurve2D', points: 'list[Point2D]') -> 'list[PolyCurve2D]':
    """Splits a PolyCurve2D at specified points and returns the resulting segments as new polycurves.
    This function sorts the given intersection points along the direction of the polycurve. Then it iterates through each segment of the polycurve, checking for intersections with the provided points and splitting the polycurve accordingly. Each segment between intersection points becomes a new PolyCurve2D object.

    #### Parameters:
    - `polycurve` (PolyCurve2D): The polycurve to be split.
    - `points` (list[Point2D]): The points at which to split the polycurve.

    #### Returns:
    `list[PolyCurve2D]`: A list of PolyCurve2D objects representing the segments of the original polycurve after splitting.

    #### Example usage:
    ```python
    polycurve = PolyCurve2D.by_points([Point2D(0, 0), Point2D(5, 5), Point2D(10, 0)])
    points = [Point2D(5, 5)]
    split_polycurves = split_polycurve_at_intersections(polycurve, points)
    # Expected output: 2 new polycurves, one from (0,0) to (5,5) and another from (5,5) to (10,0).
    ```
    """
    points.sort(key=lambda pt: Point2D.distance(polycurve.points2D[0], pt))

    current_polycurve_points = [polycurve.points2D[0]]
    created_polycurves = []

    for i in range(1, len(polycurve.points2D)):
        segment_start = polycurve.points2D[i - 1]
        segment_end = polycurve.points2D[i]

        segment_intersections = [pt for pt in points if is_point_on_line_segment(
            pt, Line2D(segment_start, segment_end))]

        segment_intersections.sort(
            key=lambda pt: Point2D.distance(segment_start, pt))

        for intersect in segment_intersections:
            current_polycurve_points.append(intersect)
            created_polycurves.append(
                polycurve.by_points(current_polycurve_points))
            current_polycurve_points = [intersect]
            points.remove(intersect)

        current_polycurve_points.append(segment_end)

    if len(current_polycurve_points) > 1:
        created_polycurves.append(
            polycurve.by_points(current_polycurve_points))

    ptlist = []
    for index, pc in enumerate(created_polycurves):
        if index == 0:
            for pt in pc.points2D:
                ptlist.append(pt)
        elif index == 2:
            for pt in pc.points2D:
                ptlist.append(pt)
                ptlist.append(ptlist[1])

    pcurve = polycurve().by_points(ptlist)

    try:
        return [created_polycurves[1], pcurve]
    except:
        return [created_polycurves[0]]


# extend to if on edge, then accept
def is_point_in_polycurve(point: 'Point2D', polycurve: 'PolyCurve2D') -> 'bool':
    """Determines if a point is located inside a closed PolyCurve2D.
    The function uses a ray-casting algorithm to count the number of times a horizontal ray starting from the given point intersects the polycurve. If the count is odd, the point is inside; if even, the point is outside.

    #### Parameters:
    - `point` (Point2D): The point to check.
    - `polycurve` (PolyCurve2D): The polycurve to check against.

    #### Returns:
    `bool`: True if the point is inside the polycurve, False otherwise.

    #### Example usage:
    ```python
    polycurve = PolyCurve2D.by_points([Point2D(0, 0), Point2D(10, 0), Point2D(10, 10), Point2D(0, 10)])
    point = Point2D(5, 5)
    inside = is_point_in_polycurve(point, polycurve)
    # Expected output: True, since the point is inside the polycurve.
    ```
    """
    x, y = point.x, point.y
    intersections = 0
    for curve in polycurve.curves:
        p1, p2 = curve.start, curve.end
        if (y > min(p1.y, p2.y)) and (y <= max(p1.y, p2.y)) and (x <= max(p1.x, p2.x)):
            if p1.y != p2.y:
                x_inters = (y - p1.y) * (p2.x - p1.x) / (p2.y - p1.y) + p1.x
                if (p1.x == p2.x) or (x <= x_inters):
                    intersections += 1
    return intersections % 2 != 0


def is_polycurve_in_polycurve(polycurve_1: 'PolyCurve2D', polycurve_2: 'PolyCurve2D') -> 'bool':
    """Checks if all points of one polycurve are inside another polycurve.
    Iterates through each point of `polycurve_1` and checks if it is inside `polycurve_2` using the `is_point_in_polycurve` function. If all points of `polycurve_1` are inside `polycurve_2`, the function returns True; otherwise, it returns False.

    #### Parameters:
    - `polycurve_1` (PolyCurve2D): The polycurve to check if it is inside `polycurve_2`.
    - `polycurve_2` (PolyCurve2D): The polycurve that may contain `polycurve_1`.

    #### Returns:
    `bool`: True if all points of `polycurve_1` are inside `polycurve_2`, False otherwise.

    #### Example usage:
    ```python
    polycurve1 = PolyCurve2D.by_points([Point2D(1, 1), Point2D(2, 2)])
    polycurve2 = PolyCurve2D.by_points([Point2D(0, 0), Point2D(3, 0), Point2D(3, 3), Point2D(0, 3)])
    result = is_polycurve_in_polycurve(polycurve1, polycurve2)
    # Expected output: True, since `polycurve1` is entirely within `polycurve2`.
    ```
    """
    colList = []
    for pt in polycurve_1.points2D:
        if is_point_in_polycurve(pt, polycurve_2):
            colList.append(True)
        else:
            colList.append(False)

    if all_true(colList):
        return True
    else:
        return False


def plane_line_intersection():
    """Calculates the intersection point between a plane and a line in 3D space.
    Given a line defined by a direction and a point on the line, and a plane defined by a normal vector and a point on the plane, this function calculates the intersection point between the line and the plane, if it exists.

    #### Example usage:
    ```python
    line_dir = [1, 2, 3]  # Direction vector of the line
    line_pt = [0, 0, 0]  # A point on the line
    plane_norm = [4, 5, 6]  # Normal vector of the plane
    plane_pt = [1, 1, 1]  # A point on the plane
    intersection_point = plane_line_intersection(line_dir, line_pt, plane_norm, plane_pt)
    print("The intersection point is:", intersection_point)
    # Output: The intersection point coordinates, if an intersection exists.
    ```
    """
    line_dir = [1, 2, 3]
    line_pt = [0, 0, 0]

    plane_norm = [4, 5, 6]
    plane_pt = [1, 1, 1]

    dot_prod = sum([a*b for a, b in zip(line_dir, plane_norm)])

    if dot_prod == 0:
        print("The line is parallel to the plane. No intersection point.")
    else:
        t = sum([(a-b)*c for a, b, c in zip(plane_pt,
                line_pt, plane_norm)]) / dot_prod

        inter_pt = [a + b*t for a, b in zip(line_pt, line_dir)]

        print("The intersection point is", inter_pt)


def split_polycurve_by_points(polycurve: 'PolyCurve2D', points: 'list[Point2D]') -> 'list[PolyCurve2D]':
    """Splits a PolyCurve2D at specified points.
    Given a list of points, this function splits the input polycurve at these points if they lie on the polycurve. Each segment of the polycurve defined by these points is returned as a new PolyCurve2D.

    #### Parameters:
    - `polycurve` (PolyCurve2D): The polycurve to split.
    - `points` (list[Point2D]): A list of points at which the polycurve is to be split.

    #### Returns:
    `list[PolyCurve2D]`: A list of PolyCurve2D objects representing segments of the original polycurve.

    #### Example usage:
    ```python
    polycurve = PolyCurve2D.by_points([Point2D(0, 0), Point2D(5, 5), Point2D(10, 0)])
    split_points = [Point2D(5, 5)]
    split_polycurves = split_polycurve_by_points(polycurve, split_points)
    # Expected output: Two polycurves, one from (0,0) to (5,5) and another from (5,5) to (10,0).
    ```
    Note: The provided code snippet for the function does not include an implementation that matches its description. The implementation details need to be adjusted accordingly.
    """
    from abstract.intersect2d import is_point_on_line_segment

    def splitCurveAtPoint(curve, point):
        if is_point_on_line_segment(point, curve):
            return curve.split([point])
        return [curve]

    split_curves = []
    for curve in polycurve.curves:
        current_curves = [curve]
        for point in points:
            new_curves = []
            for c in current_curves:
                new_curves.extend(splitCurveAtPoint(c, point))
            current_curves = new_curves
        split_curves.extend(current_curves)

    return split_curves


def is_on_line(line: 'Line2D', point: 'Point2D') -> 'bool':
    """Determines if a given point is on a specified line.
    Checks if the given point is exactly at the start or the end point of the line. It does not check if the point lies anywhere else on the line.

    #### Parameters:
    - `line` (Line2D): The line to check against.
    - `point` (Point2D): The point to check.

    #### Returns:
    `bool`: True if the point is exactly at the start or end of the line, False otherwise.

    #### Example usage:
    ```python
    line = Line2D(Point2D(0, 0), Point2D(10, 10))
    point = Point2D(0, 0)
    result = is_on_line(line, point)
    # Expected output: True
    ```
    Note: This function's implementation appears to contain an error in its condition check. The comparison should directly involve the point with line.start and line.end rather than using `Point2D` class in the condition.
    """

    if line.start == Point2D or line.end == Point2D:
        return True
    return False


def split_polycurve_by_line(polycurve: 'PolyCurve2D', line: 'Line2D') -> 'dict':
    """Splits a PolyCurve2D based on its intersection with a Line2D and categorizes the segments.

    This function finds the intersection points between a PolyCurve2D and a Line2D. If exactly two intersection points are found, it splits the PolyCurve2D at these points. The function returns a dictionary containing the original polycurve, the splitted polycurves (if any), and the intersection points.

    #### Parameters:
    - `polycurve` (PolyCurve2D): The polycurve to be split.
    - `line` (Line2D): The line used to split the polycurve.

    #### Returns:
    `dict`: A dictionary with the following keys:
      - `inputPolycurve`: The original polycurve.
      - `splittedPolycurve`: A list of PolyCurve2D objects representing the splitted segments.
      - `nonsplittedPolycurve`: A list containing the original polycurve if no splitting occurred.
      - `IntersectGridPoints`: The intersection points between the polycurve and the line.

    #### Example usage:
    ```python
    polycurve = PolyCurve2D.by_points([Point2D(0, 0), Point2D(5, 5), Point2D(10, 0)])
    line = Line2D(Point2D(0, 5), Point2D(10, 5))
    result_dict = split_polycurve_by_line(polycurve, line)
    # Expected output: Dictionary containing splitted polycurves (if any) and intersection points.
    ```
    Note: The implementation details provided in the description might not fully align with the actual function code. Adjustments might be needed to ensure the function performs as described.
    """

    dict = {}
    pcList = []
    nonsplitted = []
    intersect = get_intersect_polycurve_lines(
        polycurve, line, split=False, stretch=False)
    intersect_points = intersect["IntersectGridPoints"]
    if len(intersect_points) != 2:
        nonsplitted.append(polycurve)
        dict["inputPolycurve"] = [polycurve]
        dict["splittedPolycurve"] = pcList
        dict["nonsplittedPolycurve"] = nonsplitted
        dict["IntersectGridPoints"] = intersect_points
        return dict

    SegsandPoints = []

    for Line in polycurve.curves:
        for intersect_point in intersect_points:
            if is_point_on_line_segment(intersect_point, Line):
                SegsandPoints.append(intersect_point)
                SegsandPoints.append(intersect_point)

        SegsandPoints.append(Line)

    elementen = []
    for item in SegsandPoints:
        elementen.append(item)

    split_lists = []
    current_list = []

    for element in elementen:
        current_list.append(element)

        if len(current_list) > 1 and current_list[-1].type == current_list[-2].type == 'Point2D':
            split_lists.append(current_list[:-1])
            current_list = [element]

    if current_list:
        split_lists.append(current_list)

    merged_list = split_lists[-1] + split_lists[0]

    lijsten = [merged_list, split_lists[1]]

    for lijst in lijsten:
        q = []
        for i in lijst:
            if i.type == "Line2D":
                q.append(i.end)
            elif i.type == "Point2D":
                q.append(i)
        pc = PolyCurve2D.by_points(q)
        pcList.append(pc)

    dict["inputPolycurve"] = [polycurve]
    dict["splittedPolycurve"] = pcList
    dict["nonsplittedPolycurve"] = nonsplitted
    dict["IntersectGridPoints"] = intersect_points

    return dict
