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

from project.fileformat import *
from geometry.curve import *
from geometry.point import Point
from geometry.geometry2d import Point2D, Line2D, Arc2D, PolyCurve2D
from pathlib import Path


__title__ = "DXF"
__author__ = "Maarten & Jonathan"
__url__ = "./exchange/dxf.py"


import sys
import ezdxf
import math

sys.path.append(str(Path(__file__).resolve().parents[2]))


# [!not included in BP singlefile - end]


class ReadDXF:
    def __init__(self, filepath):
        self.filepath = filepath
        self.points = []
        self.lines = []
        self.arcs = []
        self.polylines = []
        self._read_dxf_file()

    def _read_dxf_file(self):
        self._read_line()
        self._read_arc()
        self._read_polyline()


    def _read_arc(self):
        arc_stukken = []
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
                    arc_stukken.append(arc_object)
                    self.arcs.append(arc_object)

            i += 1

        return arc_stukken

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
                while True:
                    i += 1
                    if i >= len(lines):
                        break

                    code = lines[i]
                    if code == "10":
                        i += 1
                        x = float(lines[i])*project.scale
                    elif code == "20":
                        i += 1
                        y = float(lines[i])*project.scale
                        points2D.append(Point2D(x, y))
                    elif code == "0":
                        break

                if points2D:
                    polyline_object = PolyCurve2D.by_points(points2D)
                    polyline_stukken.append(polyline_object)
                    self.polylines.append(polyline_object)

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
                    polyline_object = PolyCurve2D.by_points(points2D)
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