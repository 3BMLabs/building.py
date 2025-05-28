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


"""Derive from this class to use serialization functions!
"""

__title__ = "segmentation"
__author__ = "JohnHeikens"
__url__ = "./abstract/segmentation.py"
from abc import abstractmethod
import math

from geometry.mesh import Mesh

# [!not included in BP singlefile - end]

class SegmentationSettings:
	def __init__(self, max_angle: float =  math.pi / 4):
		self.max_angle = max_angle
		"""the maximum angle to keep a straight line"""

class TesselationSettings(SegmentationSettings):
	def __init__(self, max_angle = math.pi / 4, fallback_color = 0xffffffff):
		super().__init__(max_angle)
		self.fallback_color = fallback_color

class Meshable:
	"""A Meshable is a class convertable to mesh.
	"""
	@abstractmethod
	def to_mesh(self, settings: TesselationSettings) -> Mesh:
		pass