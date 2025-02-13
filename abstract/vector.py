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


"""
Represents a 3D vector with x, y, and z coordinates.
"""

__title__ = "vector"
__author__ = "Maarten & Jonathan"
__url__ = "./abstract/vector.py"

import sys


from geometry.point import *
from packages.helper import *
from geometry.coords import Coords

# [!not included in BP singlefile - end]


class Vector(Coords):
	"""Represents a 3D vector with x, y, and z coordinates."""
	def __init__(self, *args, **kwargs) -> 'Vector':
		"""Initializes a new Vector instance with the given x, y, and z coordinates.

		- `x` (float): X-coordinate of the vector.
		- `y` (float): Y-coordinate of the vector.
		- `z` (float): Z-coordinate of the vector.
		"""
		super().__init__(*args, **kwargs)

	@staticmethod
	def to_line(vector_1: 'Vector', vector_2: 'Vector') -> 'Vector':
		"""Creates a Line object from two vectors.

		#### Parameters:
		- `vector_1` (`Vector`): The start vector of the line.
		- `vector_2` (`Vector`): The end vector of the line.

		#### Returns:
		`Line`: A Line object connecting the two vectors.

		#### Example usage:
		```python
		vector1 = Vector(10, 20, 30)
		vector2 = Vector(2, 4, 5)
		line = Vector.to_line(vector1, vector2)
		# Line(start=Point(X = 10.000, Y = 20.000, Z = 30.000), end=Point(X = 2.000, Y = 4.000, Z = 5.000))
		```
		"""
		from geometry.point import Point
		from geometry.curve import Line
		return Line(start=Point(x=vector_1.x, y=vector_1.y, z=vector_1.z), end=Point(x=vector_2.x, y=vector_2.y, z=vector_2.z))

	@staticmethod
	def by_line(line_1) -> 'Vector':
		"""Computes a vector representing the direction of a given line.
		This method takes a Line object and returns a Vector representing the direction of the line.

		#### Parameters:
		- `line_1` (`Line`): The Line object from which to extract the direction.

		#### Returns:
		`Vector`: A Vector representing the direction of the line.

		#### Example usage:
		```python
		line = Line(start=Point(0, 0, 0), end=Point(1, 1, 1))
		direction_vector = Vector.by_line(line)
		# Vector(X = 1, Y = 1, Z = 1)
		```
		"""
		return Vector(line_1.dx, line_1.dy, line_1.dz)

	@staticmethod
	def pitch(vector_1: 'Vector', angle: float) -> 'Vector':
		"""Rotates a vector around the X-axis (pitch).
		This method rotates the vector around the X-axis (pitch) by the specified angle.

		#### Parameters:
		- `vector_1` (`Vector`): The vector to be rotated.
		- `angle` (float): The angle of rotation in radians.

		#### Returns:
		`Vector`: A new Vector object representing the rotated vector.

		#### Example usage:
		```python
		vector1 = Vector(1, 2, 3)
		rotated_vector = Vector.pitch(vector1, math.pi/2)
		# Vector(X = 1.000, Y = -3.000, Z = 2.000)
		```
		"""
		return Vector(
			vector_1.x,
			vector_1.y*math.cos(angle) - vector_1.z*math.sin(angle),
			vector_1.y*math.sin(angle) + vector_1.z*math.cos(angle)
		)

	@staticmethod
	def value(vector_1: 'Vector') -> tuple:
		"""Returns the rounded values of the vector's components.

		#### Parameters:
		- `vector_1` (`Vector`): The vector.

		#### Returns:
		`tuple`: A tuple containing the rounded values of the vector's components.

		#### Example usage:
		```python
		vector1 = Vector(1.123456, 2.345678, 3.987654)
		rounded_values = Vector.value(vector1)
		# (1.1235, 2.3457, 3.9877)
		```
		"""
		roundValue = 4
		return (round(vector_1.x, roundValue), round(vector_1.y, roundValue), round(vector_1.z, roundValue))

	@staticmethod
	def reverse(vector_1: 'Vector') -> 'Vector':
		"""Returns the reverse (negation) of the vector.

		#### Parameters:
		- `vector_1` (`Vector`): The vector.

		#### Returns:
		`Vector`: The reverse (negation) of the input vector.

		#### Example usage:
		```python
		vector1 = Vector(1, 2, 3)
		reversed_vector = Vector.reverse(vector1)
		# Vector(X = -1, Y = -2, Z = -3)
		```
		"""
		return Vector(
			vector_1.x*-1,
			vector_1.y*-1,
			vector_1.z*-1
		)

	@staticmethod
	def rotate_XY(vector: 'Vector', Beta: float) -> 'Vector':
		"""Rotates the vector in the XY plane by the specified angle.

		#### Parameters:
		- `vector` (`Vector`): The vector to be rotated.
		- `Beta` (float): The angle of rotation in radians.

		#### Returns:
		`Vector`: A new Vector object representing the rotated vector.

		#### Example usage:
		```python
		vector = Vector(1, 0, 0)
		rotated_vector = Vector.rotate_XY(vector, math.pi/2)
		# Vector(X = 0, Y = 1, Z = 0)
		```
		"""
		return Vector(
			math.cos(Beta)*vector.x - math.sin(Beta)*vector.y,
			math.sin(Beta)*vector.x + math.cos(Beta)*vector.y,
			vector.z
		)