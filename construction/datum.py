# [included in BP singlefile]
# [!not included in BP singlefile - start]
# -*- coding: utf8 -*-
# ***************************************************************************
# *   Copyright (c) 2024 Maarten Vroegindeweij & Jonathan van der Gouwe	  *
# *   maarten@3bm.co.nl & jonathan@3bm.co.nl								*
# *																		 *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)	*
# *   as published by the Free Software Foundation; either version 2 of	 *
# *   the License, or (at your option) any later version.				   *
# *   for detail see the LICENCE text file.								 *
# *																		 *
# *   This program is distributed in the hope that it will be useful,	   *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of		*
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the		 *
# *   GNU Library General Public License for more details.				  *
# *																		 *
# *   You should have received a copy of the GNU Library General Public	 *
# *   License along with this program; if not, write to the Free Software   *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA																   *
# *																		 *
# ***************************************************************************


"""This module provides tools grids, levels and other datums
"""

__title__ = "datum"
__author__ = "Maarten & Jonathan"
__url__ = "./objects/datum.py"

from abstract.matrix import Matrix, CoordinateSystem
from abstract.serializable import Serializable
from abstract.text import *
from geometry.curve import Arc




# [!not included in BP singlefile - end]
seqChar = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z AA AB AC"
seqNumber = "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24"


class GridheadType(Serializable):
	def __init__(self):
		
		self.name = None
		self.curves = []
		self.diameter = 150
		self.text_height = 200
		self.radius = self.diameter/2
		self.font_family = "calibri"

	def by_diam(self, name, diameter: float, font_family, text_height):
		self.name = name
		self.diameter = diameter
		self.radius = self.diameter / 2
		self.font_family = font_family
		self.text_height = text_height
		self.geom()
		return self

	def geom(self):
		radius = self.radius
		self.curves.append(Arc.by_start_mid_end(Point(-radius, radius, 0),
						   Point(0, radius*2, 0), Point(radius, radius, 0)))
		self.curves.append(Arc.by_start_mid_end(Point(-radius, radius, 0),
						   Point(0, 0, 0), Point(radius, radius, 0)))
		# origin is at center of circle

GHT30 = GridheadType().by_diam("2.5 mm", 400, "calibri", 200)

GHT50 = GridheadType().by_diam("GHT50", 600, "calibri", 350)


class GridHead:
	def __init__(self):
		
		self.grid_name: str = "A"
		self.grid_head_type = GHT50
		self.radius = GHT50.radius
		self.CS: CoordinateSystem = Matrix()
		self.x: float = 0.5
		self.y: float = 0
		self.text_curves = []
		self.curves = []
		self.__textobject()
		self.__geom()

	def __geom(self):
		# CStot = CoordinateSystem.translate(self.CS,Vector(0,self.grid_head_type.radius,0))
		for i in self.grid_head_type.curves:
			self.curves.append(transform_arc(i, (self.CS)))

	def __textobject(self):
		cs_text = self.CS
		# to change after center text function is implemented
		cs_text_new = CoordinateSystem.move_local(cs_text, -100, 40, 0)
		self.text_curves = Text(text=self.grid_name, font_family=self.grid_head_type.font_family,
								height=self.grid_head_type.text_height, cs=cs_text_new).write()

	@staticmethod
	def by_name_gridheadtype_y(name, cs: CoordinateSystem, gridhead_type, y: float):
		GH = GridHead()
		GH.grid_name = name
		GH.grid_head_type = gridhead_type
		GH.CS = cs
		GH.x = 0.5
		GH.y = y
		GH.__textobject()
		GH.__geom()
		return GH

	def write(self, project):
		for x in self.text_curves:
			project.objects.append(x)
		for y in self.curves:
			project.objects.append(y)


class Grid:
	def __init__(self):
		self.line = None
		self.start = None
		self.end = None
		self.direction: Vector = Vector(0, 1, 0)
		self.grid_head_type = GHT50
		self.name = None
		self.bulbStart = False
		self.bulbEnd = True
		self.cs_end: CoordinateSystem = CoordinateSystem() #Maarten
		self.grid_heads = []

	def __cs(self, line):
		self.direction = line.vector_normalised
		vect3 = Vector.rotate_XY(self.direction, math.radians(-90))
		self.cs_end = CoordinateSystem(line.end, vect3, self.direction, Z_Axis)

	@classmethod
	def by_startpoint_endpoint(cls, line, name):
		# Create panel by polycurve
		g1 = Grid()
		g1.start = line.start
		g1.end = line.start
		g1.name = name
		g1.__cs(line)
		g1.line = line_to_pattern(line, Centerline)
		# g1.__grid_heads()
		return g1

	def __grid_heads(self):
		if self.bulbEnd == True:
			self.grid_heads.append(
				GridHead.by_name_gridheadtype_y(self.name, self.cs_end, self.grid_head_type, 0))

	def write(self, project):
		for x in self.line:
			project.objects.append(x)
		for y in self.grid_heads:
			y.write(project)
		return self


def get_grid_distances(Grids):
	# Function to create grids from the format 0, 4x5400, 4000, 4000 to absolute XYZ-values
	GridsNew = []
	GridsNew.append(0)
	distance = 0.0
	# GridsNew.append(distance)
	for i in Grids:
		# del Grids[0]
		if "x" in i:
			spl = i.split("x")
			count = int(spl[0])
			width = float(spl[1])
			for i in range(count):
				distance = distance + width
				GridsNew.append(distance)
		else:
			distance = distance + float(i)
			GridsNew.append(distance)
	return GridsNew


class GridSystem:
	# rectangle Gridsystem
	def __init__(self):
		
		self.gridsX = None
		self.gridsY = None
		self.dimensions = []
		self.name = None

	@classmethod
	def by_spacing_labels(cls, spacingX, labelsX, spacingY, labelsY, gridExtension):
		gs = GridSystem()
		# Create gridsystem
		# spacingXformat = "0 3000 3000 3000"
		GridEx = gridExtension

		GridsX = spacingX.split()
		GridsX = get_grid_distances(GridsX)
		Xmax = max(GridsX)
		GridsXLable = labelsX.split()
		GridsY = spacingY.split()
		GridsY = get_grid_distances(GridsY)
		Ymax = max(GridsY)
		GridsYLable = labelsY.split()

		gridsX = []
		dimensions = []
		count = 0
		ymaxdim1 = Ymax+GridEx-300
		ymaxdim2 = Ymax+GridEx-0
		xmaxdim1 = Xmax+GridEx-300
		xmaxdim2 = Xmax+GridEx-0
		for i in GridsX:
			gridsX.append(Grid.by_startpoint_endpoint(
				Line(Point(i, -GridEx, 0), Point(i, Ymax+GridEx, 0)), GridsXLable[count]))
			try:
				dim = Dimension(Point(i, ymaxdim1, 0), Point(
					GridsX[count+1], ymaxdim1, 0), DT2_5_mm)
				gs.dimensions.append(dim)
			except:
				pass
			count = count + 1

		# Totaal maatvoering 1
		dim = Dimension(Point(GridsX[0], ymaxdim2, 0), Point(
			Xmax, ymaxdim2, 0), DT2_5_mm)
		gs.dimensions.append(dim)

		# Totaal maatvoering 2
		dim = Dimension(Point(xmaxdim2, GridsY[0], 0), Point(
			xmaxdim2, Ymax, 0), DT2_5_mm)
		gs.dimensions.append(dim)

		gridsY = []
		count = 0
		for i in GridsY:
			gridsY.append(Grid.by_startpoint_endpoint(
				Line(Point(-GridEx, i, 0), Point(Xmax+GridEx, i, 0)), GridsYLable[count]))
			try:
				dim = Dimension(Point(xmaxdim1, i, 0), Point(
					xmaxdim1, GridsY[count+1], 0))  # ,DT3_5_mm)
				gs.dimensions.append(dim)
			except:
				pass
			count = count + 1
		gs.gridsX = gridsX
		gs.gridsY = gridsY
		return gs

	def write(self, project):
		for x in self.gridsX:
			project.objects.append(x)
			for i in x.grid_heads:
				i.write(project)
		for y in self.gridsY:
			project.objects.append(y)
			for j in y.grid_heads:
				j.write(project)
		for z in self.dimensions:
			z.write(project)
		return self
