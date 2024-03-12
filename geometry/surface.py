# [included in BP singlefile]
# [!not included in BP singlefile - start]
# -*- coding: utf8 -*-
#***************************************************************************
#*   Copyright (c) 2024 Maarten Vroegindeweij & Jonathan van der Gouwe      *
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


import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from geometry.curve import *
from geometry.solid import Extrusion
from abstract.color import Color
from abstract.intersect2d import *

# [!not included in BP singlefile - end]
#check if there are innercurves inside the outer curve.

class Surface:
    def __init__(self, PolyCurves:PolyCurve, color=None) -> None:
        #self.outerPolyCurve
        #self.innerPolyCurves
        if isinstance(PolyCurves, PolyCurve):
            PolyCurves = [PolyCurves]
        self.type = __class__.__name__
        self.mesh = []
        self.length = 0
        self.area = 0 #return the same area of the polyCurve but remove the innerpolycurves
        self.offset = 0
        self.name = "test2"
        self.id = generateID()
        self.PolyCurveList = PolyCurves
        self.origincurve = None
        if color is None:
            self.color = Color.rgb_to_int(Color().Components("gray"))
        else:
            self.color = color

        self.colorlst = []
        self.fill(self.PolyCurveList)

    def serialize(self):
        return {
            'type': self.type,
            'mesh': self.mesh,
            'length': self.length,
            'area': self.area,
            'offset': self.offset,
            'name': self.name,
            'id': self.id,
            'PolyCurveList': [polycurve.serialize() for polycurve in self.PolyCurveList],
            'origincurve': self.origincurve.serialize() if self.origincurve else None,
            'color': self.color,
            'colorlst': self.colorlst
        }
    
    @staticmethod
    def deserialize(data):
        polycurves = [PolyCurve.deserialize(pc_data) for pc_data in data.get('PolyCurveList', [])]
        surface = Surface(polycurves, data.get('color'))

        surface.mesh = data.get('mesh', [])
        surface.length = data.get('length', 0)
        surface.area = data.get('area', 0)
        surface.offset = data.get('offset', 0)
        surface.name = data.get('name', "test2")
        surface.id = data.get('id')
        surface.colorlst = data.get('colorlst', [])

        if data.get('origincurve'):
            surface.origincurve = PolyCurve.deserialize(data['origincurve'])

        return surface

    def fill(self, PolyCurveList):
        if isinstance(PolyCurveList, PolyCurve):
            plycColorList = []
            p = Extrusion.by_polycurve_height(PolyCurveList, 0, self.offset)
            self.mesh.append(p)
            for j in range(int(len(p.verts) / 3)):
                plycColorList.append(self.color)
            self.colorlst.append(plycColorList)

        elif isinstance(PolyCurveList, list):
            for polyCurve in PolyCurveList:
                plycColorList = []
                p = Extrusion.by_polycurve_height(polyCurve, 0, self.offset)
                self.mesh.append(p)
                for j in range(int(len(p.verts) / 3)):
                    plycColorList.append(self.color)
                self.colorlst.append(plycColorList)

    def void(self, polyCurve):
        # Find the index of the extrusion that intersects with the polyCurve
        idx = None
        for i, extr in enumerate(self.mesh):
            if extr.intersects(polyCurve):
                idx = i
                break

        if idx is not None:
            # Remove the intersected extrusion from the extrusion list
            removed = self.mesh.pop(idx)

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
            self.mesh.append(hole_extrusion)

            # Add the hole colors to the colorlst list
            hole_colors = [Color.rgb_to_int(Color().Components("red"))] * int(len(hole_extrusion.verts) / 3)
            self.colorlst.append(hole_colors)

            # Add the remaining colors to the colorlst list
            self.colorlst.extend(new_colors)

            # Update the origin curve
            self.origincurve = self.PolyCurveList[0]


    def __id__(self):
        return f"id:{self.id}"

    # def __str__(self) -> str:
    #     return f"{__class__.__name__}({self})"


class NurbsSurface: #based on point data / degreeU&countU / degreeV&countV?
    def __init__(self) -> None:
        pass
        self.id = generateID()
        self.type = __class__.__name__        
    pass

    def __id__(self):
        return f"id:{self.id}"

    def __str__(self) -> str:
        return f"{__class__.__name__}({self})"


class PolySurface:
    def __init__(self) -> None:
        pass
        self.id = generateID()
        self.type = __class__.__name__        
    pass

    def __id__(self):
        return f"id:{self.id}"

    def __str__(self) -> str:
        return f"{__class__.__name__}({self})"