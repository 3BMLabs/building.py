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
"""This module provides tools for analytical element like supports, loads
"""

__title__= "analytical"
__author__ = "Maarten & Jonathan"
__url__ = "./objects/analytical.py"

class Support:
    def __init__(self):
        self.Number = None
        self.Point: Point = Point(0,0,0)
        self.Tx: str = "" # A, P, N, S
        self.Ty: str = "" # A, P, N, S
        self.Tz: str = "" # A, P, N, S
        self.Rx: str = "" # A, P, N, S
        self.Ry: str = "" # A, P, N, S
        self.Rz: str = "" # A, P, N, S
        self.Kx: float = 0 # kN/m
        self.Ky: float = 0 # kN/m
        self.Kz: float = 0 # kN/m
        self.Cx: float = 0 # kNm/rad
        self.Cy: float = 0 # kNm/rad
        self.Cz: float = 0 # kNm/rad
        self.dx: float = 0 #eccentricity in x
        self.dy: float = 0 #eccentricity in y
        self.dz: float = 0 #eccentricity in z






        < Nodenumber > 3 < / Nodenumber >
        < Tx > < / Tx >
        < Ty > < / Ty >
        < Tz > S < / Tz >
        < Rx > < / Rx >
        < Ry > < / Ry >
        < Rz > < / Rz >
        < Kx > 0 < / Kx >
        < Ky > 0 < / Ky >
        < Kz > 35000 < / Kz >
        < Cx > 0 < / Cx >
        < Cy > 0 < / Cy >
        < Cz > 0 < / Cz >
        < dx > 0 < / dx >
        < dy > 0 < / dy >
        < dz > 0 < / dz >