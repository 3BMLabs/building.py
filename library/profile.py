# -*- coding: utf8 -*-
#***************************************************************************
#*   Copyright (c) 2023 Jonathan Van der Gouwe & Maarten Vroegindeweij     *
#*   jonathan@3bm.co.nl & maarten@3bm.co.nl                                *
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


"""This module provides tools to get profiledata from the database
"""

__title__= "profile"
__author__ = "Maarten & Jonathan"
__url__ = "./objects/shape.py"

from packages import helper
from objects.shape import *

jsonFile = "C:/Users/mikev/3BM Dropbox/Maarten Vroegindeweij/Maarten en Jonathan 3BM/PyBuildingSystems/library/profile_database/steelprofile.json"
jsonFileStr = open(jsonFile, "r").read()


def findProfile(name):
    try:
        data = helper.findjson(name, jsonFileStr)[0]
        data.insert(0,name) #voeg profilename weer toe aan de lijst
        d1 = data[:-1]
        if data[-1] == "C-channel parallel flange":
            prof = CChannelParallelFlange(data[:-1])
        elif data[-1] == "C-channel sloped flange":
            prof = CChannelSlopedFlange(data[:-1])
        elif data[-1] == "I-shape parallel flange":
            prof = IShapeParallelFlange(d1[0],d1[1],d1[2],d1[3],d1[4],d1[5]) #HELE GEKKE BUG, ITEMS WERKEN WEL LOS, MAAR TOTALE LIST NIET
        elif data[-1] == "Rectangle":
            prof = Rectangle(data[:-1])
        elif data[-1] == "Round":
            prof = Round(data[:-1])
        elif data[-1] == "L-angle":
            prof = LAngle(data[:-1])
        else:
            prof = "profile not found"
    except:
        prof = "exception"
        data = None
    return(prof, data)


#print(findProfile("IPE500"))

