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
    for p in segment:
        project.objects.append(Point(p[0],p[1],0))
    print(segment)
########################################


project.toSpeckle("5ab2faedba")