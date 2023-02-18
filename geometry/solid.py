# -*- coding: utf8 -*-
#***************************************************************************
#*   Copyright (c) 2023 Jonathan Van der Gouwe & Maarten Vroegindeweij     *
#*   jonathan@3bm.co.nl & maarten@3bm.co.nl                                *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   This program is distributed in the hope that it will be useful,       *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Library General Public License for more details.                  *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************


"""This module provides tools to create solids
"""

__title__= "solid"
__author__ = "Maarten & Jonathan"
__url__ = "./geometry/solid.py"



import math, os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) #path: PyBuildingSystems
from geometry.point import *
from packages import helper

class Extrusion:
    #Extrude a 2D profile to a 3D mesh
    def __init__(self):
        self.verts = []
        self.faces = []
        self.numberFaces = 0
        self.name = "none"

    def byPolyCurveHeightVector(self, polycurve, height, CSOld, startpoint, DirectionVector: Vector3):
        count = 0
        for i in polycurve:
            startpointLow = transformPoint(Point(i.start.x,i.start.y,0), CSOld, startpoint, DirectionVector)
            endpointLow = transformPoint(Point(i.end.x,i.end.y,0), CSOld, startpoint, DirectionVector)
            endpointHigh = transformPoint(Point(i.end.x,i.end.y,height), CSOld, startpoint, DirectionVector)
            startpointHigh = transformPoint(Point(i.start.x,i.start.y,height), CSOld, startpoint, DirectionVector)

            #Construct faces perpendicular on polycurve
            self.faces.append(4)
            self.verts.append(startpointLow.x)
            self.verts.append(startpointLow.y)
            self.verts.append(startpointLow.z)
            self.faces.append(count)
            count += 1
            self.verts.append(endpointLow.x)
            self.verts.append(endpointLow.y)
            self.verts.append(endpointLow.z)
            self.faces.append(count)
            count += 1
            self.verts.append(endpointHigh.x)
            self.verts.append(endpointHigh.y)
            self.verts.append(endpointHigh.z)
            self.faces.append(count)
            count += 1
            self.verts.append(startpointHigh.x)
            self.verts.append(startpointHigh.y)
            self.verts.append(startpointHigh.z)
            self.faces.append(count)
            count += 1
            self.numberFaces = self.numberFaces + 1
            #    vert = [0, 0, 0, 1000, 0, 0, 1000, 2000, 0, 0, 1000, 0, 0, 2000, 2000, 3000, 2000, 1000]
            # list structure of verts is x y z x y z x y z
            #    faces = [3, 0, 1, 2, 3, 2, 3, 5]
            # list structure of faces is [number of verts], vert.index, vert.index, vert.index, vert2.index. enz.
            # first number is number of vertices.
            # then
        return self.verts, self.faces, self.numberFaces

class Sweep:
    def __init__(self, id=helper.generateID()) -> None:
        pass
        self.id = id
    pass

    def __id__(self):
        return f"id:{self.id}"

    def __str__(self) -> str:
        return f"{__class__.__name__}({self})"


class SweptBlend:
    def __init__(self, id=helper.generateID()) -> None:
        pass
        self.id = id
    pass

    def __id__(self):
        return f"id:{self.id}"

    def __str__(self) -> str:
        return f"{__class__.__name__}({self})"