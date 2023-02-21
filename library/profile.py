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


"""This module provides tools to get profiledata from the database. These are json files
"""

__title__= "profile"
__author__ = "Maarten & Jonathan"
__url__ = "./objects/profile.py"

import sys, os, math
from pathlib import Path

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

from packages import helper
from objects.shape import *

jsonFile = "library\\profile_database\\steelprofile.json"

jsonFileStr = open(jsonFile, "r").read()


def findProfile(name):
    try:
        data = helper.findjson(name, jsonFileStr)[0]
        data.insert(0,name) #voeg profilename toe aan de lijst
        d1 = data[:-1]
        if data[-1] == "C-channel parallel flange":
            prof = CChannelParallelFlange(d1)
        elif data[-1] == "C-channel sloped flange":
            prof = CChannelSlopedFlange(d1[0],d1[1],d1[2],d1[3],d1[4],d1[5],d1[6],d1[7],d1[8],d1[9])
        elif data[-1] == "I-shape parallel flange":
            prof = IShapeParallelFlange(d1[0],d1[1],d1[2],d1[3],d1[4],d1[5]) #HELE GEKKE BUG, ITEMS WERKEN WEL LOS, MAAR TOTALE LIST NIET
        elif data[-1] == "Rectangle":
            prof = Rectangle(d1[0],d1[1],d1[2])
        elif data[-1] == "Round":
            prof = Round(d1)
        elif data[-1] == "LAngle":
            prof = LAngle(d1[0],d1[1],d1[2],d1[3],d1[4],d1[5],d1[6],d1[7],d1[8])
        elif data[-1] == "Rectangle hollow section":
            prof = RectangleHollowSection(d1[0],d1[1],d1[2],d1[3],d1[4],d1[5])
        else:
            prof = "error, profile not created"
    except:
        prof = "profileshape not found"
        data = "no profiledata found"
    return(prof, data)