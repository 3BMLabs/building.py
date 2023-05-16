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


"""This module provides tools for familys/objects
"""

__title__= "plane"
__author__ = "Maarten & Jonathan"
__url__ = "./objects/objectcollection.py"

import sys, os, math
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from abstract.vector import Vector3
from geometry.point import Point
from geometry.curve import Line, PolyCurve


class WurksRaster:
    def __init__(self):
        self.name = "x"
        

    def byLine(self, lines: list[Line], height: float):
        self.height = Vector3(0, 0, height)
        self.inputLines = lines
        self.toPolyCurve()


    def fRaster(self):
        fourlines = []
        for line in self.inputLines:
            btm = line
            fourlines.append(btm)
            offbtm = Line.offset(btm, self.height)
            fourlines.append(offbtm)
            left = Line(btm.start, offbtm.start)
            fourlines.append(left)
            right = Line(btm.end, offbtm.end)
            fourlines.append(right)
        return fourlines
    

    def toPolyCurve(self):
        self.lines = self.fRaster()
        print(self.lines)
        return PolyCurve.byJoinedCurves(self.lines)