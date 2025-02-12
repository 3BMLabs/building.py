# [included in BP singlefile]
# [!not included in BP singlefile - start]
# -*- coding: utf8 -*-
#***************************************************************************
#*   Copyright (c) 2024 Maarten Vroegindeweij & Jonathan van der Gouwe	  *
#*   maarten@3bm.co.nl & jonathan@3bm.co.nl								*
#*																		 *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)	*
#*   as published by the Free Software Foundation; either version 2 of	 *
#*   the License, or (at your option) any later version.				   *
#*   for detail see the LICENCE text file.								 *
#*																		 *
#*   This program is distributed in the hope that it will be useful,	   *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of		*
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the		 *
#*   GNU Library General Public License for more details.				  *
#*																		 *
#*   You should have received a copy of the GNU Library General Public	 *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA																   *
#*																		 *
#***************************************************************************


"""This module provides tools to get profiledata from the database. These are json files
"""

__title__= "profile"
__author__ = "Maarten & Jonathan"
__url__ = "./objects/profile.py"

import math
import sys
from pathlib import Path
import urllib.request
import json
import re

file = Path(__file__).resolve()
package_root_directory = file.parents[2]
sys.path.append(str(package_root_directory))

from abstract.vector import Vector
from construction.profile import CChannelParallelFlange, CChannelSlopedFlange, IShapeParallelFlange, LAngle, Rectangle, RectangleHollowSection, Round, Roundtube, TProfileRounded
from geometry.curve import PolyCurve
from abstract.segmentation import SegmentationSettings

# [!not included in BP singlefile - end]
jsonFile = "https://raw.githubusercontent.com/3BMLabs/Project-Ocondat/master/steelprofile.json"
url = urllib.request.urlopen(jsonFile)
data = json.loads(url.read())


def is_rectangle_format(shape_name):
	match = re.match(r'^(\d{1,4})x(\d{1,4})$', shape_name)
	if match:
		width, height = int(match.group(1)), int(match.group(2))
		if 0 <= width <= 10000 and 0 <= height <= 10000:
			return True, width, height
	return False, 0, 0


class _getProfileDataFromDatabase:
	def __init__(self, name):
		self.name = name
		self.shape_coords = None
		self.shape_name = None
		self.synonyms = None
		for item in data:
			for i in item.values():
				synonymList = i[0]["synonyms"]
				if self.name.lower() in [synonym.lower() for synonym in synonymList]:
					self.shape_coords = i[0]["shape_coords"]
					self.shape_name = i[0]["shape_name"]
					self.synonyms = i[0]["synonyms"]
		if self.shape_coords == None:
			check_rect, width, height = is_rectangle_format(name)
			if check_rect:
				self.shape_coords = [width, height]
				self.shape_name = "Rectangle"
				self.synonyms = name


class nameToProfile:
	def __init__(self, name1, segmented = True):
		profile_data = _getProfileDataFromDatabase(name1)
		if profile_data == None:
			print(f"profile {name1} not recognised")
		profile_name = profile_data.shape_name
		if profile_name == None:
			structural_fallback_element = "HEA100"
			profile_data = _getProfileDataFromDatabase(structural_fallback_element)
			print(f"Error, profile '{name1}' not recognised, define in {jsonFile} | fallback: '{structural_fallback_element}'")
			profile_name = profile_data.shape_name
		self.profile_data = profile_data
		self.profile_name = profile_name
		name = profile_data.name
		self.d1 = profile_data.shape_coords
		d1 = self.d1
		if profile_name == "C-channel parallel flange":
			profile = CChannelParallelFlange(name,d1[0],d1[1],d1[2],d1[3],d1[4],d1[5])
		elif profile_name == "C-channel sloped flange":
			profile = CChannelSlopedFlange(name,d1[0],d1[1],d1[2],d1[3],d1[4],d1[5],d1[6],d1[7],d1[8])
		elif profile_name == "I-shape parallel flange":
			profile = IShapeParallelFlange(name,d1[0],d1[1],d1[2],d1[3],d1[4])
		elif profile_name == "I-shape sloped flange":
			profile = IShapeParallelFlange(name, d1[0], d1[1], d1[2], d1[3], d1[4])
			#Todo: add sloped flange shape
		elif profile_name == "Rectangle":
			profile = Rectangle(name,d1[0], d1[1])
		elif profile_name == "Round":
			profile = Round(name, d1[1])
		elif profile_name == "Round tube profile":
			profile = Roundtube(name, d1[0], d1[1])
		elif profile_name == "LAngle":
			profile = LAngle(name,d1[0],d1[1],d1[2],d1[3],d1[4],d1[5],d1[6],d1[7])
		elif profile_name == "TProfile":
			profile = TProfileRounded(name, d1[0], d1[1], d1[2], d1[3], d1[4], d1[5], d1[6], d1[7], d1[8])
		elif profile_name == "Rectangle Hollow Section":
			profile = RectangleHollowSection(name,d1[0],d1[1],d1[2],d1[3],d1[4])
		self.profile = profile
		self.data = d1
		final_curve = self.profile.curve  # 2D polycurve
		if segmented == True:
			final_curve = PolyCurve.segmentate(self.profile.curve, SegmentationSettings(max_angle = math.pi / 4))
		self.polycurve2d = final_curve

def justificationToVector(plycrv2D: PolyCurve, XJustifiction, Yjustification, ey=None, ez=None):

	# print(XJustifiction)
	xval = []
	yval = []
	for i in plycrv2D.curves:
		xval.append(i.start.x)
		yval.append(i.start.y)

	#Rect
	xmin = min(xval)
	xmax = max(xval)
	ymin = min(yval)
	ymax = max(yval)

	b = xmax-xmin
	h = ymax-ymin

	# print(b, h)

	dxleft = -xmax
	dxright = -xmin
	dxcenter = dxleft - 0.5 * b #CHECK
	dxorigin = 0

	dytop = -ymax
	dybottom = -ymin
	dycenter = dytop - 0.5 * h #CHECK
	dyorigin = 0

	if XJustifiction == "center":
		dx = dxorigin #TODO
	elif XJustifiction == "left":
		dx = dxleft
	elif XJustifiction == "right":  
		dx = dxright
	elif XJustifiction == "origin":
		dx = dxorigin #TODO
	else:
		dx = 0

	if Yjustification == "center":
		dy = dyorigin   #TODO
	elif Yjustification == "top":
		dy = dytop
	elif Yjustification == "bottom":
		dy = dybottom
	elif Yjustification == "origin":
		dy = dyorigin #TODO
	else:
		dy = 0

	# print(dx, dy)
	v1 = Vector(dx, dy)
	# v1 = Vector2(0, 0)

	return v1