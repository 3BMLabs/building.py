# [included in BP singlefile]
# [!not included in BP singlefile - start]
# -*- coding: utf8 -*-
# ***************************************************************************
# *   Copyright (c) 2024 Maarten Vroegindeweij & Jonathan van der Gouwe      *
# *   maarten@3bm.co.nl & jonathan@3bm.co.nl                                *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with this program; if not, write to the Free Software   *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************

"""This module contains sphere math
"""


__title__ = "sphere"
__author__ = "JohnHeikens"
__url__ = "./geometry/sphere.py"

import math
import sys
from pathlib import Path

from geometry.vector import Vector


sys.path.append(str(Path(__file__).resolve().parents[1]))

from abstract.text import *

from geometry.curve import Line
# [!not included in BP singlefile - end]

from abstract.serializable import Serializable
from geometry.point import Point


class Sphere(Serializable):
	def __init__(self, point:Point, diameter:int):
		self.point = point
		self.diameter = diameter
        
	def __str__(self) -> str:
		return str(Sphere)

	@staticmethod
	def radius_by_3_points(start:float, mid: float, end: float) -> float:
		a = Point.distance(start, mid)
		b = Point.distance(mid, end)
		c = Point.distance(end, start)
		s = (a + b + c) / 2
		A = math.sqrt(max(s * (s - a) * (s - b) * (s - c), 0))
				
		if abs(A) < 1e-6:
			return float('inf')
		else:
			R = (a * b * c) / (4 * A)
			return R