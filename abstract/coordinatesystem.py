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


"""This module provides tools for coordinatesystems
"""

__title__= "coordinatesystem"
__author__ = "Maarten & Jonathan"
__url__ = "./abstract/coordinatesystem.py"


import math, os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) #path: PyBuildingSystems
from abstract.vector import *
from geometry.point import Point as pnt

from packages import helper

class CoordinateSystem: 
    #Origin = Point
    #xaxis = Normalised Vector
    def __init__(self,origin: pnt, xaxis: Vector3, yaxis: Vector3, zaxis: Vector3):
        self.Origin = origin
        self.Xaxis = xaxis
        self.Yaxis = yaxis
        self.Zaxis = zaxis

    def __str__(self):
        return f"{__class__.__name__}(" + f"{self.Origin}, {self.Xaxis}, {self.Yaxis}, {self.Zaxis})"

CSGlobal = CoordinateSystem(pnt(0,0,0), XAxis, YAxis, ZAxis)
