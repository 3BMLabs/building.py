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


"""This module provides tools for the modelling of level components."""

__title__ = "panel"
__author__ = "Maarten & Jonathan"
__url__ = "./objects/panel.py"

from abstract.vector import Point, Vector
from geometry.plane import Plane





# [!not included in BP singlefile - end]

class Level:
	def __init__(self):
		
		self.name = None
		self.polycurve = None
		self.plane = None
		self.parms = None
		self.elevation = None

	@classmethod
	def by_point(self, point=Point, name=str):
		if isinstance(point, Point):
			Lvl = Level()
			XY_plane = [Vector(x=1, y=0, z=0), Vector(x=0, y=1, z=0)]
			Lvl.plane = Plane.by_two_vectors_origin(
				XY_plane[0], XY_plane[1], point)
			Lvl.polycurve = Rect_XY(Point.to_vector(point), 1000, 1000)
			Lvl.elevation = point.z
			if name != None:
				Lvl.name = name
			return Lvl
		elif isinstance(point, Point):
			pass  # 0

	def __str__(self) -> str:
		return f"{self.type}(Name={self.name}, Elevation={self.elevation})"
