# [included in BP singlefile]
# [!not included in BP singlefile - start]
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


"""This module provides tools for coordinatesystems
"""

__title__= "coordinatesystem"
__author__ = "Maarten & Jonathan"
__url__ = "./abstract/coordinatesystem.py"


import math
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from abstract.vector import *
from geometry.point import Point
from project.fileformat import project

# [!not included in BP singlefile - end]

class CoordinateSystem:
    #UNITY VECTORS REQUIRED #TOdo organize resic
    def __init__(self, origin: Point, xaxis, yaxis, zaxis):
        self.Origin = origin
        self.Xaxis = Vector3.normalize(xaxis)
        self.Yaxis = Vector3.normalize(yaxis)
        self.Zaxis = Vector3.normalize(zaxis)

    @classmethod
    def by_origin(self, origin: Point):
        self.Origin = origin
        self.Xaxis = XAxis
        self.Yaxis = YAxis
        self.Zaxis = ZAxis
        return self

    @staticmethod
    def translate(CSOld, direction):
        CSNew = CoordinateSystem(CSOld.Origin, CSOld.Xaxis, CSOld.Yaxis, CSOld.Zaxis)
        new_origin = Point.translate(CSNew.Origin, direction)
        CSNew.Origin = new_origin
        return CSNew

    @staticmethod
    def move_local(CSOld,x: float, y:float, z:float):
        #move coordinatesystem by y in local coordinates(not global)
        xloc_vect_norm = CSOld.Xaxis
        xdisp = Vector3.scale(xloc_vect_norm,x)
        yloc_vect_norm = CSOld.Xaxis
        ydisp = Vector3.scale(yloc_vect_norm, y)
        zloc_vect_norm = CSOld.Xaxis
        zdisp = Vector3.scale(zloc_vect_norm, z)
        disp = Vector3.sum3(xdisp,ydisp,zdisp)
        CS = CoordinateSystem.translate(CSOld,disp)
        return CS

    @staticmethod
    def by_point_main_vector(self, NewOriginCoordinateSystem: Point, DirectionVectorZ):
        vz = DirectionVectorZ  # LineVector and new Z-axis
        vz = Vector3.normalize(vz)  # NewZAxis
        vx = Vector3.perpendicular(vz)[0]  # NewXAxis
        try:
            vx = Vector3.normalize(vx)  # NewXAxisnormalized
        except:
            vx = Vector3(1, 0, 0) #In case of vertical element the length is zero
        vy = Vector3.perpendicular(vz)[1]  # NewYAxis
        try:
            vy = Vector3.normalize(vy)  # NewYAxisnormalized
        except:
            vy = Vector3(0, 1, 0)  #In case of vertical element the length is zero
        CSNew = CoordinateSystem(NewOriginCoordinateSystem, vx, vy, vz)
        return CSNew

    def __str__(self):
        return f"{__class__.__name__}(" + f"{self.Origin}, {self.Xaxis}, {self.Yaxis}, {self.Zaxis})"

CSGlobal = project.CSGlobal