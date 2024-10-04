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

"""This module provides tools for analytical element like supports, loads
"""

__title__ = "annotation"
__author__ = "Maarten & Jonathan"
__url__ = "./objects/annotation.py"

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from geometry.curve import *

class View:
    def __init__(self):
        self.name = None
        self.id = generateID()
        self.type = __class__.__name__
        self.origin = Point(0, 0, 0)
        self.cutplane: CoordinateSystem = None
        self.visibility = None
        self.scale = 0.01

    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
            'type': self.type,
            'origin': self.origin.serialize(),
            'cutplane': self.cutplane.serialize() if self.cutplane else None,
            'visibility': self.visibility,
            'scale': self.scale
        }

    @staticmethod
    def deserialize(data):
        view = View()
        view.name = data.get('name')
        view.id = data.get('id')
        view.type = data.get('type')
        view.origin = Point.deserialize(data['origin'])
        view.cutplane = CoordinateSystem.deserialize(
            data['cutplane']) if data.get('cutplane') else None
        view.visibility = data.get('visibility')
        view.scale = data.get('scale', 0.01)

        return view


class Visibility:
    def __init__(self):
        self.name = None
        self.id = generateID()
        self.type = __class__.__name__
        self.origin = Point(0, 0, 0)
        self.cutplane: CoordinateSystem = None
        self.visibility = None
        self.scale = 0.01

    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
            'type': self.type,
            'origin': self.origin.serialize(),
            'cutplane': self.cutplane.serialize() if self.cutplane else None,
            'visibility': self.visibility,
            'scale': self.scale
        }

    @staticmethod
    def deserialize(data):
        visibility = Visibility()
        visibility.name = data.get('name')
        visibility.id = data.get('id')
        visibility.type = data.get('type')
        visibility.origin = Point.deserialize(data['origin'])
        visibility.cutplane = CoordinateSystem.deserialize(
            data['cutplane']) if data.get('cutplane') else None
        visibility.visibility = data.get('visibility')
        visibility.scale = data.get('scale', 0.01)

        return visibility
