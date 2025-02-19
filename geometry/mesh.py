# [included in BP singlefile]
# [!not included in BP singlefile - start]
# -*- coding: utf8 -*-
# ***************************************************************************
# *   Copyright (c) 2024 Maarten Vroegindeweij                              *
# *   maarten@3bm.co.nl                                                     *
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

__title__ = "mesh"
__author__ = "Maarten"
__url__ = "./geometry/solid.py"


from abstract.serializable import Serializable
from library.material import Material


class Mesh(Serializable):
	"""Represents a mesh object with vertices, faces, and other attributes."""
	def __init__(self):
		"""The Mesh class is designed to construct mesh objects from vertices and faces. It supports creating meshes from a variety of inputs including vertex-face lists, polycurves, and coordinate lists with support for nested structures.
		
		- `verts` (list): A list of vertices that make up the mesh.
		- `faces` (list): A list defining the faces of the mesh. Each face is represented by indices into the `verts` list.
		- `face_count` (int): The number of faces in the mesh.
		- `name` (str): The name of the mesh.
		- `material` (Material): The material assigned to the mesh.
		- `colorlst` (list): A list of colors for the mesh, derived from the material.
		"""
		self.vertices = []
		
		#this nested list contains indices for every face. for example:
		#[[0, 1, 2], [3, 0, 4]] -> 2 faces. the first face connects the points 0, 1 and 2, while the second face connects the points 3, 0 and 4.
		self.faces: list[list] = []
		
		self.face_count = 0
		self.name = None
		self.material = None
		self.colors = []
	
	def set_solid_color(self, solid_color_int: int):
		self.colors = [solid_color_int for j in range(int(len(self.vertices) / 3))]

	def by_verts_faces(self, verts: 'list', faces: 'list') -> 'Mesh':
		"""Initializes the mesh with vertices and faces.

		#### Parameters:
		- `verts` (list): A list of vertices.
		- `faces` (list): A list of faces. Each face is a list of indices into the `verts` list.

		This method directly sets the vertices and faces of the mesh based on the input lists.
		
		#### Example usage:
		```python

		```
		"""
		self.vertices = verts
		self.faces = faces

	#create material class; Material
	def by_polycurve(self, PC:'PolyCurve', name: 'str', material:Material) -> 'Mesh':
		"""Creates a mesh from a polycurve object.

		#### Parameters:
		- `PC` (Polycurve): A polycurve object from which to generate the mesh.
		- `name` (str): The name of the mesh.
		- `material` (Material): The material to apply to the mesh.

		This method constructs the mesh such that it represents the shape defined by the polycurve.
		
		#### Example usage:
		```python

		```
		"""
		# Mesh of single face
		verts = []
		faces = []
		# numberFaces = 0
		n = 0  # number of vert. Every vert has a unique number in the list
		pnts = PC.points  # points in every polycurve
		
		current_face = []

		for j in pnts:
			current_face.append(n)
			verts.append(j.x)
			verts.append(j.y)
			verts.append(j.z)
			n = n + 1
		self.vertices = verts
		self.faces = [current_face]
		# ex.numberFaces = numberFaces
		self.name = name
		self.material = material
		self.colorlst = [material.colorint]
		return self

	def by_coords(self, lsts: 'list', name: 'str', material, doublenest: 'bool') -> 'Mesh':
		"""Creates a mesh from a list of coordinates.

		#### Parameters:
		- `lsts` (list): A nested list of coordinates defining the vertices of the mesh.
		- `name` (str): The name of the mesh.
		- `material` (Material): The material to apply to the mesh.
		- `doublenest` (bool): A flag indicating if the list of coordinates is double-nested.

		This method allows for flexible mesh creation from complex nested list structures of coordinates.
		
		#### Example usage:
		```python

		```
		"""
		# Example list structure, can be multiple as wel
		# [[[[8252, 2129, 1520], [-6735, 1188, 1520], [8753, -5855, 1520]]], [[[-6735, 1188, 1520], [-6234, -6796, 1520], [8753, -5855, 1520]]], [[[8252, 2129, 870], [8753, -5855, 1520], [8753, -5855, 870]]], [[[8252, 2129, 870], [8252, 2129, 1520], [8753, -5855, 1520]]], [[[8753, -5855, 870], [-6234, -6796, 1520], [-6234, -6796, 870]]], [[[8753, -5855, 870], [8753, -5855, 1520], [-6234, -6796, 1520]]], [[[-6234, -6796, 870], [-6735, 1188, 1520], [-6735, 1188, 870]]], [[[-6234, -6796, 870], [-6234, -6796, 1520], [-6735, 1188, 1520]]], [[[-6735, 1188, 870], [8252, 2129, 1520], [8252, 2129, 870]]], [[[-6735, 1188, 870], [-6735, 1188, 1520], [8252, 2129, 1520]]], [[[-6735, 1188, 870], [8252, 2129, 870], [8753, -5855, 870]]], [[[-6234, -6796, 870], [-6735, 1188, 870], [8753, -5855, 870]]]]
		verts = []
		faces = []
		count = 0
		# lst is [[8252, 2129, 1520], [-6735, 1188, 1520], [8753, -5855, 1520]]
		for lst in lsts:
			if doublenest:
				# lst is [8252, 2129, 1520], [-6735, 1188, 1520], [8753, -5855, 1520], [8753, -5855, 1520]
				lst = lst[0]
			else:
				lst = lst
			faces.append(len(lst))
			for coord in lst:  # [8252, 2129, 1520]
				faces.append(count)
				verts.append(coord[0])  # x
				verts.append(coord[1])  # y
				verts.append(coord[2])  # z
				count += 1
			self.face_count = + 1
		for j in range(int(len(verts) / 3)):
			self.colorlst.append(material.colorint)
		self.vertices = verts
		self.faces = faces
		self.name = name
		self.material = material
		return self
