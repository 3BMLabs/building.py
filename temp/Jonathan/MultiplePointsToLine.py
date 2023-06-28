import sys, math, requests, json, cv2
from svg.path import parse_path
from typing import List, Tuple
from pathlib import Path
import numpy as np


sys.path.append(str(Path(__file__).resolve().parents[2]))

from exchange.speckle import TransportToSpeckle, translateObjectsToSpeckleObjects
from geometry.point import Point
from geometry.curve import *
from abstract.vector import Vector3
from abstract.intersect2d import *
from abstract.plane import Plane
from abstract.text import Text
from abstract.intersect2d import Intersect2d
from objects.datum import *
from geometry.solid import Extrusion
from objects.panel import Panel
from abstract.color import Color
from geometry.surface import Surface
from geometry.geometry2d import *

########################################
def get_line_segments(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    line_segments = []

    for contour in contours:
        epsilon = 0.01 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        segment = [tuple(point[0]) for point in approx]
        line_segments.append(segment)

    return line_segments

image_path = "temp/Jonathan/output.png"#"output.png"
segments = get_line_segments(image_path)

for segment in segments:
    # for p in segment:
    #     project.objects.append(Point(p[0],p[1],0))
    # print(segment)



# segment = [(273, 0), (272, 0), (272, 1), (271, 2), (271, 3), (270, 4), (270, 5), (271, 5), (271, 4), (272, 3), (272, 2), (273, 1)]
# segment1 = [(293, 0), (292, 0), (290, 2), (290, 3), (291, 3), (292, 2), (292, 1)]
    avg_x = sum(point[0] for point in segment) / len(segment)
    avg_y = sum(point[1] for point in segment) / len(segment)

    start_point = segment[0]
    end_point = segment[0]

    for point in segment:
        # project.objects.append(Point2D(point[0], point[1]))
        if point[0] < start_point[0]:
            start_point = point
        if point[0] > end_point[0]:
            end_point = point
    # print(start_point, end_point)

    project.objects.append(Line(start=Point2D(start_point[0], start_point[1]), end=Point2D(end_point[0], end_point[1])))


########################################


project.toSpeckle("5ab2faedba")