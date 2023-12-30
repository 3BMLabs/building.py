# [included in BP singlefile]

# -*- coding: utf8 -*-
#***************************************************************************
#*   Copyright (c) 2023 Maarten Vroegindeweij                              *
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

Patprefix = ';%UNITS=MM' \
         ';' \

Revitmodelpattern = ";%TYPE=MODEL"

class PATRow:
    def __init__(self,):
        self.angle = 0
        self.x_orig = 0
        self.y_orig = 0
        self.shift_pattern = 0
        self.offset = 0
        self.dash = 0
        self.space = 0
        self.patstr = ""

    def createpatstr(self):
        patstr = str(self.angle) + ",  " + str(self.x_orig) + ",  " + str(self.y_orig) + ",  " + str(self.shift_pattern) + ",  " + str(
            self.offset)
        if self.dash == 0:
            addstr = ""
        else:
            addstr = ",  " + str(self.dash) + ",  " + str(self.space)
        patstr = patstr + addstr
        return patstr

    def create(self,angle: float, x_orig: float, y_orig: float, shift_pattern: float, offset: float, dash: float=0, space: float=0):
        self.angle = angle
        self.x_orig = x_orig
        self.y_orig = y_orig
        self.shift_pattern = shift_pattern
        self.offset = offset
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
            row3 = PATRow().create(0, grosswidthheight, subspacing * n, grosswidthheight, grosswidthheight, grosswidthheight, -grosswidthheight)
            row4 = PATRow().create(90, subspacing * n, 0, grosswidthheight, grosswidthheight, grosswidthheight,-grosswidthheight)
            self.patrows.append(row3)
            self.patrows.append(row4)
            self.patstrings.append(row3.patstr)
            self.patstrings.append(row4.patstr)
            n = n + 1
        self.patstrings.append(";")
        return self

    def ParallelLines(self, name: str, widths: list, patterntype: str):
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

def CreatePatFile(patternobjects: list, filepath: str):
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

#Old , to be removed after transition to class system
def PatRow(angle: float, x_orig: float, y_orig: float, shift_pattern: float, offset: float, dash: float=0, space: float=0):
    #if dash and space are 0 then no pattern
    #rules: ;;;angle, x-origin, y-origin, shift_pattern, offset(spacing), pen_down, pen_up (negatief waarde)

    patstr = str(angle) + ",  " + str(x_orig) + ",  " + str(y_orig) + ",  " + str(shift_pattern) + ",  " + str(offset)
    if dash == 0:
        addstr = ""
    else:
        addstr = ",  " + str(dash) + ",  " + str(space)
    patstr = patstr + addstr
    return patstr

def TilePattern(name: str, width: float, height: float, patterntype: str):
    #this is rectangle tile pattern
    patstrings = []
    patstrings.append("*" + name)
    patstrings.append(patterntype)
    patstrings.append(PatRow(0,0,0,0,height,0,0))
    patstrings.append(PatRow(90,0,0,0,width,0,0))
    patstrings.append(";")
    return patstrings

def BlockPattern(name: str, grosswidthheight: float, numbersublines: int, patterntype: str):
    #this is a block pattern

    patstrings = []
    subspacing = grosswidthheight/numbersublines
    patstrings.append("*" + name)
    patstrings.append(patterntype)
    patstrings.append(PatRow(0,0,0,0,grosswidthheight,0,0))
    patstrings.append(PatRow(90,0,0,0,grosswidthheight,0,0))
    n = 0
    for i in range(numbersublines):
        patstrings.append(PatRow(0, grosswidthheight,subspacing * n , grosswidthheight, grosswidthheight, grosswidthheight, -grosswidthheight))
        patstrings.append(PatRow(90, subspacing * n, 0, grosswidthheight, grosswidthheight, grosswidthheight, -grosswidthheight))
        n = n + 1
    patstrings.append(";")
    return patstrings

def CombiPattern(name: str, grosswidthheight: float, patterntype: str):
    #this is a combined pattern
    width = (2/3)*grosswidthheight
    t = grosswidthheight/6

    patstrings = []
    patstrings.append("*" + name)
    patstrings.append(patterntype)
    patstrings.append(PatRow(0, 0, 0, 0, grosswidthheight, width, (-2 * t)))
    patstrings.append(PatRow(0, 0, t, 0, grosswidthheight, width, (-2 * t)))
    patstrings.append(PatRow(0, 0, 2 * t, 0, grosswidthheight, width, (-2 * t)))
    patstrings.append(PatRow(0, 2 * t, width, 0, grosswidthheight, width, (-2 * t)))
    patstrings.append(PatRow(0, 2 * t, width + t, 0, grosswidthheight, width, (-2 * t)))
    patstrings.append(PatRow(0, 2 * t, width + 2*t, 0, grosswidthheight, width, (-2 * t)))
    patstrings.append(PatRow(90, 0, 2 * t, 0, grosswidthheight, width, (-2 * t)))
    patstrings.append(PatRow(90, t, 2 * t, 0, grosswidthheight, width, (-2 * t)))
    patstrings.append(PatRow(90, 2 * t, 2 * t, 0, grosswidthheight, width, (-2 * t)))
    patstrings.append(PatRow(90, width, 0, 0, grosswidthheight, width, (-2 * t)))
    patstrings.append(PatRow(90, width + t, 0, 0, grosswidthheight, width, (-2 * t)))
    patstrings.append(PatRow(90, width + 2* t, 0, 0, grosswidthheight, width, (-2 * t)))
    patstrings.append(";")
    return patstrings

def ChevronPattern(name: str, grosswidth: float, widthtile: float, patterntype: str):
    #this is a chevronpattern(hungarian)
    lengthline = math.sqrt(2)*grosswidth

    patstrings = []
    patstrings.append("*" + name)
    patstrings.append(patterntype)
    patstrings.append(PatRow(90, 0, 0, 0, grosswidth, 0, 0 ))
    patstrings.append(PatRow(45, 0, 0, widthtile, widthtile,lengthline,-lengthline))
    patstrings.append(PatRow(-45, -grosswidth, 0, -widthtile , widthtile, lengthline, -lengthline))
    patstrings.append(";")
    return patstrings

def HerringbonePattern(name: str, lengthtile: float, numberOfTilesInLength: float, patterntype: str):
    #this is a herringbone pattern(visgraat)
    width = lengthtile / numberOfTilesInLength

    patstrings = []
    patstrings.append("*" + name)
    patstrings.append(patterntype)
    patstrings.append(PatRow(45,0,0,width,width,lengthtile+width,-(lengthtile-width)))
    patstrings.append(PatRow(135,0,0,-width,width,lengthtile,-lengthtile))
    patstrings.append(PatRow(-45, 0, 0, -width, width, width, -(2*lengthtile-width)))
    patstrings.append(";")
    return patstrings


def Strips(name: str, spacing: float, angle: float, patterntype: str):
    #these are continues lines with a certain spacing and angle
    patstrings = []
    patstrings.append("*" + name)
    patstrings.append(patterntype)
    patstrings.append(PatRow(angle,0,0,0,spacing,0,0))
    patstrings.append(";")
    return patstrings

def StretcherBondPattern(name, width, height, shift, patterntype: str):
    # this is a brick pattern rectangle with a shift
    patstrings = []
    patstrings.append("*" + name)
    patstrings.append(patterntype)
    patstrings.append(PatRow(0, 0, 0, 0, height, 0, 0))
    patstrings.append(PatRow(90, 0, 0, 0, width, height, -height))
    patstrings.append(PatRow(90, shift, height, 0, width, height, -height))
    patstrings.append(";")
    return patstrings

#reader
#drawsection