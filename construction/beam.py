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


"""This module provides tools for the modelling of framing components. Almost every object in a building is a frame"""

__title__ = "shape"
__author__ = "Maarten & Jonathan"
__url__ = "./objects/frame.py"

import sys
from typing import Union


from abstract.segmentation import Meshable, TesselationSettings
from abstract.vector import Vector
from geometry.curve import PolyCurve, Polygon
from geometry.mesh import Mesh
from abstract.vector import Point
from geometry.solid import Extrusion
from library.material import BaseSteel, Material, BaseOther
from library.profile import profile_by_name, justification_to_vector

from abstract.serializable import Serializable
from construction.profile import Profile, RectangleProfile

# [!not included in BP singlefile - end]


# ToDo Na update van color moet ook de colorlist geupdate worden
class Beam(Serializable, Meshable):
    def __init__(
        self,
        start: Point,
        end: Point,
        profile: Profile | str,
        name: str = "Beam",
        material: Material = BaseSteel,
        angle: float = 0,
        justification: list[str] | Vector = Vector(),
    ):
        if isinstance(profile, str):
            profile = profile_by_name(profile)

        if not isinstance(justification, Vector):
            justification = justification_to_vector(
                profile.curve, justification[0], justification[1]
            )

        self.name = name
        self.comments = None
        self.start = start
        self.end = end
        self.profile = profile
        self.material = material
        self.angle = angle
        self.justification = justification

        self.profile_data = (
            None  # 2D polycurve of the sectionprofile (DOUBLE TO BE REMOVED)
        )
        self.centerbottom = None

    @property
    def extrusion(self) -> Extrusion:
        """heavy!"""
        return Extrusion.by_2d_polycurve_vector(
            self.profile.curve, self.start, self.end - self.start
        )

    def to_mesh(self, settings: TesselationSettings) -> Mesh:
        self.extrusion.to_mesh(settings)


Column = Beam
# columns and beams are the same, the profiles are the same, but they function as beams or columns.
