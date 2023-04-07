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


"""This module provides tools for vectors
"""

__title__= "vector"
__author__ = "Maarten & Jonathan"
__url__ = "./abstract/vector.py"

import math
import sys, random
from pathlib import Path
file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

# from geometry.point import *


file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))


from packages import helper

class Vector3:
    def __init__(self, x, y, z):
        self.X = x
        self.Y = y
        self.Z = z

    @staticmethod
    def sum(v1, v2):
        return Vector3(
            v1.X + v2.X,
            v1.Y + v2.Y,
            v1.Z + v2.Z
        )

    @staticmethod #Returns vector perpendicular on the two vectors
    def crossProduct(v1, v2):
        return Vector3(
            v1.Y*v2.Z - v1.Z*v2.Y,
            v1.Z*v2.X - v1.X*v2.Z,
            v1.X*v2.Y - v1.Y*v2.X
        )

    @staticmethod #inwendig product, if zero, then vectors are perpendicular
    def dotProduct(v1, v2):
        return v1.X*v2.X+v1.Y*v2.Y+v1.Z*v2.Z

    @staticmethod
    def product(n, v1): #Same as scale
        return Vector3(
            v1.X*n,
            v1.Y*n,
            v1.Z*n
        )

    @staticmethod
    def length(v1):
        return math.sqrt(v1.X*v1.X+v1.Y*v1.Y+v1.Z*v1.Z)

    @staticmethod
    def pitch(v1, angle):
        return Vector3(
            v1.X,
            v1.Y*math.cos(angle) - v1.Z*math.sin(angle),
            v1.Y*math.sin(angle) + v1.Z*math.cos(angle)
        )

    @staticmethod
    def angleBetween(v1, v2):
        return math.degrees(math.acos((Vector3.dotProduct(v1, v2)/(Vector3.length(v1)*Vector3.length(v2)))))

    @staticmethod
    def reverse(v1):
        return Vector3(
            v1.X*-1,
            v1.Y*-1,
            v1.Z*-1
        )

    @staticmethod
    def perpendicular(v1):
        #Vector Lokale X en Lokale Y haaks op gegeven vector en in globale Z-richting.
        lokX = Vector3(v1.Y,-v1.X,0)
        lokZ = Vector3.crossProduct(v1, lokX)
        if lokZ.Z<0:
            lokZ = Vector3.reverse(lokZ)
        return lokX, lokZ

    @staticmethod
    def normalise(v1):
        scale = 1/Vector3.length(v1)
        return Vector3(
            v1.X*scale,
            v1.Y*scale,
            v1.Z*scale
        )

    @staticmethod
    def byTwoPoints(p1, p2):
        return Vector3(
            p2.x-p1.x,
            p2.y-p1.y,
            p2.z-p1.z
        )

    @staticmethod
    def rotateXY(v1, Beta):
        return Vector3(
            math.cos(Beta)*v1.x - math.sin(Beta)*v1.y,
            math.sin(Beta)*v1.x + math.cos(Beta)*v1.y,
            v1.z
        )

    def __str__(self):
        return f"{__class__.__name__}(" + f"{self.X},{self.Y},{self.Z})"


XAxis = Vector3(1, 0, 0)

YAxis = Vector3(0, 1, 0)

ZAxis = Vector3(0, 0, 1)
