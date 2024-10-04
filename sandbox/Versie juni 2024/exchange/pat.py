# [included in BP singlefile]
# [!not included in BP singlefile - start]
# -*- coding: utf8 -*-
#***************************************************************************
#*   Copyright (c) 2024 Maarten Vroegindeweij                              *
#*   maarten@3bm.co.nl                                                     *
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


"""This module provides import data from PAT file
"""

__title__= "PAT"
__author__ = "Maarten"
__url__ = "./exchange/pat.py"

import math
from geometry.linestyle import *
from objects.panel import *
# [!not included in BP singlefile - end]

Patprefix = ';%UNITS=MM' \
         ';' \

Revitmodelpattern = ";%TYPE=MODEL"

class PATRow:
    def __init__(self,):
        self.angle = 0
        self.x_orig = 0
        self.y_orig = 0
        self.shift_pattern = 0
        self.offset_spacing = 0
        self.dash = 0
        self.space = 0
        self.patstr = ""

    def createpatstr(self):
        patstr = str(self.angle) + ",  " + str(self.x_orig) + ",  " + str(self.y_orig) + ",  " + str(self.shift_pattern) + ",  " + str(
            self.offset_spacing)
        if self.dash == 0:
            addstr = ""
        else:
            addstr = ",  " + str(self.dash) + ",  " + str(self.space)
        patstr = patstr + addstr
        return patstr

    def create(self,angle: float, x_orig: float, y_orig: float, shift_pattern: float, offset_spacing: float, dash: float=0, space: float=0):
        # if dash and space are 0 then no pattern
        # rules: ;;;angle, x-origin, y-origin, shift_pattern, offset(spacing), pen_down, pen_up (negatief waarde)
        # x, y-origin is global,
        self.angle = angle
        self.x_orig = x_orig
        self.y_orig = y_orig
        self.shift_pattern = shift_pattern
        self.offset_spacing = offset_spacing
        self.dash = dash
        self.space = space
        self.patstr = self.createpatstr()
        return self

class PAT:
    def __init__(self,):
        self.patrows = []
        self.patstrings = []
        self.name = "None"
        self.patterntype = "None"

    def TilePattern(self, name: str, width: float, height: float, patterntype: str):
        #this is rectangle tile pattern
        self.name = name
        self.patterntype = patterntype
        row1 = PATRow().create(0,0,0,0,height,0,0)
        row2 = PATRow().create(90,0,0,0,width,0,0)
        self.patrows.append(row1)
        self.patrows.append(row2)

        self.patstrings.append("*" + name)
        self.patstrings.append(patterntype)
        self.patstrings.append(row1.patstr)
        self.patstrings.append(row2.patstr)
        self.patstrings.append(";")
        return self

    def BlockPattern(self, name: str, grosswidthheight: float, numbersublines: int, patterntype: str):
        #this is a block pattern
        subspacing = grosswidthheight / numbersublines
        self.name = name
        self.patterntype = patterntype
        row1 = PATRow().create(0,0,0,0,grosswidthheight,0,0)
        row2 = PATRow().create(90,0,0,0,grosswidthheight,0,0)

        self.patrows.append(row1)
        self.patrows.append(row2)

        self.patstrings.append("*" + name)
        self.patstrings.append(patterntype)
        self.patstrings.append(row1.patstr)
        self.patstrings.append(row2.patstr)
        n = 0
        for i in range(numbersublines):
            row3 = PATRow().create(0, 0, subspacing * n + grosswidthheight, 0, grosswidthheight*2, grosswidthheight, -grosswidthheight)
            row4 = PATRow().create(0, grosswidthheight, subspacing * n, 0, grosswidthheight*2, grosswidthheight, -grosswidthheight)
            row5 = PATRow().create(90, subspacing * n, 0, 0, grosswidthheight*2, grosswidthheight,-grosswidthheight)
            row6 = PATRow().create(90, subspacing * n + grosswidthheight, grosswidthheight, 0, grosswidthheight*2, grosswidthheight,-grosswidthheight)
            self.patrows.append(row3)
            self.patrows.append(row4)
            self.patrows.append(row5)
            self.patrows.append(row6)
            self.patstrings.append(row3.patstr)
            self.patstrings.append(row4.patstr)
            self.patstrings.append(row5.patstr)
            self.patstrings.append(row6.patstr)
            n = n + 1
        self.patstrings.append(";")
        return self

    def CombiPattern(self, name: str, grosswidthheight: float, patterntype: str):
        #this is a combined pattern
        width = (2 / 3) * grosswidthheight
        t = grosswidthheight / 6
        self.name = name
        self.patterntype = patterntype

        row1 = PATRow().create(0, 0, 0, 0, grosswidthheight, width, (-2 * t))
        row2 = PATRow().create(0, 0, t, 0, grosswidthheight, width, (-2 * t))
        row3 = PATRow().create(0, 0, 2 * t, 0, grosswidthheight, width, (-2 * t))
        row4 = PATRow().create(0, 2 * t, width, 0, grosswidthheight, width, (-2 * t))
        row5 = PATRow().create(0, 2 * t, width + t, 0, grosswidthheight, width, (-2 * t))
        row6 = PATRow().create(0, 2 * t, width + 2 * t, 0, grosswidthheight, width, (-2 * t))
        row7 = PATRow().create(90, 0, 2 * t, 0, grosswidthheight, width, (-2 * t))
        row8 = PATRow().create(90, t, 2 * t, 0, grosswidthheight, width, (-2 * t))
        row9 = PATRow().create(90, 2 * t, 2 * t, 0, grosswidthheight, width, (-2 * t))
        row10 = PATRow().create(90, width, 0, 0, grosswidthheight, width, (-2 * t))
        row11 = PATRow().create(90, width + t, 0, 0, grosswidthheight, width, (-2 * t))
        row12 = PATRow().create(90, width + 2 * t, 0, 0, grosswidthheight, width, (-2 * t))

        self.patrows.append(row1)
        self.patrows.append(row2)
        self.patrows.append(row3)
        self.patrows.append(row4)
        self.patrows.append(row5)
        self.patrows.append(row6)
        self.patrows.append(row7)
        self.patrows.append(row8)
        self.patrows.append(row9)
        self.patrows.append(row10)
        self.patrows.append(row11)
        self.patrows.append(row12)

        self.patstrings.append("*" + name)
        self.patstrings.append(patterntype)
        self.patstrings.append(row1.patstr)
        self.patstrings.append(row2.patstr)
        self.patstrings.append(row3.patstr)
        self.patstrings.append(row4.patstr)
        self.patstrings.append(row5.patstr)
        self.patstrings.append(row6.patstr)
        self.patstrings.append(row7.patstr)
        self.patstrings.append(row8.patstr)
        self.patstrings.append(row9.patstr)
        self.patstrings.append(row10.patstr)
        self.patstrings.append(row11.patstr)
        self.patstrings.append(row12.patstr)
        self.patstrings.append(";")
        return self

    def ChevronPattern(self, name: str, grosswidth: float, widthtile: float, patterntype: str):
        #this is a chevronpattern(hungarian)
        lengthline = math.sqrt(2) * grosswidth
        self.name = name
        self.patterntype = patterntype

        row1 = PATRow().create(90, 0, 0, 0, grosswidth, 0, 0)
        row2 = PATRow().create(45, 0, 0, widthtile, widthtile, lengthline, -lengthline)
        row3 = PATRow().create(-45, -grosswidth, 0, -widthtile, widthtile, lengthline, -lengthline)

        self.patrows.append(row1)
        self.patrows.append(row2)
        self.patrows.append(row3)

        self.patstrings.append("*" + name)
        self.patstrings.append(patterntype)
        self.patstrings.append(row1.patstr)
        self.patstrings.append(row2.patstr)
        self.patstrings.append(row3.patstr)
        self.patstrings.append(";")
        return self

    def HerringbonePattern(self, name: str, lengthtile: float, numberOfTilesInLength: float, patterntype: str):
        # this is a herringbone pattern(visgraat)
        width = lengthtile / numberOfTilesInLength
        self.name = name
        self.patterntype = patterntype

        row1 = PATRow().create(45, 0, 0, width, width, lengthtile + width, -(lengthtile - width))
        row2 = PATRow().create(135, 0, 0, -width, width, lengthtile, -lengthtile)
        row3 = PATRow().create(-45, 0, 0, -width, width, width, -(2 * lengthtile - width))

        self.patrows.append(row1)
        self.patrows.append(row2)
        self.patrows.append(row3)

        self.patstrings.append("*" + name)
        self.patstrings.append(patterntype)
        self.patstrings.append(row1.patstr)
        self.patstrings.append(row2.patstr)
        self.patstrings.append(row3.patstr)
        self.patstrings.append(";")
        return self

    def Strips(self, name: str, spacing: float, angle: float, patterntype: str):
        # these are continues lines with a certain spacing and angle
        self.name = name
        self.patterntype = patterntype

        row1 = PATRow().create(angle, 0, 0, 0, spacing, 0, 0)

        self.patrows.append(row1)

        self.patstrings.append("*" + name)
        self.patstrings.append(patterntype)
        self.patstrings.append(row1.patstr)
        self.patstrings.append(";")
        return self

    def StretcherBondPattern(self, name: str, width: float, height: float, shift: float, patterntype: str):
        # this is a brick pattern rectangle with a shift
        self.name = name
        self.patterntype = patterntype

        row1 = PATRow().create(0, 0, 0, 0, height, 0, 0)
        row2 = PATRow().create(90, 0, 0, 0, width, height, -height)
        row3 = PATRow().create(90, shift, height, 0, width, height, -height)

        self.patrows.append(row1)
        self.patrows.append(row2)
        self.patrows.append(row3)

        self.patstrings.append("*" + name)
        self.patstrings.append(patterntype)
        self.patstrings.append(row1.patstr)
        self.patstrings.append(row2.patstr)
        self.patstrings.append(row3.patstr)
        self.patstrings.append(";")
        return self

    def ParallelLines(self, name: str, widths: list, patterntype: str):
        # this pattern consists of parallel lines with different offset distances. Can be defined in a list.
        self.name = name
        self.patterntype = patterntype
        self.patstrings.append("*" + name)
        self.patstrings.append(patterntype)
        width = sum(widths)
        x = 0
        for i in widths:
            row = PATRow().create(90,x,0,0,width,0,0)
            self.patrows.append(row)
            self.patstrings.append(row.patstr)
            x = x + i

        self.patstrings.append(";")
        return self

    def stretcher_bond_with_joint(self, name:str, bricklength: float, brickheight: float, jointwidth: float, jointheight: float, patterntype: str):
        #This is stretcherbond(halfsteensverband) with joints
        self.name = name
        self.patterntype = patterntype
        lagenmaat = brickheight + jointheight

        row1 = PATRow().create(0,0,0,0,lagenmaat*2, bricklength, -jointwidth)
        row2 = PATRow().create(0,0,brickheight,0,lagenmaat*2,bricklength, -jointwidth)
        row3 = PATRow().create(0,0.5*(bricklength + jointwidth),lagenmaat,0,lagenmaat*2, bricklength, -jointwidth)
        row4 = PATRow().create(0,0.5*(bricklength + jointwidth),lagenmaat+brickheight,0,lagenmaat*2, bricklength, -jointwidth)

        row5 = PATRow().create(90,0,0,0,bricklength+jointwidth,brickheight,-(brickheight+2*jointheight))
        row6 = PATRow().create(90,bricklength,0,0,bricklength+jointwidth,brickheight,-(brickheight+2*jointheight))
        row7 = PATRow().create(90,(bricklength+jointwidth)/2,lagenmaat,0,bricklength+jointwidth,brickheight,-(brickheight+2*jointheight))
        row8 = PATRow().create(90,(bricklength+jointwidth)/2+bricklength,lagenmaat,0,bricklength+jointwidth,brickheight,-(brickheight+2*jointheight))

        self.patrows.append(row1)
        self.patrows.append(row2)
        self.patrows.append(row3)
        self.patrows.append(row4)
        self.patrows.append(row5)
        self.patrows.append(row6)
        self.patrows.append(row7)
        self.patrows.append(row8)

        self.patstrings.append("*" + name)
        self.patstrings.append(patterntype)
        self.patstrings.append(row1.patstr)
        self.patstrings.append(row2.patstr)
        self.patstrings.append(row3.patstr)
        self.patstrings.append(row4.patstr)
        self.patstrings.append(row5.patstr)
        self.patstrings.append(row6.patstr)
        self.patstrings.append(row7.patstr)
        self.patstrings.append(row8.patstr)
        self.patstrings.append(";")
        return self

    def TilePatternWithJoint(self, name: str, width: float, height: float, jointwidth: float, jointheight: float, patterntype: str):
        #this is rectangle tile pattern with joints between tiles
        self.name = name
        self.patterntype = patterntype
        row1 = PATRow().create(0, 0, 0, 0, height+jointheight, width, -jointwidth)
        row2 = PATRow().create(0, 0, height, 0, height + jointheight, width, -jointwidth)
        row3 = PATRow().create(90,0,0,0,width+jointwidth,height,-jointheight)
        row4 = PATRow().create(90,width,0,0,width+jointwidth,height,-jointheight)

        self.patrows.append(row1)
        self.patrows.append(row2)
        self.patrows.append(row3)
        self.patrows.append(row4)

        self.patstrings.append("*" + name)
        self.patstrings.append(patterntype)
        self.patstrings.append(row1.patstr)
        self.patstrings.append(row2.patstr)
        self.patstrings.append(row3.patstr)
        self.patstrings.append(row4.patstr)
        self.patstrings.append(";")
        return self

    def cross_bond_with_joint(self, name:str, brickwidth: float, bricklength: float, brickheight: float, jointwidth: float, jointheight: float, patterntype: str):
        #This is crossbond(kruisverband) with joints
        self.name = name
        self.patterntype = patterntype
        lagenmaat = brickheight + jointheight

        row1 = PATRow().create(0,0,0,0,lagenmaat*4, bricklength, -jointwidth)
        row2 = PATRow().create(0,0,brickheight,0,lagenmaat*4,bricklength, -jointwidth)

        row3 = PATRow().create(0,0.5*(brickwidth + jointwidth),lagenmaat,0,lagenmaat*2, brickwidth, -jointwidth)
        row4 = PATRow().create(0,0.5*(brickwidth + jointwidth),lagenmaat + brickheight,0,lagenmaat*2, brickwidth, -jointwidth)

        row5 = PATRow().create(0,0.5*(bricklength + jointwidth),lagenmaat*2,0,lagenmaat*4, bricklength, -jointwidth)
        row6 = PATRow().create(0,0.5*(bricklength + jointwidth),lagenmaat*4+brickheight,0,lagenmaat*2, bricklength, -jointwidth)

        row7 = PATRow().create(90,0,0,0,bricklength+jointwidth,brickheight,-(3*lagenmaat+jointheight))
        row8 = PATRow().create(90,bricklength,0,0,bricklength+jointwidth,brickheight,-(3*lagenmaat+jointheight))
        row9 = PATRow().create(90,0.5*(brickwidth + jointwidth),lagenmaat,0,brickwidth+jointwidth,brickheight,-(brickheight+2*jointheight))
        row10 = PATRow().create(90,0.5*(brickwidth + jointwidth)+brickwidth,lagenmaat,0,brickwidth+jointwidth,brickheight,-(brickheight+2*jointheight))

        row11 = PATRow().create(90,(bricklength+jointwidth)/2,lagenmaat*2,0,bricklength+jointwidth,brickheight,-(3*lagenmaat+jointheight))
        row12 = PATRow().create(90,(bricklength+jointwidth)/2+bricklength,lagenmaat*2,0,bricklength+jointwidth,brickheight,-(3*lagenmaat+jointheight))

        self.patrows.append(row1)
        self.patrows.append(row2)
        self.patrows.append(row3)
        self.patrows.append(row4)
        self.patrows.append(row5)
        self.patrows.append(row6)
        self.patrows.append(row7)
        self.patrows.append(row8)
        self.patrows.append(row9)
        self.patrows.append(row10)
        self.patrows.append(row11)
        self.patrows.append(row12)

        self.patstrings.append("*" + name)
        self.patstrings.append(patterntype)
        self.patstrings.append(row1.patstr)
        self.patstrings.append(row2.patstr)
        self.patstrings.append(row3.patstr)
        self.patstrings.append(row4.patstr)
        self.patstrings.append(row5.patstr)
        self.patstrings.append(row6.patstr)
        self.patstrings.append(row7.patstr)
        self.patstrings.append(row8.patstr)
        self.patstrings.append(row9.patstr)
        self.patstrings.append(row10.patstr)
        self.patstrings.append(row11.patstr)
        self.patstrings.append(row12.patstr)
        self.patstrings.append(";")
        return self

def CreatePatFile(patternobjects: list, filepath: str):
    #Write Pattern File
    patternstrings = []
    for i in patternobjects:
        patternstrings = patternstrings + i.patstrings

    patternstrings.insert(0, Patprefix)

    patn = []
    for i in patternstrings:
        patn.append(i + "\n")
    # Create PAT-file
    fp = open(filepath, 'w')
    for i in patn:
        fp.write(i)
    fp.close()
    return filepath

def PatRowGeom(patrow: PATRow, width: float, height: float, dx, dy):
    # tested for 0-90 degrees
    #Create BuildingPy Lines from PAT-objects
    nlines = int(height / patrow.offset_spacing)+1
    lines = []
    n = 0
    for i in range(nlines):
        Xn = Vector3.rotate_XY(X_axis, math.radians(patrow.angle))
        Yn = Vector3.rotate_XY(Y_Axis, math.radians(patrow.angle))
        CSNewLn = CoordinateSystem(Point(0, 0, 0), Xn, Yn, Z_Axis)
        x_start = 0
        y_start = 0
        x_end = width
        y_end = 0
        l1 = Line(Point(x_start, y_start, 0), Point(x_end, y_end, 0)) # baseline
        l2 = Line.transform(l1, CSNewLn) # rotation
        v1 = Vector3.by_two_points(l2.start,l2.end)
        v1 = Vector3.normalize(v1)
        v2 = Vector3.scale(v1, patrow.shift_pattern * n)
        l3 = Line.translate_2(l2, v2)  # shift of line for pattern
        #if patrow.shift_pattern == 0:
        #    l3 = l2
        #else:
        #    v2 = Vector3.scale(v1, patrow.shift_pattern*(n+1))
        #    l3 = Line.translate_2(l2,v2) # shift of line for pattern
        v3 = Vector3.normalize(Vector3.cross_product(v1,Z_Axis)) #Eenheidsvector haaks op lijn
        if patrow.angle == 0:
            v4 = Vector3.scale(v3, n * patrow.offset_spacing)  # Verplaatsingsvector voor spacing, inverse in geval lijn = 0 graden
            v4 = Vector3.reverse(v4)
        else:
            v4 = Vector3.scale(v3, n * patrow.offset_spacing)  # Verplaatsingsvector voor spacing
        if n * patrow.offset_spacing == 0: # eerste lijn heeft geen verplaatsing
            l4 = l3
        else:
            l4 = l3.translate(v4)
        v6 = Vector3(dx + patrow.x_orig,dy + patrow.y_orig,0)
        print(v6)
        l5 = Line.translate_2(l4,v6)

        if patrow.dash == 0 and patrow.space == 0:
            lines.append(l5)
        else:
            # dashed lines
            LinePattern = ["Pat", [patrow.dash, -patrow.space],
                           1]  # Rule: line, whitespace, line whitespace etc., scale
            for i in line_to_pattern(l5, LinePattern):
                lines.append(i)
        n = n + 1

    return lines

def PAT2Geom(Pat: PAT, width, height,dx,dy):
    lineObjs = []
    for i in Pat.patrows:
        lines = PatRowGeom(i, width, height,dx,dy)
        for i in lines:
            lineObjs.append(i)
    return lineObjs

#reader
#drawsection