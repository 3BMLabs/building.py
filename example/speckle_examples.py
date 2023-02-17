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


"""This module provides some speckle examples
"""

__title__= "speckle_examples"
__author__ = "Maarten & Jonathan"
__url__ = "./example/speckle_examples.py"


from geometry.flat import Point2D

from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_default_account
from specklepy.objects import Base
from specklepy.objects.geometry import Point as SpecklePoint
from specklepy.objects.geometry import Line as SpeckleLine
from specklepy.objects.geometry import Mesh as SpeckleMesh
from specklepy.objects.geometry import Polyline

#Speckle Line

Line = SpeckLine(start = SpecklePoint.from_coords(0, 0, 0), end = SpecklePoint.from_coords(800, 1000, 1000))


class Mesh(Base):
    #mesh class to export to speckle
    vertices = None
    faces = None
    name = "none"

#HEA200 profiel van 2D PolyCurve naar 3D SpeckleCurve
prof = I_shape_parallel_flange("HEA200",200,200,10,15,5) #2D PolyCurve
polygon3D = polygon(prof.curve) #3D Polygon

#To Speckle
from specklepy.objects.geometry import Polyline

SpecklePoints = []

#origin
for i in polygon3D:
    SpecklePoints.append(PointToSpecklePoint(i))
ln = Polyline.from_points(SpecklePoints)  #3D polyline in Speckle

#1e translatie
SpecklePoints = []
for i in polygon3D:
    j = transformPoint(i, coordinatesystem.CSGlobal, Point(0,0,0), Vector3(1000,1000,1000))
    SpecklePoints.append(PointToSpecklePoint(j))

ln2 = Polyline.from_points(SpecklePoints)  #3D polyline in Speckle

#2e translatie
SpecklePoints = []
for i in polygon3D:
    j = transformPoint(i, coordinatesystem.CSGlobal, Point(800,1000,1000),Vector3(1000,1000,1000))
    SpecklePoints.append(PointToSpecklePoint(j))


class Beam:
    #Beam
    def __init__(self):
        self.verts = []
        self.faces = []
        self.meshpb: MeshPB
        self.Mesh: Mesh #SpeckleMesh
        self.name = "none"
        self.start: Point3D
        self.end: Point3D
        self.curve: Line3D
        self.length: double = 0
        self.rotxy: double = 0
        self.rotxz: double = 0
        self.rotyz: double = 0

    def byStartpointEndpoint(self, start, end, profile):
        self.start = start
        self.end = end
        self.curve = Line3D(start,end)
        self.length = self.curve.length
        self.name = profile[1][0]
        self.meshpb = MeshPB()
        self.rotxy = self.curve.Zrotxy
        self.rotxz = self.curve.Yrotxz
        self.rotyz = self.curve.Xrotyz
        self.meshpb.byPolyCurveHeight(profile[0],self.length)
        self.meshpb = rotateMeshYZ(self.meshpb, RotationXYZ(0, 0, 90))
        self.meshpb = rotateMeshXY(self.meshpb, RotationXYZ(90+self.curve.Zrotxy, 0, 0))
        self.meshpb = rotateMeshXZ(self.meshpb, RotationXYZ(0, -(90-self.curve.Yrotxz), 0))
        self.meshpb = rotateMeshYZ(self.meshpb, RotationXYZ(0, 0, -(90+self.curve.Xrotyz)))   # gekke buggie
        self.meshpb = translateMeshXYZ(self.meshpb,VectorXYZ(self.start.x, self.start.y, self.start.z))
        self.Mesh = Mesh(vertices=self.meshpb.verts, faces=self.meshpb.faces, name = self.name)
