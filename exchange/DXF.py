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


"""This module provides import data from DXF file
"""

import sys
import ezdxf
import math
from pathlib import Path


__title__ = "DXF"
__author__ = "Maarten & Jonathan"
__url__ = "./exchange/dxf.py"


sys.path.append(str(Path(__file__).resolve().parents[2]))

from project.fileformat import *
from geometry.curve import *
from geometry.point import Point
from geometry.geometry2d import Point2D, Line2D, Arc2D, PolyCurve2D

# [!not included in BP singlefile - end]

#todo, check if polygon is not closed, then draw polycurve
class ReadDXF:
    def __init__(self, filepath):
        self.filepath = filepath
        self.points = []
        self.lines = []
        self.arcs = []
        self.polylines = []
        self.bulges = []
        self._read_dxf_file()

    def _read_dxf_file(self):
        self._read_line()
        self._read_arc()
        self._read_polyline()


    def _read_arc(self):
        arc_pieces = []
        with open(self.filepath, 'r') as file:
            lines = [line.strip() for line in file.readlines()]

        i = 0
        while i < len(lines):
            line = lines[i]
            if line == "0":
                i += 1
                continue

            if line == "ARC":
                center_x = center_y = radius = start_angle = end_angle = None
                while True:
                    i += 1
                    if i >= len(lines):
                        break

                    code = lines[i]
                    if code == "10":
                        i += 1
                        center_x = float(lines[i])*project.scale
                    elif code == "20":
                        i += 1
                        center_y = float(lines[i])*project.scale
                    elif code == "40":
                        i += 1
                        radius = float(lines[i])*project.scale
                    elif code == "50":
                        i += 1
                        start_angle = float(lines[i])*project.scale
                    elif code == "51":
                        i += 1
                        end_angle = float(lines[i])*project.scale
                    elif code == "0":
                        break

                if None not in [center_x, center_y, radius, start_angle, end_angle]:
                    start_point = Arc2D.draw_arc_point(center_x, center_y, radius, start_angle)
                    end_point = Arc2D.draw_arc_point(center_x, center_y, radius, end_angle)
                    mid_angle = (start_angle + end_angle) / 2 if end_angle > start_angle else (start_angle + end_angle + 360) / 2
                    mid_point = Arc2D.draw_arc_point(center_x, center_y, radius, mid_angle)
                    arc_object = Arc2D(start_point, mid_point, end_point)
                    arc_pieces.append(arc_object)
                    self.arcs.append(arc_object)

            i += 1

        return arc_pieces

    def _read_polyline(self):
        polyline_stukken = []
        with open(self.filepath, 'r') as file:
            lines = [line.strip() for line in file.readlines()]

        i = 0
        while i < len(lines):
            line = lines[i]
            if line == "0":
                i += 1
                continue

            if line == "LWPOLYLINE":
                points2D = []
                x, y, elevation = None, None, 0
                polyline_flag, vertex_count = 0, None
                widths = []
                bulge = None
                bulges = []
                has_arc = False

                while True:
                    i += 1
                    if i >= len(lines):
                        break

                    code = lines[i]
                    if code == "5":
                        i += 1
                        handle_id = lines[i]                     
                    elif code == "8":
                        i += 1
                        layer = lines[i]
                    elif code == "10":
                        if x is not None and y is not None:
                            points2D.append(Point2D(x, y))
                            bulge = 0
                        i += 1
                        x = float(lines[i]) * project.scale
                    elif code == "20":
                        i += 1
                        y = float(lines[i]) * project.scale
                    elif code == "38":
                        i += 1
                        elevation = float(lines[i]) * project.scale
                    elif code == "42":
                        i += 1
                        bulge = float(lines[i]) 
                    elif code == "70":
                        i += 1
                        polyline_flag = int(lines[i])
                    elif code == "90":
                        i += 1
                        vertex_count = int(lines[i])
                    elif code == "100":
                        i += 1
                        subclass_marker = lines[i]                       
                    elif code == "40":
                        i += 1
                        start_width = float(lines[i]) * project.scale
                        widths.append(start_width)
                    elif code == "41":
                        i += 1
                        end_width = float(lines[i]) * project.scale
                        widths.append(end_width)
                    elif code == "330":
                        i += 1
                        owner_id = lines[i]                     
                    elif code == "0":
                        break

                if points2D:
                    # if polyline_flag & 1 == 1:
                    polyline_object = Polygon.by_points(points2D)
                    polyline_stukken.append(polyline_object)
                    self.polylines.append(polyline_object)
                    # else:
                    #     print("Found polyline that was not closed!")


            elif line == "POLYLINE":
                points2D = []
                while True:
                    i += 1
                    if i >= len(lines):
                        break
                    code = lines[i]
                    if code == "VERTEX":
                        while True:
                            i += 1
                            if i >= len(lines):
                                break
                            vertex_code = lines[i]
                            if vertex_code == "10":
                                i += 1
                                x = float(lines[i])*project.scale
                            elif vertex_code == "20":
                                i += 1
                                y = float(lines[i])*project.scale
                                points2D.append(Point2D(x, y))
                            elif vertex_code in ["0", "SEQEND"]:
                                break
                    if code == "SEQEND":
                        break

                if points2D:
                    is_closed = True 
                    if is_closed:
                        polyline_object = Polygon.by_points(points2D)
                    # else:
                    #     polyline_object = PolyCurve2D.by_points(points2D)  # Use this for open polylines
                    polyline_stukken.append(polyline_object)
                    self.polylines.append(polyline_object)


            i += 1

        return polyline_stukken


    def _read_line(self):
        linepieces = []
        with open(self.filepath, 'r') as file:
            lines = [line.strip() for line in file.readlines()]
        
        i = 0
        while i < len(lines):
            line = lines[i]
            if line == "0":
                i += 1
                continue
            
            if line in ["LINE"]:
                x1 = y1 = x2 = y2 = None
                while True:
                    i += 1
                    if i >= len(lines):
                        break
                    
                    code = lines[i]
                    if code == "10":
                        i += 1
                        x1 = float(lines[i])*project.scale
                    elif code == "20":
                        i += 1
                        y1 = float(lines[i])*project.scale
                    elif code == "11":
                        i += 1
                        x2 = float(lines[i])*project.scale
                    elif code == "21":
                        i += 1
                        y2 = float(lines[i])*project.scale
                    elif code == "0":
                        break
                
                if None not in [x1, y1, x2, y2]:
                    start_point = Point2D(x1, y1)
                    end_point = Point2D(x2, y2)
                    linepieces.append(Line2D(start_point, end_point))
                    self.lines.append(Line2D(start_point, end_point))

            i += 1

        return linepieces
    

    def calculate_arc_midpoint(self, start, end, bulge):
        dx = end.x - start.x
        dy = end.y - start.y
        
        L = math.sqrt(dx**2 + dy**2)
        
        S = (L / 2) * bulge
        
        try:
            R = ((L / 2)**2 + S**2) / (2 * S)
        except:
            R = 0
        
        mx = (start.x + end.x) / 2
        my = (start.y + end.y) / 2
        
        if bulge > 0:
            dir_x = -dy
            dir_y = dx
        else:
            dir_x = dy
            dir_y = -dx
        
        try:
            length = math.sqrt(dir_x**2 + dir_y**2)
            dir_x /= length
            dir_y /= length
        except:
            length = 0
            dir_x = 0
            dir_y = 0
        cx = mx + dir_x * math.sqrt(R**2 - (L / 2)**2)
        cy = my + dir_y * math.sqrt(R**2 - (L / 2)**2)
        
        return Point2D(cx, cy)    