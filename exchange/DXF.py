# [included in BP singlefile]
# [!not included in BP singlefile - start]
# -*- coding: utf8 -*-
#***************************************************************************
#*   Copyright (c) 2024 Maarten Vroegindeweij & Jonathan van der Gouwe      *
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

# [!not included in BP singlefile - end]


class ReadDXF():
    #append line only if unique start.value and end.value
    #sort them based on end.value has to be start.value
    def __init__(self, filename):
        self.points = []
        self.lines = []
        self.filename = filename
        self.get_line_coordinates()
        self.polycurve = self.create_polycurve()
        self.isClosed = project.closed


    def convert_coordinates(self, start_point, end_point, reference_point):
        
        # relative_start = start_point - reference_point
        # print(start_point, end_point, reference_point)
        relative_start = start_point[0] - reference_point[0], start_point[1] - reference_point[1], start_point[2] - reference_point[2]
        # print(relative_start)
        # print(end_point, reference_point)
        relative_end = end_point[0] - reference_point[0], end_point[1] - reference_point[1], end_point[2] - reference_point[2]
        # relative_end = end_point - reference_point
        # print(relative_end)
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
                self.lines.append(line)


            elif entity.dxftype() == 'LWPOLYLINE':
                splittedpoints = []
                splittedlines = []
                with entity.points() as points:
                    endpoint = None
                    for point in points:
                        if reference_point is None:
                            reference_point = point
                        if endpoint is None:
                            endpoint = point
                        point = point[0], point[1], point[2]
                        endpoint = endpoint[0], endpoint[1], endpoint[2]
                        reference_point = reference_point[0], reference_point[1], reference_point[2]
                        relative_start, relative_end = self.convert_coordinates(point, endpoint, reference_point)
                        p1 = Point(x=relative_start[0], y=relative_start[1], z=relative_start[2])
                        p2 = Point(x=relative_end[0], y=relative_end[1], z=relative_end[2]) 
                        line = Line(start=p1, end=p2)
                        splittedpoints.append(p1)
                        splittedlines.append(line)
                    self.points.append(splittedpoints)
                    self.lines.append(splittedlines)
        # print(self.lines)
        return self.lines

    
    def create_polycurve(self):
        if len(self.points) == 1:
            return PolyCurve.by_points(self.points)
        elif len(self.points) > 1:
            plList = []
            for pl in self.points:
                plList.append(PolyCurve.by_points(pl))
            return plList