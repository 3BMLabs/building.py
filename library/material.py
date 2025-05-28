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


"""This module provides a library of materials"""

__title__ = "material"
__author__ = "Maarten & Jonathan"
__url__ = "./library/material.py"

from pathlib import Path

from abstract.color import Color

# [!not included in BP singlefile - end]


def rgb_to_int(rgb):
    r, g, b = [max(0, min(255, c)) for c in rgb]

    return (255 << 24) | (r << 16) | (g << 8) | b


class Material:
    def __init__(self, name: str, color: Color):
        self.name = name
        self.color = color


# Building Materials
BaseConcrete = Material("Concrete", Color.by_rgb([192, 192, 192]))
BaseTimber = Material("Timber", Color.by_rgb([191, 159, 116]))
BaseSteel = Material("Steel", Color.by_rgb([237, 28, 36]))
BaseOther = Material("Other", Color.by_rgb([150, 150, 150]))
BaseBrick = Material("Brick", Color.by_rgb([170, 77, 47]))
BaseBrickYellow = Material("BrickYellow", Color.by_rgb([208, 187, 147]))

# GIS Materials
BaseBuilding = Material("Building", Color.by_rgb([150, 28, 36]))
BaseWater = Material("Water", Color.by_rgb([139, 197, 214]))
BaseGreen = Material("Green", Color.by_rgb([175, 193, 138]))
BaseInfra = Material("Infra", Color.by_rgb([234, 234, 234]))
BaseRoads = Material("Infra", Color.by_rgb([140, 140, 140]))

# class Materialfinish
