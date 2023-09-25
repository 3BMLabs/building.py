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


"""This module provides import data from PAT file
"""

__title__= "PAT"
__author__ = "Maarten & Jonathan"
__url__ = "./exchange/pat.py"

Patprefix = '%UNITS=MM' \
         ';' \

Revitmodelpattern = ";%TYPE=MODEL"

def PatRow(angle: float, x_orig: float, y_orig: float, shift_pattern: float, offset: float, dash: float=0, space: float=0):
    #if dash and space are 0 then no pattern
    patstr = ";    " + str(angle) + ",             " + str(x_orig) + ",             " + str(y_orig) + ",             " + str(shift_pattern) + ",             " + str(offset)
    if dash == 0:
        addstr = ""
    else:
        addstr = ",             " + str(dash) + ",             " + str(space)
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

def Strips(name: str, spacing: float, angle: float, patterntype: str):
    #this is rectangle tile pattern
    patstrings = []
    patstrings.append("*" + name)
    patstrings.append(patterntype)
    patstrings.append(PatRow(angle,0,0,0,spacing,0,0))
    patstrings.append(";")

    return patstrings

def StretcherBondPattern(name, width, height, shift, patterntype: str):
    # this is rectangle stretcher bond pattern
    patstrings = []
    patstrings.append("*" + name)
    patstrings.append(patterntype)
    patstrings.append(PatRow(0, 0, 0, 0, height, 0, 0))
    patstrings.append(PatRow(90, 0, 0, shift, width, height, height))
    patstrings.append(";")

    return patstrings



#reader
#drawsection