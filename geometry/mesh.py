# -*- coding: utf8 -*-
#***************************************************************************
#*   Copyright (c) 2023 Maarten Vroegindeweij & Jonathan van der Gouwe      *
#*   maarten@3bm.co.nl & jonathan@3bm.co.nl                                *
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


"""This module provides tools to create meshes
"""

__title__= "mesh"
__author__ = "Maarten & Jonathan"
__url__ = "./geometry/mesh.py"


import sys, os, math
from pathlib import Path

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

from geometry.point import *
from packages import helper

class Mesh:
    def __init__(self, id=helper.generateID()) -> None:
        pass
    pass

    def __id__(self):
        return f"id:{self.id}"

    def __str__(self) -> str:
        return f"{__class__.__name__}({self})"

class Extrusion:
    #Extrude a 2D profile to a 3D mesh
    def __init__(self):
        self.verts = []
        self.faces = []
        self.name = "none"

    def byPolyCurveHeight(self, polycurve2D, height):
        count = 0
        for i in polycurve2D:
            self.faces.append(4)
            self.verts.append(i.start.x)
            self.verts.append(i.start.y)
            self.verts.append(0)
            self.faces.append(count)
            count += 1
            self.verts.append(i.end.x)
            self.verts.append(i.end.y)
            self.verts.append(0)
            self.faces.append(count)
            count += 1
            self.verts.append(i.end.x)
            self.verts.append(i.end.y)
            self.verts.append(height)
            self.faces.append(count)
            count += 1
            self.verts.append(i.start.x)
            self.verts.append(i.start.y)
            self.verts.append(height)
            self.faces.append(count)
            count += 1
            #    vert = [0, 0, 0, 1000, 0, 0, 1000, 2000, 0, 0, 1000, 0, 0, 2000, 2000, 3000, 2000, 1000]
            # list structure of verts is x y z x y z x y z
            #    faces = [3, 0, 1, 2, 3, 2, 3, 5]
            # list structure of faces is [number of verts], vert.index, vert.index, vert.index, vert2.index. enz.
            # first number is number of vertices.
            # then

    #def byPoints(self, points3d):

    def byVertsFaces(self, verts, faces):
        self.verts = verts
        self.faces = faces