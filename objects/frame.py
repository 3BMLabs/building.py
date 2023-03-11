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


"""This module provides tools for the modelling of framing components. Almost every object in a building is a frame
"""

__title__= "shape"
__author__ = "Maarten & Jonathan"
__url__ = "./objects/frame.py"


import sys, os, math
from pathlib import Path

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

from abstract.vector import Vector3
from abstract.coordinatesystem import CoordinateSystem
from abstract.coordinatesystem import CSGlobal
from geometry.point import Point
from geometry.curve import Line 
from geometry.solid import Extrusion
from library.profile import *


class Frame:
    #Frame
    def __init__(self):
        self.extrusion = None
        self.name = "none"
        self.start: Point
        self.end: Point
        self.curve: Line
        self.length: float = 0
        self.coordinateSystem: CoordinateSystem = CSGlobal
        self.YJustification = "Origin"
        self.ZJustification = "Origin"
        self.YOffset = 0
        self.ZOffset = 0

    @classmethod
    def byStartpointEndpointProfileName(cls, start, end, profile_name, name):
        f1 = Frame()
        f1.start = start
        f1.end = end
        #self.curve = Line(start, end)
        f1.curve = profiledataToShape(profile_name)[0].curve
        f1.directionVector = Vector3.byTwoPoints(start, end)
        f1.length = Vector3.length(f1.directionVector)
        f1.name = name
        f1.extrusion = Extrusion.byPolyCurveHeightVector(f1.curve, f1.length, CSGlobal, start, f1.directionVector)
        return f1

    @classmethod
    def byStartpointEndpoint(cls, start, end, polycurve, name):
        #2D polycurve
        f1 = Frame()
        f1.start = start
        f1.end = end
        #self.curve = Line(start, end)
        f1.directionVector = Vector3.byTwoPoints(start, end)
        f1.length = Vector3.length(f1.directionVector)
        f1.name = name
        f1.extrusion = Extrusion.byPolyCurveHeightVector(polycurve, f1.length, CSGlobal, start, f1.directionVector)
        return f1