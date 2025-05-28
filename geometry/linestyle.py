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


"""This module provides tools to create linestyles and patterns
"""

__title__ = "linestyle"
__author__ = "Maarten & Jonathan"
__url__ = "./geometry/linestyle.py"


import math
import sys

from abstract.vector import Point, Vector
from geometry.curve import Line, PolyCurve





# [!not included in BP singlefile - end]

# Rule: line, whitespace, line whitespace etc., scale
HiddenLine1 = ["Hidden Line 1", [1, 1], 100]
# Rule: line, whitespace, line whitespace etc., scale
HiddenLine2 = ["Hidden Line 2", [2, 1], 100]
# Rule: line, whitespace, line whitespace etc., scale
Centerline = ["Center Line 1", [8, 2, 2, 2], 100]


def line_to_pattern(baseline: 'Line', pattern_obj) -> 'list':
	"""Converts a baseline (Line object) into a list of line segments based on a specified pattern.
	This function takes a line (defined by its start and end points) and a pattern object. The pattern object defines a repeating sequence of segments to be applied along the baseline. The function calculates the segments according to the pattern and returns a list of Line objects representing these segments.

	#### Parameters:
	- `baseline` (Line): The baseline along which the pattern is to be applied. This line is defined by its start and end points.
	- `pattern_obj` (Pattern): The pattern object defining the sequence of segments. The pattern object should have the following structure:
		- An integer representing the number of repetitions.
		- A list of floats representing the lengths of each segment in the pattern.
		- A float representing the scale factor for the lengths of the segments in the pattern.

	#### Returns:
	`list`: A list of Line objects that represent the line segments created according to the pattern along the baseline.

	#### Example usage:
	```python
	baseline = Line(Point(0, 0, 0), Point(10, 0, 0))
	pattern_obj = (3, [2, 1], 1)  # 3 repetitions, pattern of lengths 2 and 1, scale factor 1
	patterned_lines = line_to_pattern(baseline, pattern_obj)
	# patterned_lines will be a list of Line objects according to the pattern
	```

	The function works by calculating the total length of the pattern, the number of whole lengths of the pattern that fit into the baseline, and then generating the line segments according to these calculations. If the end of the baseline is reached before completing a pattern sequence, the last segment is adjusted to end at the baseline's end point.
	"""
	# this converts a line to list of lines based on a pattern
	origin = baseline.start
	dir = Vector.by_two_points(baseline.start, baseline.end)
	unityvect = dir.normalized

	Pattern = pattern_obj
	l = baseline.length
	patternlength = sum(Pattern[1]) * Pattern[2]
	# number of whole lengths of the pattern
	count = math.floor(l / patternlength)
	lines = []

	startpoint = origin
	ll = 0
	rl = 10000
	for i in range(count + 1):
		n = 0
		for i in Pattern[1]:
			deltaV = unityvect * (i * Pattern[2])
			dl = deltaV.length
			if rl < dl:  # this is the last line segment on the line where the pattern is going to be cut into pieces.
				endpoint = baseline.end
			else:
				endpoint = Point.translate(startpoint, deltaV)
			if n % 2:
				a = 1 + 1
			else:
				lines.append(Line(start=startpoint, end=endpoint))
			if rl < dl:
				break  # end of line reached
			startpoint = endpoint
			n = n + 1
			ll = ll + dl  # total length
			rl = l - ll  # remaining length within the pattern
		startpoint = startpoint
	return lines

def polycurve_to_pattern(polycurve: 'PolyCurve', pattern_obj) -> 'list':
	res = []
	for i in polycurve.curves:
		res.append(line_to_pattern(i,pattern_obj))
	return res