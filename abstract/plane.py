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


"""This module provides tools for planes
"""

__title__= "plane"
__author__ = "Maarten & Jonathan"
__url__ = "./abstract/plane.py"

from abstract.vector import *
from geometry.point import Point as pnt

class Plane:
    #Plane is an infinite element in space defined by a point and a normal
    def __init__(self):
        self.Origin = pnt(0, 0, 0)
        self.Normal = Vector3(0, 0, 1)

    @classmethod
    def byTwoVectorsOrigin(cls, v1, v2, origin):
        p1 = Plane()
        p1.Normal = Vector3.normalise(Vector3.crossProduct(v1, v2))
        p1.Origin = origin
        return p1

    def __str__(self):
        return f"{__class__.__name__}(" + f"{self.Origin}, {self.Normal})"

    #TODO
    #byLineAndPoint
    #byOriginNormal
    #byThreePoints