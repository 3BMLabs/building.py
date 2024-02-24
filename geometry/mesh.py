# [included in BP singlefile]
# [!not included in BP singlefile - start]
# -*- coding: utf8 -*-
#***************************************************************************
#*   Copyright (c) 2024 Maarten Vroegindeweij                              *
#*   maarten@3bm.co.nl                                                     *
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

__title__= "mesh"
__author__ = "Maarten"
__url__ = "./geometry/solid.py"

class MeshPB:
    def __init__(self):
        self.type = __class__.__name__
        self.verts = []
        self.faces = []
        self.numberFaces = 0
        self.name = None
        self.material = None
        self.colorlst = []

    def byVertsFaces(self, verts, faces):
        self.verts = verts
        self.faces = faces

    def byPolyCurve(self, PC, name, material):
        #Mesh of single face
        verts = []
        faces = []
        # numberFaces = 0
        n = 0  # number of vert. Every vert has a unique number in the list
        pnts = PC.points  # points in every polycurve
        faces.append(len(pnts))  # number of verts in face
        for j in pnts:
            faces.append(n)
            verts.append(j.x)
            verts.append(j.y)
            verts.append(j.z)
            n = n + 1
        self.verts = verts
        self.faces = faces
        # ex.numberFaces = numberFaces
        self.name = name
        self.material = material
        self.colorlst = [material.colorint]
        return self