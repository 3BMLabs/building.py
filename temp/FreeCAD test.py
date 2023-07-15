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


"""This module provides tools for exporting geometry to Speckle
"""

__title__ = "revit"
__author__ = "Maarten & Jonathan"
__url__ = "./exchange/freecad.py"

#FreeCAD imports
#import Part

#General imports
import sys, os, math

package_root_directory = "C:/Users/mikev/Documents/GitHub/building.py/"
sys.path.append(str(package_root_directory))

#Building Py Imports
from objects.frame import *
from objects.steelshape import *


test = profiledataToShape("HEA200").polycurve2d.curves

PartCurves = []


for i in test:
	if i.__class__.__name__ == "Arc2D":
        curve = Part.Arc(Vector(i.start.x,i.start.y,0),Vector(i.mid.x,i.mid.y,0),Vector(i.end.x,i.end.y,0))
        PartCurves.append(curve.toShape())
    elif i.__class__.__name__ == "Line2D":
        PartCurves.append(Part.makeLine(Vector(i.start.x,i.start.y,0),Vector(i.end.x,i.end.y,0)))

aWire = Part.Wire(PartCurves)
p = Part.Face(aWire)
solid = p.extrude(FreeCAD.Vector(0, 0, float(k) * 1000))
sld = Part.show(solid)

PartCurves.append(Line2D(i.start.translate(v1), i.end.translate(v1)))
    else:
        print("Curvetype not found")

print(test)