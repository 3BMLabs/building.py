# -*- coding: utf8 -*-
# ***************************************************************************
# *   Copyright (c) 2023 Maarten Vroegindeweij & Jonathan van der Gouwe      *
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


"""This module provides tools to create curves
"""

__title__= "curve"
__author__ = "Maarten & Jonathan"
__url__ = "./geometry/curve.py"


import sys, os, math
from pathlib import Path

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

from geometry.point import *
from packages import helper
from abstract.vector import Vector3
from abstract.plane import Plane

from temp.EXPORTER import send_to_speckle
from specklepy.objects.geometry import Brep, BrepFace, BrepLoop, BrepLoopType, BrepEdge, Point, Vector, BrepTrim, BrepTrimType


#Brep start
# pt1 = Point(x=0, y=0, z=0)
# pt2 = Point(x=1, y=0, z=0)
# pt3 = Point(x=0, y=1, z=0)
# pt4 = Point(x=1, y=1, z=0)
# brep = Brep(points=[pt1, pt2, pt3, pt4], faces=[0, 1, 2, 3])
# obj1 = [brep]

# send_to_speckle(INhost="https://3bm.exchange", INstream_id="fa4e56aed4", INobjects=obj1)
#Brep end


# #BrepEdge start
start_point = Point.from_coords(0, 0, 0)
end_point = Point.from_coords(1, 1, 1)
tangent_vector = Vector.from_coords(1, 0, 0)
brep_edge = BrepEdge(start_point=start_point, end_point=end_point, tangent_vector=tangent_vector)
brep_edge._displayValue = True
obj1 = [brep_edge]
send_to_speckle(INhost="https://3bm.exchange", INstream_id="fa4e56aed4", INobjects=obj1)

# #BrepEdge end


# #BrepFace start
# pt1 = Point(x=0, y=0, z=0)
# pt2 = Point(x=1, y=0, z=0)
# pt3 = Point(x=0, y=1, z=0)
# edge1 = BrepEdge(start=pt1, end=pt2)
# edge2 = BrepEdge(start=pt2, end=pt3)
# edge3 = BrepEdge(start=pt3, end=pt1)
# outer_loop = BrepLoop(type=BrepLoopType.Outer, edges=[edge1, edge2, edge3])
# face = BrepFace(outer_loop=outer_loop)
# obj1 = [face]

# send_to_speckle(INhost="https://3bm.exchange", INstream_id="fa4e56aed4", INobjects=obj1)
# #BrepFace end


# #BrepLoop start
# pt1 = Point(x=0, y=0, z=0)
# pt2 = Point(x=1, y=0, z=0)
# pt3 = Point(x=0, y=1, z=0)
# edge1 = BrepEdge(start=pt1, end=pt2)
# edge2 = BrepEdge(start=pt2, end=pt3)
# edge3 = BrepEdge(start=pt3, end=pt1)
# loop = BrepLoop(type=BrepLoopType.CurveOnSurface, edges=[edge1, edge2, edge3])
# obj1 = [loop]

# send_to_speckle(INhost="https://3bm.exchange", INstream_id="fa4e56aed4", INobjects=obj1)
# #BrepLoop end


# #BrepTrim start
# pt1 = Point(x=0, y=0, z=0)
# pt2 = Point(x=1, y=0, z=0)
# edge = BrepEdge(start=pt1, end=pt2)
# trim = BrepTrim(edge=edge, type=BrepTrimType.CurveOnSurface)
# obj1 = [trim]

# send_to_speckle(INhost="https://3bm.exchange", INstream_id="fa4e56aed4", INobjects=obj1)
# #BrepTrim end