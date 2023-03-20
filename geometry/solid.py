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


"""This module provides tools to create solids
"""

__title__= "solid"
__author__ = "Maarten & Jonathan"
__url__ = "./geometry/solid.py"


import sys, os, math
from pathlib import Path

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

from geometry.point import *
from geometry.curve import *
from abstract.plane import *
from packages import helper


class Extrusion:
    #Extrude a 2D profile to a 3D mesh
    def __init__(self):
        self.verts = []
        self.faces = []
        self.numberFaces = 0
        self.countVertsFaces = 0 # total number of verts per face (not the same as total verts)
        self.name = "none"
        self.color = (255,255,0)
        self.colorlst = []

    @classmethod
    def byPolyCurveHeightVector(cls, polycurve, height, CSOld, startpoint, DirectionVector: Vector3):
        Extrus = Extrusion()
        #2D PolyCurve @ Global origin
        count = 0
        for i in polycurve:
            startpointLow = transformPoint(Point(i.start.x,i.start.y,0), CSOld, startpoint, DirectionVector)
            endpointLow = transformPoint(Point(i.end.x,i.end.y,0), CSOld, startpoint, DirectionVector)
            endpointHigh = transformPoint(Point(i.end.x,i.end.y,height), CSOld, startpoint, DirectionVector)
            startpointHigh = transformPoint(Point(i.start.x,i.start.y,height), CSOld, startpoint, DirectionVector)

            #Construct faces perpendicular on polycurve
            Extrus.faces.append(4)
            Extrus.verts.append(startpointLow.x)
            Extrus.verts.append(startpointLow.y)
            Extrus.verts.append(startpointLow.z)
            Extrus.faces.append(count)
            count += 1
            Extrus.verts.append(endpointLow.x)
            Extrus.verts.append(endpointLow.y)
            Extrus.verts.append(endpointLow.z)
            Extrus.faces.append(count)
            count += 1
            Extrus.verts.append(endpointHigh.x)
            Extrus.verts.append(endpointHigh.y)
            Extrus.verts.append(endpointHigh.z)
            Extrus.faces.append(count)
            count += 1
            Extrus.verts.append(startpointHigh.x)
            Extrus.verts.append(startpointHigh.y)
            Extrus.verts.append(startpointHigh.z)
            Extrus.faces.append(count)
            count += 1
            Extrus.numberFaces = Extrus.numberFaces + 1
            #    vert = [0, 0, 0, 1000, 0, 0, 1000, 2000, 0, 0, 1000, 0, 0, 2000, 2000, 3000, 2000, 1000]
            # list structure of verts is x y z x y z x y z
            #    faces = [3, 0, 1, 2, 3, 2, 3, 5]
            # list structure of faces is [number of verts], vert.index, vert.index, vert.index, vert2.index. enz.
            # first number is number of vertices.
            # then

        #bottomface
        Extrus.faces.append(len(polycurve))
        count = 0
        for i in polycurve:
            Extrus.faces.append(count)
            count = count + 4

        # topface
        Extrus.faces.append(len(polycurve))
        count = 3
        for i in polycurve:
            Extrus.faces.append(count)
            count = count + 4

        Extrus.countVertsFaces = (4 * Extrus.numberFaces) #aantal zonder bovenzijde/onderzijde

        Extrus.countVertsFaces = Extrus.countVertsFaces + len(polycurve)*2
        Extrus.numberFaces = Extrus.numberFaces + 2

        for j in range(int(len(Extrus.verts) / 3)):
            Extrus.colorlst.append(Extrus.color)

        return Extrus

    @classmethod
    def byPolyCurveHeight(cls, polycurve: PolyCurve, height, dzloc):
        #global len
        Extrus = Extrusion()
        Points = polycurve.points
        V1 = Vector3.byTwoPoints(Points[0], Points[1])  # Vector op basis van punt 0 en 1
        V2 = Vector3.byTwoPoints(Points[-2], Points[-1])  # Vector op basis van laatste punt en een na laatste punt

        p1 = Plane.byTwoVectorsOrigin(V1, V2, Points[0]) #Workplane of PolyCurve
        norm = p1.Normal

        pnts = []
        faces = []
        #allverts
        for pnt in Points:
            pnts.append(Point.translate(pnt, Vector3.product(dzloc, norm))) # Onderzijde verplaatst met dzloc
        for pnt in Points:
            pnts.append(Point.translate(pnt, Vector3.product((dzloc+height), norm)))  # Bovenzijde verplaatst met dzloc

        numPoints = len(Points)

        #Bottomface
        count = 0
        face = []
        for x in range(numPoints):
            face.append(count)
            count = count + 1
        faces.append(face)

        # Topface
        count = 0
        face = []
        for x in range(numPoints):
            face.append(count+numPoints)
            count = count + 1
        faces.append(face)

        # Sides
        count = 0
        length = len(faces[0])
        for i,j in zip(faces[0],faces[1]):
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

        #toMeshStructure
        for i in pnts:
            Extrus.verts.append(i.x)
            Extrus.verts.append(i.y)
            Extrus.verts.append(i.z)

        for x in faces:
            Extrus.faces.append(len(x)) #Number of verts in face
            for y in x:
                Extrus.faces.append(y)
            #    vert = [0, 0, 0, 1000, 0, 0, 1000, 2000, 0, 0, 1000, 0, 0, 2000, 2000, 3000, 2000, 1000]
            # list structure of verts is x y z x y z x y z
            #    faces = [3, 0, 1, 2, 3, 2, 3, 5]
            # list structure of faces is [number of verts], vert.index, vert.index, vert.index, vert2.index. enz.
            # first number is number of vertices.
            # then
        Extrus.numberFaces = len(faces)
        Extrus.countVertsFaces = (4 * len(faces))
        return Extrus