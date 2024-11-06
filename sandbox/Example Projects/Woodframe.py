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

import sys
import math
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
from construction.datum import *
from construction.panel import *
from exchange.speckle import *
from geometry.curve import *
from abstract.node import *
from construction.frame import *
from exchange.speckle import *

#Proof of Concept of Wood Frame Wall
def POCWoodFrameWall(l,h,startPoint,studheight,studwidth,spacing):
    distribution = 0 #Fixed Distance, Fixed Number, Maximum Spacing, Minimum Spacing
    count = round(l/spacing)
    obj1 = []
    x = 0 + studheight*0.5
    for i in range(count):
        obj1.append(Frame.by_startpoint_endpoint(Point.translate(startPoint, Vector(x, 0, studheight)),
                                               Point.translate(startPoint, Vector(x, 0, h-studheight)),
                                               Rectangle("stud", studwidth, studheight).curve, "stud", 0, BaseTimber))
        x = x + spacing

    obj1.append(Frame.by_startpoint_endpoint(startPoint, Point.translate(startPoint,Vector(l,0,0)),Rectangle("stud", studwidth, studheight).curve.translate(Vector2(studheight/2,0)),"bottomplate", 90, BaseTimber))
    obj1.append(Frame.by_startpoint_endpoint(Point.translate(startPoint,Vector(0,0,h)), Point.translate(startPoint,Vector(l,0,h)),Rectangle("stud", studwidth, studheight).curve.translate(Vector2(-studheight/2,0)),"topplate", 90, BaseTimber))
    obj1.append(Frame.by_startpoint_endpoint(Point.translate(startPoint, Vector(l-studheight*0.5, 0, studheight)),
                                           Point.translate(startPoint, Vector(l-studheight*0.5, 0, h - studheight)),
                                           Rectangle("stud", studwidth, studheight).curve, "last stud", 0, BaseTimber))
    return obj1

a = POCWoodFrameWall(2000,2600,Point(0, 0, 0),38,184,407)
b = POCWoodFrameWall(1500,1000,Point(2000, 0, 0),38,184,407)
c = POCWoodFrameWall(1500,600,Point(2000, 0, 2000),38,184,407)
d = POCWoodFrameWall(2000,2600,Point(3500, 0, 0),38,184,407)

obj = a + b + c + d

SpeckleObj = translateObjectsToSpeckleObjects(obj)
Commit = TransportToSpeckle("speckle.xyz", "7603a8603c", SpeckleObj, "Test objects")

