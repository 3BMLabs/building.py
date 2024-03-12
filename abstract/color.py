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


"""This module provides tools for colors
"""

__title__ = "color"
__author__ = "Maarten & Jonathan"
__url__ = "./geometry/color.py"

import sys
from pathlib import Path

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

# [!not included in BP singlefile - end]


class Color:
    """Documentation: output returns [r, g, b]"""

    def __init__(self, colorInput=None):
        self.colorInput = colorInput

    red = [255, 0, 0]
    green = [0, 255, 0]
    blue = [0, 0, 255]

    def Components(self, colorInput=None):
        """1"""
        if colorInput is None:
            return f"Error: Example usage Color().{sys._getframe(0).f_code.co_name}('green')"
        else:
            try:
                import json
                JSONfile = "library/color/colorComponents.json"
                with open(JSONfile, 'r') as file:
                    components_dict = json.load(file)
                    checkExist = components_dict.get(str(colorInput))
                    if checkExist is not None:
                        r, g, b, a = components_dict[colorInput]
                        return [r, g, b]
                    else:
                        return f"Invalid {sys._getframe(0).f_code.co_name}-color, check '{JSONfile}' for available {sys._getframe(0).f_code.co_name}-colors."
            except:
                return f"Error: Color {sys._getframe(0).f_code.co_name} attribute usage is incorrect. Documentation: Color().{sys._getframe(0).f_code.co_name}.__doc__"

    def Hex(self, colorInput=None):
        """NAN"""
        if colorInput is None:
            return f"Error: Example usage Color().{sys._getframe(0).f_code.co_name}('#2ba4ff')"
        else:
            # validate if value is correct/found
            try:
                colorInput = colorInput.split("#")[1]
                rgb_color = list(int(colorInput[i:i+2], 16) for i in (1, 3, 5))
                return [rgb_color[0], rgb_color[1], rgb_color[2], 255]

                # colorInput = colorInput.lstrip('#')
                # return list(int(colorInput[i:i+2], 16) for i in (0, 2, 4))
            except:
                return f"Error: Color {sys._getframe(0).f_code.co_name} attribute usage is incorrect. Documentation: Color().{sys._getframe(0).f_code.co_name}.__doc__"

    def rgba_to_hex(self, colorInput=None):
        """NAN"""
        if colorInput is None:
            return f"Error: Example usage Color().{sys._getframe(0).f_code.co_name}('#2ba4ff')"
        else:
            # validate if value is correct/found
            try:
                red_i = int(colorInput[0] * 255)
                green_i = int(colorInput[1] * 255)
                blue_i = int(colorInput[2] * 255)
                alpha_i = int(colorInput[3] * 255)

                red_hex = hex(red_i)[2:].zfill(2)
                green_hex = hex(green_i)[2:].zfill(2)
                blue_hex = hex(blue_i)[2:].zfill(2)
                alpha_hex = hex(alpha_i)[2:].zfill(2)

                colorInput = "#" + red_hex + green_hex + blue_hex + alpha_hex

                return colorInput.upper()

            except:
                return f"Error: Color {sys._getframe(0).f_code.co_name} attribute usage is incorrect. Documentation: Color().{sys._getframe(0).f_code.co_name}.__doc__"

    def hex_to_rgba(self, colorInput=None):
        """NAN"""
        if colorInput is None:
            return f"Error: Example usage Color().{sys._getframe(0).f_code.co_name}('#2ba4ff')"
        else:
            # validate if value is correct/found
            try:
                colorInput = colorInput.lstrip('#')
                red_int = int(colorInput[0:2], 16)
                green_int = int(colorInput[2:4], 16)
                blue_int = int(colorInput[4:6], 16)

                if len(colorInput) == 8:
                    alpha_int = int(colorInput[6:8], 16)
                    alpha = round(alpha_int / 255, 2)
                else:
                    alpha = 1.0

                red = round(red_int / 255, 2)
                green = round(green_int / 255, 2)
                blue = round(blue_int / 255, 2)

                return [red, green, blue, alpha]

            except:
                return f"Error: Color {sys._getframe(0).f_code.co_name} attribute usage is incorrect. Documentation: Color().{sys._getframe(0).f_code.co_name}.__doc__"

    def CMYK(self, colorInput=None):
        """NAN"""
        if colorInput is None:
            return f"Error: Example usage Color().CMYK([0.5, 0.25, 0, 0.2])"
        else:
            try:
                c, m, y, k = colorInput
                r = int((1-c) * (1-k) * 255)
                g = int((1-m) * (1-k) * 255)
                b = int((1-y) * (1-k) * 255)
                return [r, g, b]
            except:
                # add check help attribute
                return f"Error: Color {sys._getframe(0).f_code.co_name} attribute usage is incorrect. Documentation: Color().{sys._getframe(0).f_code.co_name}.__doc__"

    def Alpha(self, colorInput=None):
        """NAN"""
        if colorInput is None:
            return f"Error: Example usage Color().{sys._getframe(0).f_code.co_name}([255, 0, 0, 128])"
        else:
            try:
                r, g, b, a = colorInput
                return [r, g, b]
            except:
                return f"Error: Color {sys._getframe(0).f_code.co_name} attribute usage is incorrect. Documentation: Color().{sys._getframe(0).f_code.co_name}.__doc__"

    def Brightness(self, colorInput=None):
        """Expected value is int(0) - int(1)"""
        if colorInput is None:
            return f"Error: Example usage Color().{sys._getframe(0).f_code.co_name}([255, 0, 0, 128])"
        else:
            try:
                if colorInput >= 0 and colorInput <= 1:
                    r = g = b = int(255 * colorInput)
                    return [r, g, b]
                else:
                    return f"Error: Color {sys._getframe(0).f_code.co_name} attribute usage is incorrect. Documentation: Color().{sys._getframe(0).f_code.co_name}.__doc__"
            except:
                return f"Error: Color {sys._getframe(0).f_code.co_name} attribute usage is incorrect. Documentation: Color().{sys._getframe(0).f_code.co_name}.__doc__"

    def RGB(self, colorInput=None):
        """NAN"""
        if colorInput is None:
            return f"Error: Example usage Color().{sys._getframe(0).f_code.co_name}([255, 0, 0])"
        else:
            try:
                r, g, b = colorInput
                return [r, g, b]
            except:
                return f"Error: Color {sys._getframe(0).f_code.co_name} attribute usage is incorrect. Documentation: Color().{sys._getframe(0).f_code.co_name}.__doc__"

    def HSV(self, colorInput=None):
        """NAN"""
        if colorInput is None:
            return f"Error: Example usage Color().{sys._getframe(0).f_code.co_name}()"
        else:
            try:
                h, s, v = colorInput
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
                return [int((r + m) * 255), int((g + m) * 255), int((b + m) * 255)]
            except:
                return f"Error: Color {sys._getframe(0).f_code.co_name} attribute usage is incorrect. Documentation: Color().{sys._getframe(0).f_code.co_name}.__doc__"

    def HSL(self, colorInput=None):
        """NAN"""
        if colorInput is None:
            return f"Error: Example usage Color().{sys._getframe(0).f_code.co_name}()"
        else:
            try:
                h, s, l = colorInput
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
                r, g, b = int((r + m) * 255), int((g + m)
                                                  * 255), int((b + m) * 255)
                return [r, g, b]
            except:
                return f"Error: Color {sys._getframe(0).f_code.co_name} attribute usage is incorrect. Documentation: Color().{sys._getframe(0).f_code.co_name}.__doc__"

    def RAL(self, colorInput=None):
        """NAN"""
        if colorInput is None:
            return f"Error: Example usage Color().{sys._getframe(0).f_code.co_name}(1000)"
        else:
            try:
                # validate if value is correct/found
                import json
                JSONfile = "library/color/colorRAL.json"
                with open(JSONfile, 'r') as file:
                    ral_dict = json.load(file)
                    checkExist = ral_dict.get(str(colorInput))
                    if checkExist is not None:
                        r, g, b = ral_dict[str(colorInput)]["rgb"].split("-")
                        return [int(r), int(g), int(b), 100]
                    else:
                        return f"Invalid {sys._getframe(0).f_code.co_name}-color, check '{JSONfile}' for available {sys._getframe(0).f_code.co_name}-colors."
            except:
                return f"Error: Color {sys._getframe(0).f_code.co_name} attribute usage is incorrect. Documentation: Color().{sys._getframe(0).f_code.co_name}.__doc__"

    def Pantone(self, colorInput=None):
        """NAN"""
        if colorInput is None:
            return f"Error: Example usage Color().{sys._getframe(0).f_code.co_name}()"
        else:
            try:
                import json
                JSONfile = "library/color/colorPantone.json"
                with open(JSONfile, 'r') as file:
                    pantone_dict = json.load(file)
                    checkExist = pantone_dict.get(str(colorInput))
                    if checkExist is not None:
                        PantoneHex = pantone_dict[str(colorInput)]['hex']
                        return Color().Hex(PantoneHex)
                    else:
                        return f"Invalid {sys._getframe(0).f_code.co_name}-color, check '{JSONfile}' for available {sys._getframe(0).f_code.co_name}-colors."
            except:
                return f"Error: Color {sys._getframe(0).f_code.co_name} attribute usage is incorrect. Documentation: Color().{sys._getframe(0).f_code.co_name}.__doc__"

    def LRV(self, colorInput=None):
        """NAN"""
        if colorInput is None:
            return f"Error: Example usage Color().{sys._getframe(0).f_code.co_name}()"
        else:
            try:
                b = (colorInput - 0.2126 * 255 - 0.7152 * 255) / 0.0722
                b = int(max(0, min(255, b)))
                return [255, 255, b]
            except:
                return f"Error: Color {sys._getframe(0).f_code.co_name} attribute usage is incorrect. Documentation: Color().{sys._getframe(0).f_code.co_name}.__doc__"

    def rgb_to_int(rgb):
        r, g, b = [max(0, min(255, c)) for c in rgb]
        return (255 << 24) | (r << 16) | (g << 8) | b

    def __str__(self, colorInput=None):
        colorattributes = ["Components", "Hex", "rgba_to_hex", "hex_to_rgba", "CMYK",
                           "Alpha", "Brightness", "RGB", "HSV", "HSL", "RAL", "Pantone", "LRV"]
        if colorInput is None:
            header = "Available attributes: \n"
            footer = "\nColor().red | Color().green | Color().blue"
            return header + '\n'.join([f"Color().{func}()" for func in colorattributes]) + footer
        return f"Color().{colorInput}"

    def Info(self, colorInput=None):
        pass
