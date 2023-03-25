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
from geometry.geometry2d import *

class Frame:
    #Frame
    def __init__(self):
        self.extrusion = None
        self.name = "none"
        self.profileName = "none"
        self.start = None
        self.end = None
        self.curve = None
        self.length = 0
        self.coordinateSystem: CoordinateSystem = CSGlobal
        self.YJustification = "Origin"  #Top, Center, Origin, Bottom
        self.ZJustification = "Origin" #Left, Center, Origin, Right
        self.YOffset = 0
        self.ZOffset = 0
        self.rotation = 0
        self.color = None

    @classmethod
    def byStartpointEndpointProfileName(cls, start, end, profile_name, name):
        f1 = Frame()
        f1.start = start
        f1.end = end
        #self.curve = Line(start, end)
        f1.curve = profiledataToShape(profile_name).prof.curve
        f1.directionVector = Vector3.byTwoPoints(start, end)
        f1.length = Vector3.length(f1.directionVector)
        f1.name = name
        f1.extrusion = Extrusion.byPolyCurveHeightVector(f1.curve.curves, f1.length, CSGlobal, start, f1.directionVector)
        f1.extrusion.name = name
        f1.profileName = profile_name
        return f1

    @classmethod
    def byStartpointEndpointProfileNameShapevector(cls, start, end, profile_name, name, vector2d: Vector2,rotation):
        f1 = Frame()
        f1.start = start
        f1.end = end
        #self.curve = Line(start, end)
        curv = profiledataToShape(profile_name).prof.curve
        curvrot = curv.rotate(rotation)  #rotation in degrees
        f1.curve = curvrot.translate(vector2d)
        f1.directionVector = Vector3.byTwoPoints(start, end)
        f1.length = Vector3.length(f1.directionVector)
        f1.name = name
        f1.extrusion = Extrusion.byPolyCurveHeightVector(f1.curve.curves, f1.length, CSGlobal, start, f1.directionVector)
        f1.extrusion.name = name
        f1.profileName = profile_name
        return f1

    @classmethod
    def byStartpointEndpointProfileNameJustifiction(cls, start, end, profile_name, name, XJustifiction, YJustifiction,rotation):
        f1 = Frame()
        f1.start = start
        f1.end = end
        #self.curve = Line(start, end)
        curv = profiledataToShape(profile_name).prof.curve
        curvrot = curv.rotate(rotation)  #rotation in degrees
        v1 = justifictionToVector(curvrot,XJustifiction,YJustifiction)
        f1.curve = curv.translate(v1)
        f1.directionVector = Vector3.byTwoPoints(start, end)
        f1.length = Vector3.length(f1.directionVector)
        f1.name = name
        f1.extrusion = Extrusion.byPolyCurveHeightVector(f1.curve.curves, f1.length, CSGlobal, start, f1.directionVector)
        f1.extrusion.name = name
        f1.profileName = profile_name
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
        f1.extrusion.name = name
        f1.profileName = "none"
        return f1