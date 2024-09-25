# [included in BP singlefile]
# [!not included in BP singlefile - start]
# -*- coding: utf8 -*-
# ***************************************************************************
# *   Copyright (c) 2024 Maarten Vroegindeweij & Jonathan van der Gouwe      *
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


"""This module provides tools for the modelling of panel components. a panel can be a floor, wall, panel, ceiling
"""

__title__ = "panel"
__author__ = "Maarten & Jonathan"
__url__ = "./objects/panel.py"

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from abstract.coordinatesystem import CoordinateSystem
from abstract.coordinatesystem import CSGlobal
from geometry.solid import Extrusion
from geometry.curve import *

# [!not included in BP singlefile - end]


class Panel(Serializable):
    # Panel
    def __init__(self):
        self.id = generateID()
        self.extrusion = None
        self.thickness = 0
        self.name = None
        self.perimeter: float = 0
        self.coordinatesystem: CoordinateSystem = CSGlobal
        self.colorint = None
        self.colorlst = []
        self.origincurve = None

    def serialize(self):
        id_value = str(self.id) if not isinstance(
            self.id, (str, int, float)) else self.id
        return {
            'id': id_value,
            'type': self.type,
            'extrusion': self.extrusion,
            'thickness': self.thickness,
            'name': self.name,
            'perimeter': self.perimeter,
            'coordinatesystem': self.coordinatesystem.serialize(),
            'color': self.color,
            'colorlst': self.colorlst,
            'origincurve': self.origincurve
        }

    @staticmethod
    def deserialize(data):
        panel = Panel()
        panel.id = data.get('id')
        panel.type = data.get('type')
        panel.extrusion = data.get('extrusion')
        panel.thickness = data.get('thickness', 0)
        panel.name = data.get('name', "none")
        panel.perimeter = data.get('perimeter', 0)
        panel.coordinatesystem = CoordinateSystem.deserialize(
            data['coordinatesystem'])
        panel.color = data.get('color')
        panel.colorlst = data.get('colorlst', [])
        panel.origincurve = data.get('origincurve')

        return panel

    @classmethod
    def by_polycurve_thickness(self, polycurve: PolyCurve, thickness: float, offset: float, name: str, colorrgbint):
        # Create panel by polycurve
        p1 = Panel()
        p1.name = name
        p1.thickness = thickness
        p1.extrusion = Extrusion.by_polycurve_height(
            polycurve, thickness, offset)
        p1.origincurve = polycurve
        p1.colorint = colorrgbint
        for j in range(int(len(p1.extrusion.verts) / 3)):
            p1.colorlst.append(colorrgbint)
        return p1

    @classmethod
    def by_baseline_height(self, baseline: Line, height: float, thickness: float, name: str, colorrgbint):
        # place panel vertical from baseline
        p1 = Panel()
        p1.name = name
        p1.thickness = thickness
        polycurve = PolyCurve.by_points(
            [baseline.start,
             baseline.end,
             Point.translate(baseline.end, Vector(0, 0, height)),
             Point.translate(baseline.start, Vector(0, 0, height))])
        p1.extrusion = Extrusion.by_polycurve_height(polycurve, thickness, 0)
        p1.origincurve = polycurve
        for j in range(int(len(p1.extrusion.verts) / 3)):
            p1.colorlst.append(colorrgbint)
        return p1
