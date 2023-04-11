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


"""This module provides classes for steel shapes
"""

__title__= "shape"
__author__ = "Joas"
__url__ = "./objects/shape.py"


import sys, os, math
from pathlib import Path
from objects.frame import *

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

from geometry.geometry2d import *

sqrt2 = math.sqrt(2)
class Tshape:
    def __init__(self, name, h, b, h1, b1):
        self.Description = "T-shape"
        self.ID = "T"

        # parameters
        self.name = name
        self.curve = []
        self.h = h  # height
        self.b = b  # width
        self.h1 = h1
        self.b1 = b1

        # describe points
        p1 = Point2D(b1 / 2, -h / 2)  # right bottom
        p2 = Point2D(b1 / 2, h / 2 - h1)  # right middle 1
        p3 = Point2D(b / 2, h / 2 - h1) # right middle 2
        p4 = Point2D(b / 2, h / 2) # right top
        p5 = Point2D(-b / 2, h / 2)  # left top
        p6 = Point2D(-b / 2, h / 2 - h1)  # left middle 2
        p7 = Point2D(-b1 / 2, h / 2 - h1) # left middle 1
        p8 = Point2D(-b1 / 2, -h / 2) # left bottom

        # describe curves
        l1 = Line2D(p1, p2)
        l2 = Line2D(p2, p3)
        l3 = Line2D(p3, p4)
        l4 = Line2D(p4, p5)
        l5 = Line2D(p5, p6)
        l6 = Line2D(p6, p7)
        l7 = Line2D(p7, p8)
        l8 = Line2D(p8, p1)

        self.curve = PolyCurve2D().byJoinedCurves([l1, l2, l3, l4, l5, l6, l7, l8])

        def __str__(self):
            return "Profile(" + f"{self.name})"


class Lshape:
    def __init__(self, name, h, b, h1, b1):
        self.Description = "L-shape"
        self.ID = "L"

        # parameters
        self.name = name
        self.curve = []
        self.h = h  # height
        self.b = b  # width
        self.h1 = h1
        self.b1 = b1

        # describe points
        p1 = Point2D(b / 2, -h / 2)  # right bottom
        p2 = Point2D(b / 2, -h / 2 + h1)  # right middle
        p3 = Point2D(-b / 2 + b1, -h / 2 + h1) # middle
        p4 = Point2D(-b / 2 + b1, h / 2) # middle top
        p5 = Point2D(-b / 2, h / 2)  # left top
        p6 = Point2D(-b / 2, -h / 2)  # left bottom

        # describe curves
        l1 = Line2D(p1, p2)
        l2 = Line2D(p2, p3)
        l3 = Line2D(p3, p4)
        l4 = Line2D(p4, p5)
        l5 = Line2D(p5, p6)
        l6 = Line2D(p6, p1)

        self.curve = PolyCurve2D().byJoinedCurves([l1, l2, l3, l4, l5, l6])

        def __str__(self):
            return "Profile(" + f"{self.name})"


class Eshape:
    def __init__(self, name, h, b, h1):
        self.Description = "E-shape"
        self.ID = "E"

        # parameters
        self.name = name
        self.curve = []
        self.h = h  # height
        self.b = b  # width
        self.h1 = h1

        # describe points
        p1 = Point2D(b / 2, -h / 2)  # right bottom
        p2 = Point2D(b / 2, -h / 2 + h1)
        p3 = Point2D(-b / 2 + h1, -h / 2 + h1)
        p4 = Point2D(-b / 2 + h1, -h1 / 2)
        p5 = Point2D(b / 2, -h1 / 2)
        p6 = Point2D(b / 2, h1 / 2)
        p7 = Point2D(-b / 2 + h1, h1 / 2)
        p8 = Point2D(-b / 2 + h1, h / 2 - h1)
        p9 = Point2D(b / 2, h / 2 - h1)
        p10 = Point2D(b / 2, h / 2)
        p11 = Point2D(-b / 2, h / 2)
        p12 = Point2D(-b / 2, -h / 2)

        # describe curves
        l1 = Line2D(p1, p2)
        l2 = Line2D(p2, p3)
        l3 = Line2D(p3, p4)
        l4 = Line2D(p4, p5)
        l5 = Line2D(p5, p6)
        l6 = Line2D(p6, p7)
        l7 = Line2D(p7, p8)
        l8 = Line2D(p8, p9)
        l9 = Line2D(p9, p10)
        l10 = Line2D(p10, p11)
        l11 = Line2D(p11, p12)
        l12 = Line2D(p12, p1)

        self.curve = PolyCurve2D().byJoinedCurves([l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12])

        def __str__(self):
            return "Profile(" + f"{self.name})"


class Nshape:
    def __init__(self, name, h, b, b1):
        self.Description = "N-shape"
        self.ID = "N"

        # parameters
        self.name = name
        self.curve = []
        self.h = h  # height
        self.b = b  # width
        self.b1 = b1

        # describe points
        p1 = Point2D(b / 2, -h / 2)  # right bottom
        p2 = Point2D(b / 2, h / 2)
        p3 = Point2D(b / 2 - b1, h / 2)
        p4 = Point2D(b / 2 - b1, -h / 2 + b1 * 2)
        p5 = Point2D(-b / 2 + b1, h / 2)
        p6 = Point2D(-b / 2, h / 2)
        p7 = Point2D(-b / 2, -h / 2)
        p8 = Point2D(-b / 2 + b1, -h / 2)
        p9 = Point2D(-b / 2 + b1, h / 2 - b1 * 2)
        p10 = Point2D(b / 2 - b1, -h / 2)

        # describe curves
        l1 = Line2D(p1, p2)
        l2 = Line2D(p2, p3)
        l3 = Line2D(p3, p4)
        l4 = Line2D(p4, p5)
        l5 = Line2D(p5, p6)
        l6 = Line2D(p6, p7)
        l7 = Line2D(p7, p8)
        l8 = Line2D(p8, p9)
        l9 = Line2D(p9, p10)
        l10 = Line2D(p10, p1)

        self.curve = PolyCurve2D().byJoinedCurves([l1, l2, l3, l4, l5, l6, l7, l8, l9, l10])

        def __str__(self):
            return "Profile(" + f"{self.name})"

class Arrowshape:
    def __init__(self, name, l, b, b1, l1):
        self.Description = "Arrow-shape"
        self.ID = "Arrowshape"

        # parameters
        self.name = name
        self.curve = []
        self.l = l  # length
        self.b = b  # width
        self.b1 = b1
        self.l1 = l1

        # describe points
        p1 = Point2D(0, l / 2)  # top middle
        p2 = Point2D(b / 2, -l / 2 + l1)
        # p3 = Point2D(b1 / 2, -l / 2 + l1)
        p3 = Point2D(b1 / 2, (-l / 2 + l1) + (l / 2) / 4)
        p4 = Point2D(b1 / 2, -l / 2)
        p5 = Point2D(-b1 / 2, -l / 2)
        # p6 = Point2D(-b1 / 2, -l / 2 + l1)
        p6 = Point2D(-b1 / 2, (-l / 2 + l1) + (l / 2) / 4)
        p7 = Point2D(-b / 2, -l / 2 + l1)

        # describe curves
        l1 = Line2D(p1, p2)
        l2 = Line2D(p2, p3)
        l3 = Line2D(p3, p4)
        l4 = Line2D(p4, p5)
        l5 = Line2D(p5, p6)
        l6 = Line2D(p6, p7)
        l7 = Line2D(p7, p1)

        self.curve = PolyCurve2D().byJoinedCurves([l1, l2, l3, l4, l5, l6, l7])

        def __str__(self):
            return "Profile(" + f"{self.name})"

