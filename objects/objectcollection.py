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

#OVERAL FOR EACH OBJECT A ROTATION/POSITION
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


    def byPoint(self, point:Point, rotation=None):
        # top,
        # ffh / ph / ufh

        base = Rect(Vector3(0,0,0), 80, 80)
        x1 = Extrusion.byPolyCurveHeight(base, 3, 20)

        frame = Rect(Vector3(35,35,0), 10, 10)
        x2 = Extrusion.byPolyCurveHeight(frame, 120, -100)

        top = Rect(Vector3(0,0,0), 80, 80)
        x3 = Extrusion.byPolyCurveHeight(top, 3, -103)


        return Extrusion.merge([x1, x2, x3], name="test")



    pass #pootje, voet diameter(vierkant), verstelbare hoogte inregelen, 

class WurksComputerFloor(): #centerpoint / rotation / panel pattern / ply
    pass #some type of floor object

class WurksFloorFinish():
    pass #direction / pattern / ect