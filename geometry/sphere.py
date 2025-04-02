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


# [!not included in BP singlefile - end]

from abstract.serializable import Serializable
from abstract.vector import Point
from geometry.plane import Plane


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

class Circle:
	"""Represents a circle with a specific radius, plane, and length.
	"""
	def __init__(self, radius: 'float', plane: 'Plane', length: 'float') -> 'Circle':
		"""The Circle class defines a circle by its radius, the plane it lies in, and its calculated length (circumference).

		- `radius` (float): The radius of the circle.
		- `plane` (Plane): The plane in which the circle lies.
		- `length` (float): The length (circumference) of the circle. Automatically calculated during initialization.
		"""
		self.radius = radius
		self.plane = plane
		self.length = length
		
		pass  # Curve

	def __id__(self):
		"""Returns the ID of the Circle.

		#### Returns:
		`str`: The ID of the Circle in the format "id:{self.id}".
		"""

	def __str__(self) -> 'str':
		"""Generates a string representation of the Circle object.

		#### Returns:
		`str`: A string that represents the Circle object.

		#### Example usage:
		```python
		circle = Circle(radius, plane, length)
		print(circle)
		# Output: Circle(...)
		```
		"""


class Ellipse:
	"""Represents an ellipse defined by its two radii and the plane it lies in."""
	def __init__(self, firstRadius: 'float', secondRadius: 'float', plane: 'Plane') -> 'Ellipse':
		"""The Ellipse class describes an ellipse through its major and minor radii and the plane it occupies.
			
		- `firstRadius` (float): The first (major) radius of the ellipse.
		- `secondRadius` (float): The second (minor) radius of the ellipse.
		- `plane` (Plane): The plane in which the ellipse lies.
		"""
		self.firstRadius = firstRadius
		self.secondRadius = secondRadius
		self.plane = plane
		
		pass  # Curve

	def __id__(self):
		"""Returns the ID of the Ellipse.

		#### Returns:
		`str`: The ID of the Ellipse in the format "id:{self.id}".
		"""
		return f"id:{self.id}"

	def __str__(self) -> 'str':
		"""Generates a string representation of the Ellipse object.

		#### Returns:
		`str`: A string that represents the Ellipse object.

		#### Example usage:
		```python
		ellipse = Ellipse(firstRadius, secondRadius, plane)
		print(ellipse)
		# Output: Ellipse(...)
		```
		"""
		return f"{__class__.__name__}({self})"