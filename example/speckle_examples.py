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


"""This module provides some speckle examples
"""

__title__= "speckle_examples"
__author__ = "Maarten & Jonathan"
__url__ = "./example/speckle_examples.py"

import sys, os, math
from pathlib import Path

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))


from geometry.geometry2d import Point2D

from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_default_account
from specklepy.objects import Base
from specklepy.objects.geometry import Point as SpecklePoint
from specklepy.objects.geometry import Line as SpeckleLine
from specklepy.objects.geometry import Mesh as SpeckleMesh
from specklepy.objects.geometry import Polyline
from specklepy.objects.geometry import Vector as SpeckleVector
from specklepy.objects.geometry import Plane as SpecklePlane
from specklepy.objects.geometry import Arc as SpeckleArc
from specklepy.objects.primitive import Interval as SpeckleInterval

#Speckle Point
SpecklePoint.from_coords(0, 0, 0)

#Speckle Line
Line = SpeckleLine(start = SpecklePoint.from_coords(0, 0, 0), end = SpecklePoint.from_coords(800, 1000, 1000))

#Speckle Vector
#V1 = SpeckleVector.from_coords(0, 0, 1000) # Vector

#Speckle Plane
V1 = SpeckleVector.from_coords(0, 0, 1000) # Vector
X = SpeckleVector.from_coords(1000, 0, 0)
Y = SpeckleVector.from_coords(0, 1000, 0)
Orig = SpecklePoint.from_coords(0, 0, 0)
pln = SpecklePlane(origin = Orig, normal = V1, xdir = X, ydir = Y)

#Speckle Polyline
P1 = SpecklePoint.from_coords(0,0,0)
P2 = SpecklePoint.from_coords(1000,0,0)
P3 = SpecklePoint.from_coords(2000,0,0)
P4 = SpecklePoint.from_coords(2000,1000,0)

ply = Polyline.from_points([P1,P2,P3,P4])

#Speckle Mesh
Mesh = SpeckleMesh(vertices = [1000,1000,0,1000,1000,1000,2000,2000,0], faces = [3,0,1,2],
                   name = "Jonathan his mesh", colors = [-1762845660,-1762845660,-1762845660]) #, units = "mm"


#Speckle Arc
V1 = SpeckleVector.from_coords(0, 0, 1)
X = SpeckleVector.from_coords(1, 0, 0)
Y = SpeckleVector.from_coords(0, 1, 0)
Orig = SpecklePoint.from_coords(20, 0, 0)

pln = SpecklePlane(origin=Orig, normal=V1, xdir=X, ydir=Y)
int = SpeckleInterval(start=0, end=5, totalChildrenCount=1)

arcie = SpeckleArc(
   startPoint=SpecklePoint.from_coords(0, 0, 0),
   midPoint=SpecklePoint.from_coords(1000, 0, 0),
   endPoint=SpecklePoint.from_coords(2000, 500, 0),
   plane=pln,
   radius=1, #must be at least > 1
   interval=int,
   units="mm"
)


def mesh(box):
    return Mesh(
        vertices=[2, 1, 2, 4, 77.3, 5, 33, 4, 2],
        faces=[1, 2, 3, 4, 5, 6, 7],
        colors=[111, 222, 333, 444, 555, 666, 777],
        bbox=box,
        area=233,
        volume=232.2,
        units = "mm"
    )

def polyline(interval):
    return Polyline(
        value=[22, 44, 54.3, 99, 232, 21],
        closed=True,
        domain=interval,
        units="m",
        # These attributes are not handled in C#
        # bbox=None,
        # area=None,
        # length=None,
    )

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
