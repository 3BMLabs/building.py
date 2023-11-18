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


"""This module provides tools for dimensions
"""

__title__= "dimension"
__author__ = "Maarten & Jonathan"
__url__ = "./abstract/dimension.py"

import sys, os, math
from pathlib import Path
from typing import Any, List

sys.path.append(str(Path(__file__).resolve().parents[1]))

from abstract.vector import *
from geometry.point import Point as pnt

# [!not included in BP singlefile - end]
class Dimension:
    def __init__(self, start:float, end:float):
        self.start = start
        self.end = end
        self.interval = None

    @classmethod
    def bystartendcount(self, start: float, end: float, count: int):
        intval = []
        numb = start
        delta = end-start
        for i in range(count):
            intval.append(numb)
            numb = numb + (delta / (count - 1))
        self.interval = intval
        return self
    def __str__(self):
        return f"{__class__.__name__}"



# import sys, math, requests, json
# from svg.path import parse_path
# from typing import List, Tuple
# from pathlib import Path

# sys.path.append(str(Path(__file__).resolve().parents[1]))

# from exchange.speckle import TransportToSpeckle, translateObjectsToSpeckleObjects
# from geometry.point import Point
# from geometry.curve import PolyCurve, Line
# from abstract.vector import Vector3
# from abstract.intersect2 import *

# p1 = Point(5,5,4)
# q1 = Point(10,10,6)
# p2 = Point(5,5,5)
# q2 = Point(10,10,3)

# lx2 = Line(p1, q1)
# lx3 = Line(p2, q2)
# intersection_point = Intersect().getIntersect(lx2, lx3)

# obj = [lx2, lx3, intersection_point]

# SpeckleHost = "3bm.exchange"
# StreamID = "fa4e56aed4"
# SpeckleObjects = obj
# Message = "Shiny commit 170"
# SpeckleObj = translateObjectsToSpeckleObjects(obj)
# Commit = TransportToSpeckle(SpeckleHost, StreamID, SpeckleObj, Message)