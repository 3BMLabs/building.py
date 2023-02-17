# -*- coding: utf8 -*-
#***************************************************************************
#*   Copyright (c) 2023 Jonathan Van der Gouwe & Maarten Vroegindeweij     *
#*   jonathan@3bm.co.nl & maarten@3bm.co.nl                                *
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


import math, os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) #path: PyBuildingSystems
from abstract.vector import Vector3
from abstract.coordinatesystem import CoordinateSystem
from abstract.coordinatesystem import CSGlobal
from geometry.point import Point
from geometry.solid import Extrusion
from library.profile import *

class Frame:
    #Frame
    def __init__(self):
        self.extrusion = Extrusion()
        self.name = "none"
        self.start: Point
        self.end: Point
        self.curve: Line
        self.length: double = 0
        self.coordinatesystem: CoordinateSystem = CSGlobal
        self.verts = []
        self.faces = []

    def byStartpointEndpointProfileName(self, start, end, profile_name, name):
        self.start = start
        self.end = end
        #self.curve = Line(start, end)
        self.curve = findProfile(profile_name)[0].curve
        self.directionvector = Vector3.byTwoPoints(start, end)
        self.length = Vector3.length(self.directionvector)
        self.name = name
        self.extrusion = Extrusion().byPolyCurveHeightVector(self.curve, self.length, CSGlobal, start, self.directionvector)
        self.verts = self.extrusion[0]
        self.faces = self.extrusion[1]

    def byStartpointEndpoint(self, start, end, polycurve, name):
        self.start = start
        self.end = end
        #self.curve = Line(start, end)
        self.directionvector = Vector3.byTwoPoints(start, end)
        self.length = Vector3.length(self.directionvector)
        self.name = name
        self.extrusion = Extrusion().byPolyCurveHeightVector(polycurve, self.length, CSGlobal, start, self.directionvector)
        self.verts = self.extrusion[0]
        self.faces = self.extrusion[1]