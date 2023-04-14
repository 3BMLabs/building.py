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

from geometry.point import *
from geometry.curve import *
"""This module provides tools for analytical element like supports, loads
"""

__title__= "analytical"
__author__ = "Maarten & Jonathan"
__url__ = "./objects/analytical.py"

class Support:
    def __init__(self):
        self.Number = None
        self.Point: Point = Point(0,0,0)
        self.Tx: str = " " # A, P, N, S
        self.Ty: str = " " # A, P, N, S
        self.Tz: str = " " # A, P, N, S
        self.Rx: str = " " # A, P, N, S
        self.Ry: str = " " # A, P, N, S
        self.Rz: str = " " # A, P, N, S
        self.Kx: float = 0 # kN/m
        self.Ky: float = 0 # kN/m
        self.Kz: float = 0 # kN/m
        self.Cx: float = 0 # kNm/rad
        self.Cy: float = 0 # kNm/rad
        self.Cz: float = 0 # kNm/rad
        self.dx: float = 0 #eccentricity in x
        self.dy: float = 0 #eccentricity in y
        self.dz: float = 0 #eccentricity in z

    @staticmethod
    def pinned(PlacementPoint):
        sup = Support()
        sup.Point = PlacementPoint
        sup.Tx = "A"
        sup.Ty = "A"
        sup.Tz = "A"
        return(sup)

    @staticmethod
    def xRoller(PlacementPoint):
        sup = Support()
        sup.Point = PlacementPoint
        sup.Ty = "A"
        sup.Tz = "A"
        return(sup)

    @staticmethod
    def yRoller(PlacementPoint):
        sup = Support()
        sup.Point = PlacementPoint
        sup.Tx = "A"
        sup.Tz = "A"
        return(sup)

    @staticmethod
    def zRoller(PlacementPoint):
        sup = Support()
        sup.Point = PlacementPoint
        sup.Tx = "A"
        sup.Ty = "A"
        return(sup)

    @staticmethod
    def fixed(PlacementPoint):
        sup = Support()
        sup.Point = PlacementPoint
        sup.Tx = "A"
        sup.Ty = "A"
        sup.Tz = "A"
        sup.Rx = "A"
        sup.Ry = "A"
        sup.Rz = "A"
        return(sup)

class LoadCase:
    def __init__(self):
        self.Number = None
        self.Description: str = ""
        self.psi0 = 1
        self.psi1 = 1
        self.psi2 = 1
        self.Type = 0   #0 = permanent, 1 = variabel

class SurfaceLoad:
    def __init__(self):
        self.LoadCase = None
        self.PolyCurve: PolyCurve = None
        self.Description: str = ""
        self.crs = "ccaa0435161960d4c7e436cf107a03f61"
        self.direction = "caf2b4ce743de1df30071f9566b1015c6"
        self.LoadBearingDirection = "cfebf3fce7063ab9a89d28a86508c0fb3"
        self.q1 = 0
        self.q2 = 0
        self.q3 = 0
        self.LoadConstantOrLinear = "cb81ae405e988f21166edf06d7fd646fb"
        self.iq1 = -1
        self.iq2 = -1
        self.iq3 = -1

    @staticmethod
    def byLoadCasePolyCurveQ(LoadCase, PolyCurve, q):
        SL = SurfaceLoad()
        SL.LoadCase = LoadCase
        SL.PolyCurve = PolyCurve
        SL.q1 = q
        SL.q2 = q
        SL.q3 = q
        return SL


class LoadPanel:
    def __init__(self):
        self.PolyCurve: PolyCurve = None
        self.Description: str = ""
        self.LoadBearingDirection = "X"
        self.SurfaceType = "" #Wall, saddle_roof_positive_pitch #Wall, / Free-standing wall, Flat roof, Shed roof, Saddle roof, Unknown

def ChessBoardSurfaceLoadsRectangle(startx, starty, dx, dy, nx, ny, width, height, LoadCase, q123, description:str):
    SurfaceLoads = []
    x = startx
    y = starty
    for j in range(ny):
        for i in range(nx):
            SL = SurfaceLoad()
            SL.Description = description
            SL.LoadCase = LoadCase
            SL.PolyCurve = PolyCurve.byPoints(
                [Point(x, y, 0),
                Point(x + width, y, 0),
                Point(x, y + height, 0),
                Point(x, y, 0)]
            )
            SL.q1 = SL.q2 = SL.q3 = q123 #[kN/m2]
            SurfaceLoads.append(SL)
            x = x + dx
        y = y + dy
    return SurfaceLoads
