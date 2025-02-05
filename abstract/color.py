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

from geometry.coords import Coords



# [!not included in BP singlefile - end]


class Color(Coords):
	"""Documentation: output returns [r, g, b]"""

	def __init__(self, *args, **kwargs):
		Coords.__init__(self, *args,**kwargs)
	
	red = r = Coords.x
	green = g = Coords.y
	blue = b = Coords.z
	alpha = a = Coords.w
	
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
		return '#%02x%02x%02x%02x' % (self.r,self.g,self.b,self.a)
		
	@staticmethod
	def axis_index(axis:str) -> int:
		"""returns index of axis name.<br>
		raises a valueError when the name isn't valid.

		Args:
			axis (str): the name of the axis

		Returns:
			int: the index
		"""
		return ['r', 'g', 'b', 'a'].index(axis)

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
			
	@staticmethod
	def Hex(hex:str) -> 'Color':
		"""converts a heximal string to a color object.

		Args:
			hex (str): a heximal string, for example '#FF00FF88'

		Returns:
			Color: the color object
		"""
		return Color(int(hex[1:3], 16),int(hex[3:5], 16), int(hex[5:7], 16),int(hex[7:9], 16)) if len(hex) > 7 else Color(int(hex[1:3], 16),int(hex[3:5], 16), int(hex[5:7], 16))

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
			
	@staticmethod
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

Color.red = Color(255, 0, 0)
Color.green = Color(0, 255, 0)
Color.blue = Color(0, 0, 255)