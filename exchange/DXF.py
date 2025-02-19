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
from ezdxf import readfile, DXFStructureError, DXFValueError
import math
from pathlib import Path


__title__ = "DXF"
__author__ = "Maarten & Jonathan"
__url__ = "./exchange/dxf.py"




from project.fileformat import *
from geometry.curve import *
from geometry.coords import Point
from geometry.geometry2d import Point, Line2D, Arc2D, PolyCurve2D

# [!not included in BP singlefile - end]

#todo, check if polygon is not closed, then draw polycurve
class ReadDXF:
    def __init__(self, filepath):
        self.filepath = filepath
        self.points = []     
        self.lines = []      
        self.arcs = []       
        self.polylines = []  
        self.read_dxf()

    def read_dxf(self):
        doc = ezdxf.readfile(self.filepath)
        msp = doc.modelspace()

        for entity in msp:
            dxftype = entity.dxftype()
            if dxftype == 'POINT':
                # Handle point entities
                point = Point(entity.dxf.location)
                self.points.append(point)
            elif dxftype == 'LINE':
                pass
                # Handle line entities
                # start = Point(entity.dxf.start)
                # end = Point(entity.dxf.end)
                # self.lines.append(Line2D(start, end))
            elif dxftype == 'ARC':
                center = Vector(entity.dxf.center)
                radius = entity.dxf.radius
                start_angle = entity.dxf.start_angle
                end_angle = entity.dxf.end_angle
                self.arcs.append((center, radius, start_angle, end_angle))
            elif dxftype in {'LWPOLYLINE', 'POLYLINE'}:
                try:
                    points = [Point(x, y) for x, y in entity.vertices()]
                    polygon = Polygon.by_points(points)
                    self.polylines.append((polygon, entity.dxf.layer))
                except DXFValueError as error:
                    print(f"Failed to process {entity.dxftype()} on layer {entity.dxf.layer} due to a DXF error: {str(error)}")
                except ValueError as error:
                    print(f"Data format error with {entity.dxftype()} on layer {entity.dxf.layer}: {str(error)}")
                except Exception as error:
                    print(f"An unexpected error occurred while processing an entity: {str(error)}")