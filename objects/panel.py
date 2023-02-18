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


"""This module provides tools for the modelling of panel components. a panel can be a floor, wall, panel, ceiling
"""

__title__= "panel"
__author__ = "Maarten & Jonathan"
__url__ = "./objects/panel.py"

import math, os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) #path: PyBuildingSystems
from abstract.vector import Vector3
from abstract.coordinatesystem import CoordinateSystem
from abstract.coordinatesystem import CSGlobal
from geometry.point import Point
from geometry.solid import Extrusion
from library.profile import *

class Panel:
    #Panel
    def __init__(self):
        self.extrusion = Extrusion()
        self.thickness = 0
        self.name = "none"
        self.perimeter: float = 0
        self.coordinatesystem: CoordinateSystem = CSGlobal
        self.verts = []
        self.faces = []
        self.numberFaces = 0

    def byPolyCurveThickness(self, polycurve2D, thickness, directionvector, name):
        self.directionvector = directionvector
        self.name = name
        self.thickness = thickness
        self.extrusion = Extrusion().byPolyCurveHeightVector(polycurve, self.thickness, CSGlobal, start, self.directionvector)
        self.numberFaces = self.extrusion[2]
        self.verts = self.extrusion[0]
        self.faces = self.extrusion[1]
