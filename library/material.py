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


"""This module provides a library of materials
"""

__title__= "material"
__author__ = "Maarten & Jonathan"
__url__ = "./library/material.py"


import sys, os, math
from pathlib import Path
from abstract.color import *



# [!not included in BP singlefile - end]

def rgb_to_int(rgb):
    r, g, b = [max(0, min(255, c)) for c in rgb]

    return (255 << 24) | (r << 16) | (g << 8) | b

class Material:
    def __init__(self):
        self.name = "none"
        self.color = None
        self.colorint = None

    @classmethod
    def byNameColor(cls, name, color):
        M1 = Material()
        M1.name = name
        M1.color = color
        #M1.colorint = rgb_to_int(color)
        return M1

#Building Materials
BaseConcrete = Material.byNameColor("Concrete", Color().RGB([192, 192, 192]))
BaseTimber = Material.byNameColor("Timber", Color().RGB([191, 159, 116]))
BaseSteel = Material.byNameColor("Steel", Color().RGB([237, 28, 36]))
BaseOther = Material.byNameColor("Other", Color().RGB([150, 150, 150]))
BaseBrick = Material.byNameColor("Brick", Color().RGB([170, 77, 47]))
BaseBrickYellow = Material.byNameColor("BrickYellow", Color().RGB([208, 187, 147]))

#GIS Materials
BaseBuilding = Material.byNameColor("Building", Color().RGB([150, 28, 36]))
BaseWater = Material.byNameColor("Water", Color().RGB([139, 197, 214]))
BaseGreen = Material.byNameColor("Green", Color().RGB([175, 193, 138]))
BaseInfra = Material.byNameColor("Infra", Color().RGB([234, 234, 234]))
BaseRoads = Material.byNameColor("Infra", Color().RGB([140, 140, 140]))

#class Materialfinish