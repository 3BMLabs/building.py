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


"""This module provides tools grids, levels and other datums
"""

__title__= "datum"
__author__ = "Maarten & Jonathan"
__url__ = "./objects/datum.py"

from geometry.linestyle import *

seqChar = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z AA AB AC"
seqNumber = "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24"

class Grid:
    def __init__(self):
        self.line = None
        self.name = None
        self.bulbStart = 1
        self.bulbEnd = 1

    @classmethod
    def byStartpointEndpoint(cls, line, name):
        #Create panel by polycurve
        g1 = Grid()
        g1.name = name
        g1.line = lineToPattern(line, Centerline)
        return g1

def getGridDistances(Grids):
    #Function to create grids from the format 0, 4x5400, 4000, 4000 to absolute XYZ-values
    GridsNew = []
    GridsNew.append(0)
    distance = 0.0
    #GridsNew.append(distance)
    for i in Grids:
        #del Grids[0]
        if "x" in i:
            spl = i.split("x")
            count = int(spl[0])
            width = float(spl[1])
            for i in range(count):
                distance = distance + width
                GridsNew.append(distance)
        else:
            distance = distance + float(i)
            GridsNew.append(distance)
    return GridsNew

def GridSystem(spacingX, labelsX, spacingY, labelsY, gridExtension):

    #GRIDS
    GridEx = gridExtension

    GridsX = spacingX.split()
    GridsX = getGridDistances(GridsX)
    Xmax = max(GridsX)
    GridsXLable = labelsX.split()
    GridsY = spacingY.split()
    GridsY = getGridDistances(GridsY)
    Ymax = max(GridsY)
    GridsYLable = labelsY.split()

    gridsX = []
    count = 0
    for i in GridsX:
        gridsX.append(Grid.byStartpointEndpoint(Line(Point(i, -GridEx, 0),Point(i, Ymax+GridEx, 0)),GridsXLable[count]))
        count =+ 1

    gridsY = []
    count = 0
    for i in GridsY:
        gridsY.append(Grid.byStartpointEndpoint(Line(Point(-GridEx, i, 0),Point(Xmax+GridEx, i, 0)),GridsYLable[count]))
        count = + 1

    return gridsX, gridsY