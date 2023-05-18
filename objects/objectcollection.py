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


"""This module provides tools for familys/objects
"""

__title__= "plane"
__author__ = "Maarten & Jonathan"
__url__ = "./objects/objectcollection.py"

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from abstract.vector import Vector3
from geometry.point import Point
from geometry.curve import Line, PolyCurve, Rect
from geometry.surface import Surface
from geometry.solid import Extrusion
from exchange.DXF import ReadDXF
from project.fileformat import *
from packages.helper import *
#EVERYWHERE FOR EACH OBJECT A ROTATION/POSITION
#Make sure that the objects can be merged!

class WurksRaster3d:
    def __init__(self, lines: list[Line], bottom: float, top: float): #-320, 20
        self.bottom = Vector3(0, 0, bottom)
        self.top = Vector3(0, 0, top)
        self.name = "x"
        self.lines = lines

    def byLine(self):
        surfList = []
        for line in self.lines:
            pts = []
            pts.append(Point.translate(line.start, self.bottom))
            pts.append(Point.translate(line.end, self.bottom))
            pts.append(Point.translate(line.end, self.top))
            pts.append(Point.translate(line.start, self.top))
            surfList.append(Surface(PolyCurve.byPoints(pts)))
        return surfList

class WurksPedestal(): #place on point (facebased), point = top pedestal
    def __init__(self) -> None: #classes with different tops (must be parameterized)
        pass   
        #type base
        #type frame
        #type top


    def byPoint(self, points:Point or list[Point], height=int, rotation=None): #add angle rotation
        #TOP
        topfilename = "temp\\jonathan\\pedestal_top.dxf"
        topheight = 3

        #FRAME
        diameter = 10

        #BASE
        basefilename = "temp\\jonathan\\pedestal_foot.dxf"
        baseheight = 3

        if isinstance(points, Point):
            points = [points]

        for point in points:
            top = ReadDXF(topfilename).polycurve
            topcenter = Point.difference(top.centroid(), point)
            top = top.translate(Point.toVector(topcenter))
            project.objects.append(Extrusion.byPolyCurveHeight(top, topheight, 0))

            frame = Rect(Vector3(x=(top.centroid().x)-(diameter/2), y=(top.centroid().y)-(diameter/2),z=point.z-topheight), diameter, diameter)
            project.objects.append(Extrusion.byPolyCurveHeight(frame, height-baseheight-topheight, 0))

            base = ReadDXF(basefilename).polycurve
            basecenter = Point.difference(base.centroid(), point)
            base = base.translate(Point.toVector(basecenter))
            project.objects.append(Extrusion.byPolyCurveHeight(base, baseheight, -height)) 

        print(f"{len(points)}* {__class__.__name__} {project.createdTxt}")


    pass #pootje, voet diameter(vierkant), verstelbare hoogte inregelen, 


class WurksComputerFloor(): #centerpoint / rotation / panel pattern / ply
    pass #some type of floor object


class WurksFloorFinish():
    pass #direction / pattern / ect


class WorkPlane():
    def __init__(self):
        self.length = None
        self.width = None

    def create(self, length: float = None, width: float = None) -> str:
        self.length = length or 1000
        self.width = width or 1000

        project.objects.append(Rect(Vector3(0, 0, 0), self.length, self.width))
        print(f"1* {self.__class__.__name__} {project.createdTxt}")