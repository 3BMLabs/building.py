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


"""This module provides tools for the modelling of panel components. a panel can be a floor, wall, panel, ceiling
"""

__title__= "panel"
__author__ = "Maarten & Jonathan"
__url__ = "./objects/panel.py"

import sys, os, math
from pathlib import Path

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

from abstract.coordinatesystem import CoordinateSystem
from abstract.coordinatesystem import CSGlobal
from geometry.solid import Extrusion
from geometry.curve import *

class Panel:
    #Panel
    def __init__(self):
        self.extrusion = None
        self.thickness = 0
        self.name = "none"
        self.perimeter: float = 0
        self.coordinatesystem: CoordinateSystem = CSGlobal #TODO: implementend real coordinatesystem based on first curve and/or overruled by user
        self.color = None
        self.colorlst = []
        self.origincurve = None

    @classmethod
    def byPolyCurveThickness(cls, polycurve: PolyCurve, thickness: float, offset: float, name: str, colorrgbint):
        #Create panel by polycurve
        p1 = Panel()
        p1.name = name
        p1.thickness = thickness
        p1.extrusion = Extrusion.byPolyCurveHeight(polycurve, thickness, offset)
        p1.origincurve = polycurve
        for j in range(int(len(p1.extrusion.verts) / 3)):
            p1.colorlst.append(colorrgbint)
        return p1

    @classmethod
    def byBaselineHeight(cls, baseline: Line, height: float, thickness: float, name: str, colorrgbint):
        #place panel vertical from baseline
        p1 = Panel()
        p1.name = name
        p1.thickness = thickness
        polycurve = PolyCurve.byPoints(
            [baseline.start,
             baseline.end,
             Point.translate(baseline.end, Vector3(0, 0, height)),
             Point.translate(baseline.start, Vector3(0, 0, height)),
             baseline.start])
        p1.extrusion = Extrusion.byPolyCurveHeight(polycurve, thickness, 0)
        p1.origincurve = polycurve
        for j in range(int(len(p1.extrusion.verts) / 3)):
            p1.colorlst.append(colorrgbint)
        return p1
