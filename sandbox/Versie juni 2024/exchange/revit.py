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


"""This module provides tools for exporting geometry to Speckle
"""

__title__ = "revit"
__author__ = "Maarten & Jonathan"
__url__ = "./exchange/revit.py"


import sys
from pathlib import Path
# import specklepy

sys.path.append(str(Path(__file__).resolve().parents[1]))

from geometry.point import Point
from geometry.curve import Line
from objects.frame import *
from exchange.scia import *

# [!not included in BP singlefile - end]

#class CurveElement:
#class PointElement (non visible) or visible as a big cube

class StructuralElement:
    def __init__(self, structuralType: str, startPoint: list, endPoint: list, type: str, rotation: float, yJustification: int, yOffsetValue: float, zJustification: int, zOffsetValue: float, comments : None):
        validStructuralTypes = ["Column", "Beam"]
        if structuralType not in validStructuralTypes:
            raise ValueError(f"Invalid structuralType: {structuralType}. Valid options are: {validStructuralTypes}")
        self.comments = comments or None
        self.structuralType = structuralType
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.type = type
        self.rotation = rotation
        self.yJustification = yJustification
        self.yOffsetValue = yOffsetValue
        self.zJustification = zJustification
        self.zOffsetValue = zOffsetValue

    def __str__(self) -> str:
        return f"[StructuralElement] {self.type}"


def mm_to_feet(mm_value):
    feet_value = mm_value * 0.00328084
    return feet_value

objs = []
def run():
    project = BuildingPy("TempCommit", "0")
    try:
        LoadXML(IN[0], project)
    except:
        pass

    for obj in project.objects:
        
        if obj.type == "Frame":
            if obj.profile_data.shape_name == "LAngle":
                obj.rotation = obj.rotation+180
            
            #Revit problem solved (Please enter a value between -360 and 360)
            if obj.rotation < -360:
                obj.rotation = obj.rotation + 360
            elif obj.rotation > 360:
                obj.rotation = obj.rotation - 360
            element = StructuralElement("Beam", obj.start, obj.end, obj.name, obj.rotation, obj.YJustification, obj.YOffset, obj.ZJustification, obj.ZOffset, obj.comments)
            objs.append(element)
        elif obj.type == "Node":
            objs.append(obj)
    return project.objects

run()

OUT = objs