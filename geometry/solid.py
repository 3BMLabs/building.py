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





from abstract.segmentation import Meshable, SegmentationSettings
from geometry.mesh import Mesh
from geometry.plane import Plane
from geometry.rect import Rect
from abstract.vector import Vector
from geometry.curve import PolyCurve
from geometry.point import Point


# [!not included in BP singlefile - end]


class Extrusion(Meshable):
	# Extrude a 2D polycurve to a 3D mesh or solid
	"""The Extrusion class represents the process of extruding a 2D polycurve into a 3D mesh or solid form. It is designed to handle geometric transformations and properties related to the extrusion process."""
	def __init__(self, polycurve: PolyCurve, start: Vector, end: Vector):
		"""The Extrusion class represents the process of extruding a 2D polycurve into a 3D mesh or solid form. It is designed to handle geometric transformations and properties related to the extrusion process.
		
		- `id` (str): A unique identifier for the extrusion instance.
		- `type` (str): Class name, indicating the object type as "Extrusion".
		- `parameters` (list): A list of parameters associated with the extrusion.
		- `verts` (list): A list of vertices that define the shape of the extruded mesh.
		- `faces` (list): A list of faces, each defined by indices into the `verts` list.
		- `numberFaces` (int): The total number of faces in the extrusion.
		- `countVertsFaces` (int): The total number of vertices per face, distinct from the total vertex count.
		- `name` (str): The name assigned to the extrusion instance.
		- `color` (tuple): The color of the extrusion, defined as an RGB tuple.
		- `colorlst` (list): A list of colors applied to the extrusion, potentially varying per face or vertex.
		- `topface` (PolyCurve): The top face of the extrusion, returned as a polycurve converted to a surface.
		- `bottomface` (PolyCurve): The bottom face of the extrusion, similar to `topface`.
		- `polycurve_3d_translated` (PolyCurve): A polycurve representing the translated 3D polycurve of the extrusion.
		- `bottomshape` (list): A list representing the shape of the bottom face of the extrusion.
		"""
		
		self.polycurve = polycurve
		self.start = start
		self.end = end

	def set_parameter(self, data: list) -> 'Extrusion':
		"""Sets parameters for the extrusion.
		This method allows for the modification of the Extrusion's parameters, which can influence the extrusion process or define additional properties.

		#### Parameters:
		- `data` (list): A list of parameters to be applied to the extrusion.

		#### Returns:
		`Extrusion`: The Extrusion instance with updated parameters.
	
		#### Example usage:
		```python

		```
		"""
		self.parameters = data
		return self
		
	@staticmethod
	def by_polycurve_height_vector(polycurve: PolyCurve, height: float, start_point: Point, direction_vector: Vector) -> 'Extrusion':
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
		extrusion = Extrusion.by_polycurve_height_vector(polycurve_2d, 10, oldCS, startPoint, directionVec)
		```
		"""
		return Extrusion(polycurve, start_point, start_point + direction_vector * height)

	@staticmethod
	def by_polycurve_height(polycurve: PolyCurve, height: float, dz_loc: float) -> 'Extrusion':
		"""Creates an extrusion from a PolyCurve with a specified height and base elevation.
		This method generates a vertical extrusion of a given PolyCurve. The PolyCurve is first translated vertically by `dz_loc`, then extruded to the specified `height`, creating a solid form.

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
		# global len
		Extrus = Extrusion()
		Points = polycurve.points
		V1 = Vector.by_two_points(Points[0], Points[1])
		V2 = Vector.by_two_points(Points[-2], Points[-1])

		p1 = Plane.by_two_vectors_origin(
			V1, V2, Points[0])  # Workplane of PolyCurve
		norm = p1.Normal

		pnts = []
		faces = []

		Extrus.polycurve_3d_translated = polycurve

		numPoints = len(Points)
		

		return Extrus
	
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
		return Extrusion(PolyCurve.by_points(rect.corners(2)), Vector(0,0,rect.p0.z), Vector(0,0,rect.p0.z + rect.size.z))
	
	def to_mesh(self, settings: SegmentationSettings) -> Mesh:
		
  
		# allverts
		for pnt in self.polycurve.segmentate(settings):
			# bottom side moves along the normal with dz_loc units
			pnt.append(Point.translate(pnt, norm * dz_loc))
		
		# Bottomface
		face = []
		for x in reversed(range(numPoints)):
			face.append(x)
		faces.append(face)
		
		
		# Topface
		# TODO: correct winding
		face = []
		start = numPoints if height else 0
		for x in range(start, start + numPoints):
			face.append(x)
		faces.append(face)
			
		# when the height of an extrusion is 0, we only have to add the top / bottom (it doesn't really matter) side mesh. it would just cause z-buffer glitching
		if height:
			for pnt in Points:
				# Bovenzijde verplaatst met dz_loc
				pnts.append(Point.translate(
					pnt, norm * (dz_loc+height)))
			#other faces



			# Sides
			count = 0
			length = len(faces[0])
			for i, j in zip(faces[0], faces[1]):
				face = []
				face.append(i)
				face.append(faces[0][count + 1])
				face.append(faces[1][count + 1])
				face.append(j)
				count = count + 1
				if count == length-1:
					face.append(i)
					face.append(faces[0][0])
					face.append(faces[1][0])
					face.append(j)
					faces.append(face)
					break
				else:
					pass
				faces.append(face)

		# toMeshStructure
		for i in pnts:
			Extrus.verts.append(i.x)
			Extrus.verts.append(i.y)
			Extrus.verts.append(i.z)
			
		# faces are laid out like this: face 0 vert count, face 0 vert 0 index, vert ...count index, face 1 vert count etc.
		# for example: 4, 0, 1, 2, 3, 3, 4, 5, 6 => 4, (0, 1, 2, 3), 3, (4, 5, 6)
		for x in faces:
			Extrus.faces.append(len(x))  # Number of verts in face
			for y in x:
				Extrus.faces.append(y)

		Extrus.numberFaces = len(faces)
		Extrus.countVertsFaces = (4 * len(faces))

		for j in range(int(len(Extrus.verts) / 3)):
			Extrus.colorlst.append(Extrus.color)