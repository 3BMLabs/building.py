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


"""This module provides tools to create solids
"""

__title__ = "solid"
__author__ = "Maarten & Jonathan"
__url__ = "./objects/void.py"


import sys
from pathlib import Path

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

from geometry.solid import Extrusion

class Void(Extrusion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Void"
        self.type = "Void"
        
    @staticmethod
    def by_polycurve_height(polycurve, height, dz_loc):
        obj = Extrusion.by_polycurve_height(polycurve, height, dz_loc)
        void = Void()
        void.__dict__.update(obj.__dict__)
        void.polycurve_3d_translated = polycurve
        void.name = "Void"
        void.type = "Void"

        return void