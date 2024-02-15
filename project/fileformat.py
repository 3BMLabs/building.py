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


"""This module provides the fileformat class
"""

__title__= "fileformat"
__author__ = "Maarten & Jonathan"
__url__ = "./fileformat/fileformat.py"


import sys, os, math, json
from collections import defaultdict
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from geometry.point import Point
from abstract.coordinatesystem import CoordinateSystem
from abstract.vector import Vector3

# [!not included in BP singlefile - end]
class BuildingPy:
    def __init__(self, name=None, number=None):
        self.name: str = name
        self.number: str = number
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
        self.applicationId = "OPEN-AEC | BuildingPy"

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

        #structural elements
        self.structural_fallback_element = "HEA100"

        #Speckle settings
        self.speckleserver = "speckle.xyz"
        self.specklestream = None

        #FreeCAD settings

        XAxis = Vector3(1, 0, 0)
        YAxis = Vector3(0, 1, 0)
        ZAxis = Vector3(0, 0, 1)
        self.CSGlobal = CoordinateSystem(Point(0, 0, 0), XAxis, YAxis, ZAxis)
        
    def save(self):
        # print(self.objects)
        serialized_objects = []
        for obj in self.objects:
            try:
                # print(obj)
                serialized_objects.append(json.dumps(obj.serialize()))
            except:
                print(obj)

        serialized_data = json.dumps(serialized_objects)
        file_name = 'project/data.json'
        with open(file_name, 'w') as file:
            file.write(serialized_data)


        type_count = defaultdict(int)
        for serialized_item in serialized_objects:
            item = json.loads(serialized_item)
            item_type = item.get("type")
            if item_type:
                type_count[item_type] += 1

        total_items = len(serialized_objects)

        print(f"\nTotal saved items to '{file_name}': {total_items}")
        print("Type counts:")
        for item_type, count in type_count.items():
            print(f"{item_type}: {count}")


    def open(self):
        pass #open data.json objects in here

    def toSpeckle(self, streamid, commitstring=None):
        from exchange.speckle import translateObjectsToSpeckleObjects, TransportToSpeckle
        self.specklestream = streamid
        speckleobj = translateObjectsToSpeckleObjects(self.objects)
        TransportToSpeckle(self.speckleserver,streamid,speckleobj,commitstring)

    def toFreeCAD(self):
        from exchange.freecad_bupy import translateObjectsToFreeCAD
        translateObjectsToFreeCAD(self.objects)

    def toIFC(self):
        from exchange.IFC import translateObjectsToIFC
        translateObjectsToIFC(self.objects)

# [!not included in BP singlefile - end]

project = BuildingPy("Project","0")