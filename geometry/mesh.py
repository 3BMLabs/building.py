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

    def by_verts_faces(self, verts, faces):
        self.verts = verts
        self.faces = faces

    def by_polycurve(self, PC, name, material):
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

    def by_three_coords(self, lsts, name, material, doublenest: bool):
        #Example list structure
        #[[[[8252, 2129, 1520], [-6735, 1188, 1520], [8753, -5855, 1520]]], [[[-6735, 1188, 1520], [-6234, -6796, 1520], [8753, -5855, 1520]]], [[[8252, 2129, 870], [8753, -5855, 1520], [8753, -5855, 870]]], [[[8252, 2129, 870], [8252, 2129, 1520], [8753, -5855, 1520]]], [[[8753, -5855, 870], [-6234, -6796, 1520], [-6234, -6796, 870]]], [[[8753, -5855, 870], [8753, -5855, 1520], [-6234, -6796, 1520]]], [[[-6234, -6796, 870], [-6735, 1188, 1520], [-6735, 1188, 870]]], [[[-6234, -6796, 870], [-6234, -6796, 1520], [-6735, 1188, 1520]]], [[[-6735, 1188, 870], [8252, 2129, 1520], [8252, 2129, 870]]], [[[-6735, 1188, 870], [-6735, 1188, 1520], [8252, 2129, 1520]]], [[[-6735, 1188, 870], [8252, 2129, 870], [8753, -5855, 870]]], [[[-6234, -6796, 870], [-6735, 1188, 870], [8753, -5855, 870]]]]
        verts = []
        faces = []
        count = 0
        for lst in lsts: # lst is [[8252, 2129, 1520], [-6735, 1188, 1520], [8753, -5855, 1520]]
            if doublenest:
                lst = lst[0] # lst is [8252, 2129, 1520], [-6735, 1188, 1520], [8753, -5855, 1520]
            else:
                lst = lst
            faces.append(3)
            for coord in lst: #[8252, 2129, 1520]
                faces.append(count)
                verts.append(coord[0]) #x
                verts.append(coord[1]) #y
                verts.append(coord[2]) #z
                count += 1
            self.colorlst.append(material.colorint)
            self.numberFaces = + 1
        self.verts = verts
        self.faces = faces
        self.name = name
        self.material = material
        return self