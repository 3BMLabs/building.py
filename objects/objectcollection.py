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


    def byPoint(self, point:Point, height=int, rotation=None): #add angle rotation
        #Upper pedestal part:
        #head plate 80x80mm
        #thickness 2.8mm
        #Nut: M16
        # top,
        # ffh / ph / ufh

        #TOP
        topfilename = "temp\\jonathan\\pedestal_top.dxf"
        topheight = 3

        #FRAME
        diameter = 10

        #BASE
        basefilename = "temp\\jonathan\\pedestal_foot.dxf"
        baseheight = 3


        top = ReadDXF(topfilename).polycurve
        topcenter = Point.difference(top.centroid(), point)
        top = top.translate(Point.toVector(topcenter))
        x3 = Extrusion.byPolyCurveHeight(top, topheight, 0)

        frame = Rect(Vector3(x=(top.centroid().x)-(diameter/2), y=(top.centroid().y)-(diameter/2),z=point.z-topheight), diameter, diameter)
        x2 = Extrusion.byPolyCurveHeight(frame, height-baseheight-topheight, 0)

        base = ReadDXF(basefilename).polycurve
        basecenter = Point.difference(base.centroid(), point)
        base = base.translate(Point.toVector(basecenter))
        x1 = Extrusion.byPolyCurveHeight(base, baseheight, -height)    

        return x1, x2, x3#Extrusion.merge([x1, x2, x3], name="test")


    pass #pootje, voet diameter(vierkant), verstelbare hoogte inregelen, 


class WurksComputerFloor(): #centerpoint / rotation / panel pattern / ply
    pass #some type of floor object


class WurksFloorFinish():
    pass #direction / pattern / ect


class WorkPlane():
    def __init__(self):
        self.create = self.Fcreate()

    def Fcreate(self):
        return Rect(Vector3(0,0,0), 1000, 1000)