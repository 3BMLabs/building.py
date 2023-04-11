# -*- coding: utf8 -*-
#***************************************************************************
#*   Copyright (c) 2023 Maarten Vroegindeweij & Jonathan van der Gouwe      *
#*   maarten@3bm.co.nl & jonathan@3bm.co.nl                                *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   This program is distributed in the hope that it will be useful,       *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Library General Public License for more details.                  *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************


"""This module provides tools to create points
"""

__title__= "point"
__author__ = "Maarten & Jonathan"
__url__ = "./geometry/point.py"


import sys, os, math
from pathlib import Path

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

from abstract.vector import *
from abstract.vector import XAxis, YAxis, ZAxis


from geometry.geometry2d import Point2D
from packages import helper


class Point:
    def __init__(self, x, y, z, id=helper.generateID()):
        self.x: float = 0.0
        self.y: float = 0.0
        self.z: float = 0.0
        self.x = x
        self.y = y
        self.z = z

    def __id__(self):
        return f"id:{self.id}"
        
    def __str__(self) -> str:
        return f"{__class__.__name__}({self.x},{self.y},{self.z})"

    @staticmethod
    def difference(pointxyz1, pointxyz2):
        return Vector3(
            pointxyz2.x - pointxyz1.x,
            pointxyz2.y - pointxyz1.y,
            pointxyz2.z - pointxyz1.z
        )

    @staticmethod
    def translate(point1, vector: Vector3):
        return Point(
            point1.x + vector.X,
            point1.y + vector.Y,
            point1.z + vector.Z
        )

    @staticmethod
    def point2DTo3D(point2D: Point2D):
        return Point(
            point2D.x,
            point2D.y,
            0
        )

    @staticmethod
    def rotateXY(p1, Beta, dz):
        return Point(
            math.cos(math.radians(Beta))*p1.x - math.sin(math.radians(Beta))*p1.y,
            math.sin(math.radians(Beta))*p1.x + math.cos(math.radians(Beta))*p1.y,
            p1.z + dz
        )

    @staticmethod
    def intersect(p1,p2):
        #Intersection of two points
        if p1.x == p2.x and p1.y == p2.y and p1.z == p2.z:
            return 1
        else:
            return 0

class CoordinateSystem:
    #Origin = Point
    #xaxis = Normalised Vector
    def __init__(self,origin: Point, xaxis: Vector3, yaxis: Vector3, zaxis: Vector3):
        self.Origin = origin
        self.Xaxis = xaxis
        self.Yaxis = yaxis
        self.Zaxis = zaxis

    def __str__(self):
        return f"{__class__.__name__}(" + f"{self.Origin}, {self.Xaxis}, {self.Yaxis}, {self.Zaxis})"

CSGlobal = CoordinateSystem(Point(0,0,0), XAxis, YAxis, ZAxis)


def transformPoint(PointLocal: Point, CoordinateSystemOld: CoordinateSystem, NewOriginCoordinateSystem: Point, DirectionVector: Vector3):
    vz = DirectionVector  # LineVector and new Z-axis
    vz = Vector3.normalise(vz)  # NewZAxis
    vx = Vector3.perpendicular(vz)[0]  # NewXAxis
    try:
        vx = Vector3.normalise(vx)  # NewXAxisNormalised
    except:
        vx = Vector3(1,0,0) #In case of vertical element the length is zero
    vy = Vector3.perpendicular(vz)[1]  # NewYAxis
    try:
        vy = Vector3.normalise(vy)  # NewYAxisNormalised
    except:
        vy = Vector3(0,1,0)  #In case of vertical element the length is zero
    P1 = PointLocal #het te transformeren punt
    CSNew = CoordinateSystem(NewOriginCoordinateSystem, vx, vy, vz)
    v1 = Point.difference(CoordinateSystemOld.Origin, CSNew.Origin)
    v2 = Vector3.product(P1.x, CSNew.Xaxis)  # locale transformatie van X
    v3 = Vector3.product(P1.y, CSNew.Yaxis)  # locale transformatie van Y
    v4 = Vector3.product(P1.z, CSNew.Zaxis)  # locale transformatie van Z
    vtot = Vector3(v1.X + v2.X + v3.X + v4.X, v1.Y + v2.Y + v3.Y + v4.Y, v1.Z + v2.Z + v3.Z + v4.Z)
    pointNew = Point.translate(Point(0, 0, 0), vtot)  # Point 0,0,0 moet nog gecheckt worden
    return pointNew