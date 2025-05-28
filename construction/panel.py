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


"""This module provides tools for the modelling of panel components. a panel can be a floor, wall, panel, ceiling"""

__title__ = "panel"
__author__ = "Maarten & Jonathan"
__url__ = "./objects/panel.py"

import sys


from abstract.segmentation import Meshable, TesselationSettings
from abstract.serializable import Serializable
from abstract.transformer import dimension_changer
from abstract.vector import Point, Vector
from geometry.curve import Line, PolyCurve
from geometry.mesh import Mesh
from geometry.solid import Extrusion
from library.material import BaseTimber, Material


# [!not included in BP singlefile - end]


class Panel(Serializable, Meshable):
    # Panel
    def __init__(self, extrusion: Extrusion, material: Material, name: str = None):
        self.extrusion = extrusion
        self.material = material
        self.name = name

    def to_mesh(self, settings: TesselationSettings) -> Mesh:
        colorSettings = TesselationSettings(settings.max_angle, self.material.color.int)
        return self.extrusion.to_mesh(colorSettings)

    @classmethod
    def by_polycurve_thickness(
        self,
        polycurve: PolyCurve,
        thickness: float,
        offset: float = 0,
        name: str = None,
        material=BaseTimber,
    ):
        # Create panel by polycurve
        p1 = Panel(
            Extrusion.by_polycurve_height(polycurve, thickness, offset), material, name
        )
        return p1

    @classmethod
    def by_baseline_height(
        self,
        baseline: Line,
        height: float,
        thickness: float,
        name: str = None,
        material=BaseTimber,
    ):
        # place panel vertical from baseline
        return Panel(
            Extrusion.by_polycurve_height(
                PolyCurve.by_points(
                    [
                        baseline.start,
                        baseline.end,
                        baseline.end + Vector(0, 0, height),
                        baseline.start + Vector(0, 0, height),
                    ]
                ),
                thickness,
                0,
            ),
            material,
            name,
        )
