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


"""This module provides tools to get profiledata from the database. These are json files
"""

__title__= "profile"
__author__ = "Maarten & Jonathan"
__url__ = "./objects/profile.py"

import sys
from pathlib import Path
import urllib.request
import json

file = Path(__file__).resolve()
package_root_directory = file.parents[2]
sys.path.append(str(package_root_directory))

from objects.steelshape import *
from geometry.geometry2d import *

# [!not included in BP singlefile - end]
jsonFile = "https://raw.githubusercontent.com/3BMLabs/Project-Ocondat/master/steelprofile.json"
url = urllib.request.urlopen(jsonFile)
data = json.loads(url.read())


class searchProfile:
    def __init__(self, name):
        self.name = name
        self.shape_coords = None
        self.shape_name = None
        self.synonyms = None
        for item in data:
            for i in item.values():
                synonymList = i[0]["synonyms"]
                #if self.name in synonymList:
                #bools = [self.name.lower() in e for e in [synonym.lower() for synonym in synonymList]]
                #if True in bools:
                if self.name.lower() in [synonym.lower() for synonym in synonymList]:
                    self.shape_coords = i[0]["shape_coords"]
                    self.shape_name = i[0]["shape_name"]
                    self.synonyms = i[0]["synonyms"]


class profiledataToShape:
    def __init__(self, name1, segmented = False):
        from geometry.curve import PolyCurve
        profile_data = searchProfile(name1)
        if profile_data == None:
            print(f"profile {name1} not recognised")
        shape_name = profile_data.shape_name

        if shape_name == None:
            profile_data = searchProfile(project.structural_fallback_element)
            err = f"Error, profile '{name1}' not recognised, define in {jsonFile} | fallback: '{project.structural_fallback_element}'"
            print(err)
            shape_name = profile_data.shape_name
        self.profile_data = profile_data
        self.shape_name = shape_name
        name = profile_data.name
        self.d1 = profile_data.shape_coords
        #self.d1.insert(0,name)
        d1 = self.d1
        if shape_name == "C-channel parallel flange":
            prof = CChannelParallelFlange(name,d1[0],d1[1],d1[2],d1[3],d1[4],d1[5])
        elif shape_name == "C-channel sloped flange":
            prof = CChannelSlopedFlange(name,d1[0],d1[1],d1[2],d1[3],d1[4],d1[5],d1[6],d1[7],d1[8])
        elif shape_name == "I-shape parallel flange":
            prof = IShapeParallelFlange(name,d1[0],d1[1],d1[2],d1[3],d1[4])
        elif shape_name == "I-shape sloped flange":
            prof = IShapeParallelFlange(name, d1[0], d1[1], d1[2], d1[3], d1[4])
            #Todo: add sloped flange shape
        elif shape_name == "Rectangle":
            prof = Rectangle(name,d1[0], d1[1])
        elif shape_name == "Round":
            prof = Round(name, d1[1])
        elif shape_name == "Round tube profile":
            prof = Roundtube(name, d1[0], d1[1])
        elif shape_name == "LAngle":
            prof = LAngle(name,d1[0],d1[1],d1[2],d1[3],d1[4],d1[5],d1[6],d1[7])
        elif shape_name == "TProfile":
            prof = TProfile(name, d1[0], d1[1], d1[2], d1[3], d1[4], d1[5], d1[6], d1[7], d1[8])
        elif shape_name == "Rectangle Hollow Section":
            prof = RectangleHollowSection(name,d1[0],d1[1],d1[2],d1[3],d1[4])

        self.prof = prof
        self.data = d1
        pc2d = self.prof.curve  # 2D polycurve
        if segmented == True:
            pc3d = PolyCurve.byPolyCurve2D(pc2d)
            pcsegment = PolyCurve.segment(pc3d, 10)
            pc2d2 = pcsegment.toPolyCurve2D()
        else:
            pc2d2 = pc2d
        self.polycurve2d = pc2d2

def justifictionToVector(plycrv2D: PolyCurve2D, XJustifiction, Yjustification, ey=None, ez=None):
    
    # print(XJustifiction)
    xval = []
    yval = []
    for i in plycrv2D.curves:
        xval.append(i.start.x)
        yval.append(i.start.y)

    #Boundingbox2D
    xmin = min(xval)
    xmax = max(xval)
    ymin = min(yval)
    ymax = max(yval)

    b = xmax-xmin
    h = ymax-ymin

    # print(b, h)

    dxleft = -xmax
    dxright = -xmin
    dxcenter = dxleft - 0.5 * b #CHECK
    dxorigin = 0

    dytop = -ymax
    dybottom = -ymin
    dycenter = dytop - 0.5 * h #CHECK
    dyorigin = 0

    if XJustifiction == "center":
        dx = dxorigin #TODO
    elif XJustifiction == "left":
        dx = dxleft
    elif XJustifiction == "right":
        dx = dxright
    elif XJustifiction == "origin":
        dx = dxorigin #TODO
    else:
        dx = 0

    if Yjustification == "center":
        dy = dyorigin   #TODO
    elif Yjustification == "top":
        dy = dytop
    elif Yjustification == "bottom":
        dy = dybottom
    elif Yjustification == "origin":
        dy = dyorigin #TODO
    else:
        dy = 0

    # print(dx, dy)
    v1 = Vector2(dx, dy)
    # v1 = Vector2(0, 0)

    return v1