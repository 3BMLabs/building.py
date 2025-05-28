# [included in BP singlefile]
# [!not included in BP singlefile - start]

# -*- coding: utf8 -*-
# ***************************************************************************
# *   Copyright (c) 2024 Maarten Vroegindeweij                              *
# *   maarten@3bm.co.nl                                                     *
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


"""This module provides conversion from and to GIS2BIM to BuildingPy Objects
"""



from geometry.curve import Point, PolyCurve, Line
from geometry.linestyle import line_to_pattern

__title__ = "GIS2BIM"
__author__ = "Maarten"
__url__ = "./exchange/GIS2BIM.py"

# [!not included in BP singlefile - end]

def WFSCurvesToBPCurves(curves):
    BPyPolyCurves = []
    for i in curves:
        pointlist = []
        for j in i:
            pointlist.append(Point(j[0], j[1], 0))
        PC = PolyCurve.by_points(pointlist)
        BPyPolyCurves.append(PC)
    return BPyPolyCurves


def WFSCurvesToBPCurvesLinePattern(curves, pattern):
    Lines = []
    for i in curves:
        n = 0
        for j in range(len(i)-1):
            PntStart = Point(i[n][0], i[n][1], 0)
            n = n + 1
            PntEnd = Point(i[n][0], i[n][1], 0)
            ln = line_to_pattern(Line(PntStart, PntEnd), pattern)
            # print(ln)
            for x in ln:
                Lines.append(x)
    return Lines
