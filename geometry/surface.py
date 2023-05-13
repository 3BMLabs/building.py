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


"""This module provides tools to create surfaces
"""

__title__= "surface"
__author__ = "Maarten & Jonathan"
__url__ = "./geometry/surface.py"


import sys, os, math
from pathlib import Path

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

from geometry.point import *
from packages import helper
from geometry.curve import *
from geometry.solid import Extrusion
from abstract.color import Color
from abstract.intersect2d import *

#check if there are innercurves inside the outer curve.

class Surface: #Polycurves must be closed!!!!!!!
    def __init__(self, PolyCurves:list=PolyCurve, color=None, id=helper.generateID()) -> None:
        #self.outerPolyCurve
        #self.innerPolyCurves
        self.extrusion = []
        self.thickness = 0
        self.offset = 0
        self.name = "test2"
        self.id = id
        self.PolyCurveList = PolyCurves
        self.color = None
        self.origincurve = None
        if color is None:
            self.color = Color.rgb_to_int(Color().Components("gray"))
        else:
            self.color = color

        self.colorlst = []
        self.fill(self.PolyCurveList)

    def fill(self, PolyCurveList):
        for polyCurve in PolyCurveList:
            plycColorList = []
            p = Extrusion.byPolyCurveHeight(polyCurve, self.thickness, self.offset)
            self.extrusion.append(p)
            for j in range(int(len(p.verts) / 3)):
                plycColorList.append(self.color)
            self.colorlst.append(plycColorList)

    def void(self, polyCurve):
        # Find the index of the extrusion that intersects with the polyCurve
        idx = None
        for i, extr in enumerate(self.extrusion):
            if extr.intersects(polyCurve):
                idx = i
                break

        if idx is not None:
            # Remove the intersected extrusion from the extrusion list
            removed = self.extrusion.pop(idx)

            # Remove the corresponding color list from the colorlst list
            removed_colors = self.colorlst.pop(idx)

            # Create a new list of colors for the remaining extrusions
            new_colors = []
            for colors in self.colorlst:
                new_colors.extend(colors)

            # Fill the hole with a new surface
            hole_surface = Surface([polyCurve], color=self.color)
            hole_surface.fill([polyCurve])
            hole_extrusion = hole_surface.extrusion[0]

            # Add the hole extrusion to the extrusion list
            self.extrusion.append(hole_extrusion)

            # Add the hole colors to the colorlst list
            hole_colors = [Color.rgb_to_int(Color().Components("red"))] * int(len(hole_extrusion.verts) / 3)
            self.colorlst.append(hole_colors)

            # Add the remaining colors to the colorlst list
            self.colorlst.extend(new_colors)

            # Update the origin curve
            self.origincurve = self.PolyCurveList[0]


    def __id__(self):
        return f"id:{self.id}"

    def __str__(self) -> str:
        return f"{__class__.__name__}({self})"


class NurbsSurface: #based on point data / degreeU&countU / degreeV&countV?
    def __init__(self, id=helper.generateID()) -> None:
        pass
        self.id = id
    pass

    def __id__(self):
        return f"id:{self.id}"

    def __str__(self) -> str:
        return f"{__class__.__name__}({self})"


class PolySurface:
    def __init__(self, id=helper.generateID()) -> None:
        pass
        self.id = id
    pass

    def __id__(self):
        return f"id:{self.id}"

    def __str__(self) -> str:
        return f"{__class__.__name__}({self})"