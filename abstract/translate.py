# [included in BP singlefile]
# [!not included in BP singlefile - start]
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
__url__ = "./abstract/translate.py"


import math
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from abstract.vector import *
from geometry.point import Point
from geometry.curve import Line, PolyCurve
from project.fileformat import project

# [!not included in BP singlefile - end]


class Geometry:
    def Translate(object, v):
        if object.type == 'Point':
            p1 = Point.to_matrix(object)
            v1 = Vector3.to_matrix(v)

            ar1 = np.array([p1])
            ar2 = np.array([v1])

            c = np.add(ar1,ar2)[0]
            return Point(c[0], c[1], c[2])

        elif object.type == 'Line':
            return Line(Geometry.Translate(object.start, v), (Geometry.Translate(object.end, v)))

        elif object.type == "PolyCurve":
            translated_points = []

            # Extract the direction components from the Vector3 object
            direction_x, direction_y, direction_z = v.x, v.y, v.z

            for point in object.points:
                p1 = Point.to_array(point)
                # Apply the translation
                c = np.add(p1, [direction_x, direction_y, direction_z])
                translated_points.append(Point(c[0], c[1], c[2]))

            return PolyCurve.byPoints(translated_points)
        else:
            print(f"[translate] '{object.type}' object is not added yet")