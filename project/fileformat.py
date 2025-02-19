# [included in BP singlefile]
# [!not included in BP singlefile - start]
# -*- coding: utf8 -*-
# ***************************************************************************
# *   Copyright (c) 2024 Maarten Vroegindeweij & Jonathan van der Gouwe		*
# *   maarten@3bm.co.nl & jonathan@3bm.co.nl								*
# *																		 	*
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)	*
# *   as published by the Free Software Foundation; either version 2 of	 	*
# *   the License, or (at your option) any later version.				   	*
# *   for detail see the LICENCE text file.								 	*
# *																		 	*
# *   This program is distributed in the hope that it will be useful,	   	*
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of		*
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the		 	*
# *   GNU Library General Public License for more details.				  	*
# *																		 	*
# *   You should have received a copy of the GNU Library General Public	 	*
# *   License along with this program; if not, write to the Free Software   *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA																   	*
# *																		 	*
# ***************************************************************************


"""This module provides the fileformat class
"""

__title__= "fileformat"
__author__ = "Maarten & Jonathan"
__url__ = "./fileformat/fileformat.py"


import sys
from collections import defaultdict

from abstract.serializable import Serializable
from abstract.vector import Point


# [!not included in BP singlefile - end]
class BuildingPy(Serializable):
	def __init__(self, name=None, number=None):
		self.name: str = name
		self.number: str = number
		#settings
		self.debug: bool = True
		self.objects = []
		self.units = "mm"
		self.decimals = 3 #not fully implemented yet

		self.origin = Point(0,0,0)
		self.default_font = "calibri"
		self.scale = 1000
		self.font_height = 500
		self.repr_round = 3
		#prefix objects (name)
		#Geometry settings

		#export selection info
		self.domain = None
		self.applicationId = "OPEN-AEC BuildingPy"

		#different settings for company's?

		#rename this to autoclose?
		self.closed: bool = True #auto close polygons? By default true, else overwrite
		self.round: bool = False #If True then arcs will be segmented. Can be used in Speckle.

		#functie polycurve of iets van een class/def
		self.autoclose: bool = True #new self.closed

		#nodes
		self.node_merge = True #False not yet created
		self.node_diameter = 250
		self.node_threshold = 50
		
		#text
		self.createdTxt = "has been created"

		#Speckle settings
		self.speckleserver = "app.speckle.systems"
		self.specklestream = None

		#FreeCAD settings
		
	def save(self, file_name = 'project/data.json'):
		Serializable.save(file_name)
		
		type_count = defaultdict(int)
		for serialized_item in self.objects:
			#item = json.loads(serialized_item)
			type_count[serialized_item.__class__.__name__] += 1

		total_items = len(self.objects)

		print(f"\nTotal saved items to '{file_name}': {total_items}")
		print("Type counts:")
		for item_type, count in type_count.items():
			print(f"{item_type}: {count}")
	def open(self, file_name = 'project/data.json'):
		Serializable.open(file_name)

	def to_speckle(self, streamid, commitstring=None):
		from exchange.speckle import translateObjectsToSpeckleObjects, TransportToSpeckle
		self.specklestream = streamid
		speckleobj = translateObjectsToSpeckleObjects(self.objects)
		TransportToSpeckle(self.speckleserver, streamid, speckleobj, commitstring)

	def to_FreeCAD(self):
		from exchange.Freecad_Bupy import translateObjectsToFreeCAD
		translateObjectsToFreeCAD(self.objects)

	def to_IFC(self, name):
		from exchange.IFC import translateObjectsToIFC, CreateIFC
		ifc_project = CreateIFC()
		ifc_project.add_project(name)
		ifc_project.add_site("My Site")
		ifc_project.add_building("Building A")
		ifc_project.add_storey("Ground Floor")
		ifc_project.add_storey("G2Floor")	 
		translateObjectsToIFC(self.objects, ifc_project)
		ifc_project.export(f"{name}.ifc")
# [!not included in BP singlefile - end]

#god object! multiple instances of buildingpy should be able to live next to eachother
#project = BuildingPy("Project", "0")
