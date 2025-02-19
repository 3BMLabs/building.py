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


"""This module provides tools to create solids
"""

__title__ = "solid"
__author__ = "Maarten & Jonathan"
__url__ = "./geometry/solid.py"


import sys
from pathlib import Path
from typing import Self





from abstract.matrix import Matrix
from abstract.segmentation import Meshable, TesselationSettings
from geometry.mesh import Mesh
from geometry.plane import Plane
from geometry.rect import Rect
from abstract.vector import Vector
from geometry.curve import PolyCurve
from abstract.vector import Point
from abstract.vector import Vector


# [!not included in BP singlefile - end]


class Extrusion(Meshable):
	# Extrude a 2D polycurve to a 3D mesh or solid
	"""The Extrusion class represents the process of extruding a 2D polycurve into a 3D mesh or solid form. It is designed to handle geometric transformations and properties related to the extrusion process."""
	def __init__(self, polycurve: PolyCurve, extrusion_vector: Vector):
		"""The Extrusion class extrudes a 3d polycurve into a 3D mesh or solid form.
  
		all the extrusion class does, is save a polycurve and an extrusion vector.
  		the polycurve will be translated by the extrusion vector to get the 'top' face, the existing polycurve is the 'bottom' face.
  
		- `bottom_curve` (PolyCurve): the 3d polycurve defining the bottom face
		- `extrusion_vector` (Vector): we'll translate bottom_curve by this vector to get the top curve.
		"""

		self.bottom_curve = PolyCurve(polycurve)
		"""the 3d polycurve defining the bottom face"""
		self.extrusion_vector = Vector(extrusion_vector)
		"""we'll translate bottom_curve by this vector to get the top curve."""

	@staticmethod
	def by_2d_polycurve_height_vector(polycurve: PolyCurve, start_point: Point, extrusion_vector: Vector) -> 'Extrusion':
		"""Creates an extrusion from a 2D polycurve along a specified vector.
		This method extrudes a 2D polycurve into a 3D form by translating it to a specified start point and direction. The extrusion is created perpendicular to the polycurve's plane, extending it to the specified height.

		#### Parameters:
		- `polycurve_2d` (PolyCurve): The 2D polycurve to be extruded.
		- `height` (float): The height of the extrusion.
		- `cs_old` (CoordinateSystem): The original coordinate system of the polycurve.
		- `start_point` (Point): The start point for the extrusion in the new coordinate system.
		- `direction_vector` (Vector): The direction vector along which the polycurve is extruded.

		#### Returns:
		`Extrusion`: An Extrusion object representing the 3D form of the extruded polycurve.

		#### Example usage:
		```python
		extrusion = Extrusion.by_2d_polycurve_height_vector(polycurve_2d, 10, oldCS, startPoint, directionVec)
		```
		"""
		direction = extrusion_vector.normalized
		
		#since we don't have an up vector, we will need to determine how to rotate this extrusion ourselves. we assume that y must be up.
		if direction == Vector.z_axis:
			transform = Matrix.translate(start_point)
		else:
			#new x = horizontal (xy)
			x_vector = Vector.cross_product(direction, Vector.Z_Axis).normalized
			#new y = more vertical (contains at least a little bit of z)
			y_vector = Vector.cross_product(direction, x_vector)
			transform = Matrix.by_origin_unit_axes(start_point,[x_vector,y_vector, direction])
		return Extrusion(transform * PolyCurve(polycurve), extrusion_vector)

	@staticmethod
	def by_polycurve_height(polycurve: PolyCurve, height: float, dz_loc: float) -> 'Extrusion':
		"""Creates an extrusion from a PolyCurve with a specified height and base elevation.
		This method generates a vertical extrusion of a given PolyCurve. The PolyCurve is first translated vertically by `dz_loc`, then extruded to the specified `height`, creating a solid form.
		assumes the polycurve is wound counterclockwise

		#### Parameters:
		- `polycurve` (PolyCurve): The PolyCurve to be extruded. expected to be flat!
		- `height` (float): The height of the extrusion.
		- `dz_loc` (float): The base elevation offset from the original plane of the PolyCurve.

		#### Returns:
		`Extrusion`: An Extrusion object that represents the 3D extruded form of the input PolyCurve.

		#### Example usage:
		```python
		extrusion = Extrusion.by_polycurve_height(polycurve, 5, 0)
		```
		"""
		
		return Extrusion(polycurve, Vector.cross_product((polycurve[1].end - polycurve[0].start).normalized, (polycurve[-1].end - polycurve[0].start).normalized))
	
	@staticmethod
	def from_3d_rect(rect:Rect) -> Self:
		"""Generates an extrusion representing a cuboid from the 3D bounding box dimensions.

		#### Returns:
		`Extrusion`: An Extrusion object that represents a cuboid, matching the dimensions and orientation of the bounding box.

		#### Example usage:
		```python
		bbox2d = Rect().by_dimensions(length=100, width=50)
		cs = CoordinateSystem()
		bbox3d = BoundingBox3d().convert_boundingbox_2d(bbox2d, cs, height=30)
		cuboid = bbox3d.to_cuboid()
		# Generates a cuboid extrusion based on the 3D bounding box
		```
		"""
		return Extrusion(Matrix.translate(Vector(0, 0, rect.p0.z)) * PolyCurve.by_points(rect.corners(2)), Vector(0,0, rect.size.z))
	
	def to_mesh(self, settings: TesselationSettings) -> Mesh:
		mesh = Mesh()
		
		segmentated_polygon = self.bottom_curve.segmentate(settings)
		point_count = len(segmentated_polygon)

		# bottom face (face winding is reversed, but vertice winding isn't)
		for point in segmentated_polygon:
			mesh.vertices.append(point)
		
		mesh.faces.append(list(reversed(range(point_count))))
  
		# top face
		mesh.faces.append(list(range(point_count, point_count * 2)))
		for point_index in range(point_count):
			mesh.vertices.append(segmentated_polygon[point_index] + self.extrusion_vector)
			
		# when the height of an extrusion is 0, we only have to add the top / bottom (it doesn't really matter) side mesh. it would just cause z-buffer glitching
		if self.extrusion_vector.length_squared > 0:
			#other faces

			# Sides
			length = len(mesh.faces[0])
			for current_indice in range(length):
				next_indice = (current_indice + 1) % length
				face = [
        			current_indice, next_indice, #bottom
            		next_indice + length, current_indice + length #top
               	]
				mesh.faces.append(face)
		mesh.set_solid_color(settings.fallback_color)