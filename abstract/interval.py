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


"""This module provides tools for intervales
"""

__title__ = "interval"
__author__ = "Maarten & Jonathan"
__url__ = "./abstract/interval.py"

import sys
from pathlib import Path
from typing import Any, List

sys.path.append(str(Path(__file__).resolve().parents[1]))

from geometry.point import Point as pnt
from abstract.vector import *

# [!not included in BP singlefile - end]


class Interval:
    def __init__(self, start: float, end: float):
        self.start = start
        self.end = end
        self.interval = None

    def serialize(self):
        return {
            'start': self.start,
            'end': self.end,
            'interval': self.interval
        }

    @staticmethod
    def deserialize(data):
        start = data.get('start')
        end = data.get('end')
        interval = Interval(start, end)
        interval.interval = data.get('interval')
        return interval

    @classmethod
    def by_start_end_count(self, start: float, end: float, count: int):
        intval = []
        numb = start
        delta = end-start
        for i in range(count):
            intval.append(numb)
            numb = numb + (delta / (count - 1))
        self.interval = intval
        return self

    def __str__(self):
        return f"{__class__.__name__}"
