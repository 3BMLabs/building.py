# [included in BP singlefile]
# [!not included in BP singlefile - start]
# -*- coding: utf8 -*-
#***************************************************************************
#*   Copyright (c) 2024 Maarten Vroegindeweij & Jonathan van der Gouwe      *
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


"""This module provides tools for boundingbox
"""

__title__= "coordinatesystem"
__author__ = "Maarten & Jonathan"
__url__ = "./abstract/boundingbox.py"


import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from geometry.geometry2d import Point2D, PolyCurve2D
from geometry.point import Point
from geometry.curve import PolyCurve, Line
from abstract.coordinatesystem import CoordinateSystem, CSGlobal
from abstract.vector import Vector3
from geometry.solid import Extrusion
from helper import *


# [!not included in BP singlefile - end]

class BoundingBox2d:
    def __init__(self):
        self.id = generateID()
        self.type = __class__.__name__
        self.points = []
        self.corners = []
        self.isClosed = True
        self.length = 0
        self.width = 0
        self.z = 0

    def serialize(self):
        id_value = str(self.id) if not isinstance(self.id, (str, int, float)) else self.id
        return {
            'id': id_value,
            'points': self.points,
            'corners': self.corners,
            'isClosed': self.isClosed,
            'length': self.length,
            'width': self.width,
            'z': self.z
        }

    @staticmethod
    def deserialize(data):
        bounding_box = BoundingBox2d()
        bounding_box.id = data.get('id')
        bounding_box.points = data.get('points', [])
        bounding_box.corners = data.get('corners', [])
        bounding_box.isClosed = data.get('isClosed', True)
        bounding_box.length = data.get('length', 0)
        bounding_box.width = data.get('width', 0)
        bounding_box.z = data.get('z', 0)

        return bounding_box

    def _length(self):
        return 0
    
    def area(self):
        return 0

    def byPoints(self, points=Point):
        self.points = points
        x_values = [point.x for point in self.points]
        y_values = [point.y for point in self.points]

        min_x = min(x_values)
        max_x = max(x_values)
        min_y = min(y_values)
        max_y = max(y_values)


        left_top = Point(x=min_x, y=max_y, z=self.z)
        left_bottom = Point(x=min_x, y=min_y, z=self.z)
        right_top = Point(x=max_x, y=max_y, z=self.z)
        right_bottom = Point(x=max_x, y=min_y, z=self.z)
        self.length = abs(Point.distance(left_top, left_bottom))
        self.width = abs(Point.distance(left_top, right_top))
        self.corners.append(left_top) 
        self.corners.append(left_bottom) 
        self.corners.append(right_bottom)
        self.corners.append(right_top)
        return self
    
    def byDimensions(self, length:float, width:float):
        # startpoint = Point2D(0,0)
        # widthpoint = Point2D(0,width)
        # widthlengthpoint = Point2D(length,width)
        # lengthpoint = Point2D(length,0)

        half_length = length / 2
        half_width = width / 2

        startpoint = Point2D(-half_length, -half_width)
        widthpoint = Point2D(-half_length, half_width)
        widthlengthpoint = Point2D(half_length, half_width)
        lengthpoint = Point2D(half_length, -half_width)

        self.points.append(startpoint)
        self.corners.append(startpoint)
        self.points.append(widthpoint)
        self.corners.append(widthpoint)
        self.points.append(widthlengthpoint)
        self.corners.append(widthlengthpoint)
        self.points.append(lengthpoint)
        self.corners.append(lengthpoint)

        self.length = length
        self.width = width
        return self


class BoundingBox3d:
    def __init__(self, points=Point):
        self.id = generateID()
        self.type = __class__.__name__        
        self.points = points
        self.boundingbox2d = None
        self.coordinatesystem = None
        self.height = None

    def serialize(self):
        id_value = str(self.id) if not isinstance(self.id, (str, int, float)) else self.id
        return {
            'id': id_value,
            'type': self.type,
            'points': [point.serialize() for point in self.points]
        }

    @staticmethod
    def deserialize(data):
        points = [Point.deserialize(point_data) for point_data in data.get('points', [])]
        return BoundingBox3d(points)

    def corners(self, points=Point):
        x_values = [point.x for point in self.points]
        y_values = [point.y for point in self.points]
        z_values = [point.z for point in self.points]

        min_x = min(x_values)
        max_x = max(x_values)
        min_y = min(y_values)
        max_y = max(y_values)
        min_z = min(z_values)
        max_z = max(z_values)

        left_top_bottom = Point(x=min_x, y=max_y, z=min_z)
        left_bottom_bottom = Point(x=min_x, y=min_y, z=min_z)
        right_top_bottom = Point(x=max_x, y=max_y, z=min_z)
        right_bottom_bottom = Point(x=max_x, y=min_y, z=min_z)
        
        left_top_top = Point(x=min_x, y=max_y, z=max_z)
        left_bottom_top = Point(x=min_x, y=min_y, z=max_z)
        right_top_top = Point(x=max_x, y=max_y, z=max_z)
        right_bottom_top = Point(x=max_x, y=min_y, z=max_z)

        return [left_top_bottom, left_top_top, right_top_top, right_top_bottom, left_top_bottom, left_bottom_bottom, left_bottom_top, left_top_top, left_bottom_top, right_bottom_top, right_bottom_bottom, left_bottom_bottom, right_bottom_bottom, right_top_bottom, right_top_top, right_bottom_top]

    def perimeter(self):
        return PolyCurve.byPoints(self.corners(self.points))
    
    def convertBoundingbox2d(self, boundingbox2d:BoundingBox2d, coordinatesystem: CoordinateSystem, height=float):
        self.boundingbox2d = boundingbox2d
        self.coordinatesystem = coordinatesystem
        self.height = height
        return self
    
    def toCuboid(self) -> Extrusion:
        pts = self.boundingbox2d.corners
        pc = PolyCurve2D.byPoints(pts)
        height = self.height
        cs = self.coordinatesystem
        dirXvector = Vector3.angleBetween(CSGlobal.Yaxis, cs.Yaxis)
        pcrot = pc.rotate(dirXvector) #bug multi direction
        cuboid = Extrusion.byPolyCurveHeightVector(pcrot, height, CSGlobal, cs.Origin, cs.Zaxis)
        return cuboid
    
    def toAxis(self, length:int=None) -> Line:
        if length == None:
            length = 1000
        cs = self.coordinatesystem
        lnX = Line.ByStartPointDirectionLength(cs.Origin, cs.Xaxis, length)
        lnY = Line.ByStartPointDirectionLength(cs.Origin, cs.Yaxis, length)
        lnZ = Line.ByStartPointDirectionLength(cs.Origin, cs.Zaxis, length)
        return [lnX, lnY, lnZ]
    