import sys, math, requests, json
from svg.path import parse_path
from typing import List, Tuple
from pathlib import Path
# https://help.xtools.pro/pro/22.0/en/XTools_Pro_Components/Geometry_Tools/Split_Polygons.htm

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
from geometry.surface import *
from math import fabs

#finish
# l1 = Line(start=Point(230,-1000,0), end=Point(45,1000,0))
# l2 = Line(start=Point(-1000,0,0), end=Point(1230,0,0))
# f1 = Intersect2d().getLineIntersect(l1, l2)
# obj = [l1, l2, f1]


Point1 = Point(1000,4000,0) #b
Point2 = Point(1000,0,0) #b
Point3 = Point(0,0,0) #x
Point4 = Point(0,340,0) #x
Point5 = Point(0,-4000,0) #x
ply1 = PolyCurve.byPoints([Point1, Point2, Point3, Point4, Point5, Point1])


def polycurve_area(ply: PolyCurve) -> float:
    # Create planar projection of the polycurve
    planar_points = [Point(p.x, p.y, 0) for p in ply.points]
    
    # Calculate area of polygon using Shoelace formula
    area = 0.5 * fabs(sum(planar_points[i].x * planar_points[i+1].y - planar_points[i+1].x * planar_points[i].y 
                     for i in range(len(planar_points)-1))) 
    
    return area

area = polycurve_area(ply1)
print(area)