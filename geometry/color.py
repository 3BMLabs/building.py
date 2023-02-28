# -*- coding: utf8 -*-
#***************************************************************************
#*   Copyright (c) 2023 Maarten Vroegindeweij & Jonathan van der Gouwe      *
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


"""This module provides tools for colors
"""

__title__= "color"
__author__ = "Maarten & Jonathan"
__url__ = "./geometry/color.py"


import sys, os, math
from pathlib import Path

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

import sys

class Color:
	"""Documentation: output returns [r, g, b]"""

	def __init__(self, colorInput=None):
		self.colorInput = colorInput
	

	red = [255,0,0]
	green = [0,255,0]
	blue = [0,0,255]


	def Components(self, colorInput=None):
		"""1"""
		if colorInput is None:
			return f"Error: Example usage Color().{sys._getframe(0).f_code.co_name}('green')"
		else:
			try:
				import json
				JSONfile = "colorComponents.json"
				with open(JSONfile,'r') as file:
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
			#validate if value is correct/found
			try:
				colorInput = colorInput.lstrip('#')
				return list(int(colorInput[i:i+2], 16) for i in (0, 2, 4))
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
				#add check help attribute
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
				r, g, b = int((r + m) * 255), int((g + m) * 255), int((b + m) * 255)
				return [r, g, b]
			except:
				return f"Error: Color {sys._getframe(0).f_code.co_name} attribute usage is incorrect. Documentation: Color().{sys._getframe(0).f_code.co_name}.__doc__"


	def RAL(self, colorInput=None):
		"""NAN"""
		if colorInput is None:
			return f"Error: Example usage Color().{sys._getframe(0).f_code.co_name}(1000)"
		else:
			try:
			#validate if value is correct/found
				import json
				JSONfile = "colorRAL.json"
				with open(JSONfile,'r') as file:
					ral_dict = json.load(file)
					checkExist = ral_dict.get(str(colorInput))
					if checkExist is not None:
						r, g, b = ral_dict[str(colorInput)]["rgb"].split("-")
						return [int(r), int(g), int(b)]
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
				JSONfile = "colorPantone.json"
				with open(JSONfile,'r') as file:
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
		colorattributes = ["Components", "Hex", "CMYK", "Alpha", "Brightness", "RGB", "HSV", "HSL", "RAL", "Pantone", "LRV"]
		if colorInput is None:
			header = "Available attributes: \n"
			footer = "\nColor().red | Color().green | Color().blue"
			return header + '\n'.join([f"Color().{func}()" for func in colorattributes]) + footer
		return f"Color().{colorInput}"


	def Info(self, colorInput=None):
		pass


c = Color()
# print(c) #available attributes

# print(c.red)
# print(c.green)
# print(c.blue)

# print(c.Components.__doc__) #documentation
# print(c.Components()) #no value | Error: missing value.
# print(c.Components('test')) #incorrect value
# print(c.Components('red')) #correct value

# print(c.Hex.__doc__) #documentation
# print(c.Hex()) #no value
# print(c.Hex('.')) #incorrect value
# print(c.Hex('#ff2ba4')) #correct value

# print(c.CMYK.__doc__) #documentation
# print(c.CMYK()) #no value
# print(c.CMYK('.')) #incorrect value
# print(c.CMYK([0.5, 0.25, 0, 0.2])) #correct value

# print(c.Alpha.__doc__) #documentation
# print(c.Alpha()) #no value
# print(c.Alpha('.')) #incorrect value
# print(c.Alpha([255, 0, 0, 128])) #correct value

# print(c.Brightness.__doc__) #documentation
# print(c.Brightness()) #no value
# print(c.Brightness('.')) #incorrect value
# print(c.Brightness(0.03)) #correct value

# print(c.RGB.__doc__) #documentation
# print(c.RGB()) #no value
# print(c.RGB('.')) #incorrect value
# print(c.RGB([255, 0, 0])) #correct value

# print(c.HSV.__doc__) #documentation
# print(c.HSV()) #no value
# print(c.HSV('.')) #incorrect value
# print(c.HSV([120, 0.5, 0.8])) #correct value

# print(c.HSL.__doc__) #documentation
# print(c.HSL()) #no value
# print(c.HSL('.')) #incorrect value
# print(c.HSL([120, 0.5, 0.8])) #correct value

# print(c.RAL.__doc__) #documentation
# print(c.RAL()) #no value
# print(c.RAL('.')) #incorrect value
# print(c.RAL(1002)) #correct value

# print(c.Pantone.__doc__) #documentation
# print(c.Pantone()) #no value
# print(c.Pantone('.')) #incorrect value
# print(c.Pantone('19-5232')) #correct value

# print(c.LRV.__doc__) #documentation
# print(c.LRV()) #no value
# print(c.LRV('.')) #incorrect value
# print(c.LRV(237)) #correct value -> value between 236.6 and 255


#RGB / RBG / BRG / BGR / GRB / GBR
