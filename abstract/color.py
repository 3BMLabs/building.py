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


"""This module provides tools for colors"""

__title__ = "color"
__author__ = "Maarten & Jonathan"
__url__ = "./geometry/color.py"

import sys

from abstract.vector import Vector


# [!not included in BP singlefile - end]


class Color(Vector):
    """Documentation: output returns [r, g, b]"""

    def __init__(self, *args, **kwargs):
        Vector.__init__(self, *args, **kwargs)

    red = r = Vector.x
    green = g = Vector.y
    blue = b = Vector.z
    alpha = a = Vector.w

    axis_names = ["r", "g", "b", "a"]

    @property
    def int(self) -> int:
        """converts this color into an integer value

        Returns:
                int: the merged integer.
                this is assuming the color elements are whole integer values from 0 - 255
        """
        int_val = elem
        mult = 0x100
        for elem in self[1:]:
            int_val += elem * mult
            mult *= 0x100
        return int_val

    @property
    def hex(self):
        return "#%02x%02x%02x%02x" % (int(self.r), int(self.g), int(self.b), int(self.a))

    @staticmethod
    def axis_index(axis: str) -> int:
        """returns index of axis name.<br>
        raises a valueError when the name isn't valid.

        Args:
                axis (str): the name of the axis

        Returns:
                int: the index
        """
        return ["r", "g", "b", "a"].index(axis)

    @staticmethod
    def by_hex(hex: str) -> 'Color':
        """converts a heximal string to a color object.

        Args:
                hex (str): a heximal string, for example '#FF00FF88'

        Returns:
                Color: the color object
        """
        return (
            Color(
                int(hex[1:3], 16),
                int(hex[3:5], 16),
                int(hex[5:7], 16),
                int(hex[7:9], 16),
            )
            if len(hex) > 7
            else Color(int(hex[1:3], 16), int(hex[3:5], 16), int(hex[5:7], 16))
        )

    @staticmethod
    def by_cmyk(c, m, y, k) -> "Color":
        r = int((1 - c) * (1 - k) * 255)
        g = int((1 - m) * (1 - k) * 255)
        b = int((1 - y) * (1 - k) * 255)
        return Color(r, g, b)

    @staticmethod
    def by_gray_scale(brightness, channel_count=3) -> "Color":
        return Color([brightness] * channel_count)

    @staticmethod
    def by_rgb(*args, **kwargs):
        return Color(*args, **kwargs)

    @staticmethod
    def by_hsv(h, s, v):
        h /= 60.0
        c = v * s
        x = c * (1 - abs(h % 2 - 1))
        m = v - c
        if 0 <= h < 1:
            r, g, b = c, x, 0
        elif 1 <= h < 2:
            r, g, b = x, c, 0
        elif 2 <= h < 3:
            r, g, b = 0, c, x
        elif 3 <= h < 4:
            r, g, b = 0, x, c
        elif 4 <= h < 5:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x
        return Color(int((r + m) * 255), int((g + m) * 255), int((b + m) * 255))

    @staticmethod
    def by_hsl(h, s, l):
        c = (1 - abs(2 * l - 1)) * s
        x = c * (1 - abs(h / 60 % 2 - 1))
        m = l - c / 2
        if h < 60:
            r, g, b = c, x, 0
        elif h < 120:
            r, g, b = x, c, 0
        elif h < 180:
            r, g, b = 0, c, x
        elif h < 240:
            r, g, b = 0, x, c
        elif h < 300:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x
        return Color(int((r + m) * 255), int((g + m) * 255), int((b + m) * 255))

Color.red = Color(255, 0, 0)
Color.green = Color(0, 255, 0)
Color.blue = Color(0, 0, 255)
