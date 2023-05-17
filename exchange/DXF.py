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


"""This module provides import data from DXF file
"""

__title__= "DXF"
__author__ = "Maarten & Jonathan"
__url__ = "./exchange/dxf.py"


import sys, ezdxf
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from geometry.point import Point
from geometry.curve import *
from project.fileformat import *


class ReadDXF():
    #append line only if unique start.value and end.value
    #sort them based on end.value has to be start.value
    def __init__(self, filename):
        self.points = []
        self.lines = []
        self.filename = filename
        self.get_line_coordinates()
        self.polycurve = self.create_polycurve()
        self.isClosed = self.polycurve.isClosed


    def convert_coordinates(self, start_point, end_point, reference_point):
        relative_start = start_point - reference_point
        relative_end = end_point - reference_point
        relative_start = round(relative_start[0], project.decimals), round(relative_start[1], project.decimals), round(relative_start[2], project.decimals)
        relative_end = round(relative_end[0], project.decimals), round(relative_end[1], project.decimals), round(relative_end[2], project.decimals)
        return relative_start, relative_end


    def get_line_coordinates(self):
        doc = ezdxf.readfile(self.filename)
        modelspace = doc.modelspace()
        reference_point = None
        for entity in modelspace:
            if entity.dxftype() == 'LINE':
                start_point = entity.dxf.start
                end_point = entity.dxf.end
                if reference_point is None:
                    reference_point = start_point
                relative_start, relative_end = self.convert_coordinates(start_point, end_point, reference_point)
                p1 = Point(x=relative_start[0], y=relative_start[1], z=relative_start[2])
                p2 = Point(x=relative_end[0], y=relative_end[1], z=relative_end[2]) 
                line = Line(start=p1, end=p2)
                self.points.append(p1)
                # self.points.append(p2)
                self.lines.append(line)
        return self.lines


    def create_polycurve(self):
        return PolyCurve.byPoints(self.points)