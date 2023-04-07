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
__author__ = "Maarten & Jonathan"
__url__ = "./objects/steelshape.py"


import sys, os, math
from pathlib import Path
from objects.frame import *

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

from geometry.geometry2d import *

sqrt2 = math.sqrt(2)

#Hierachie:
  #point 2D
  #line 2D
  #PolyCurve2D 2D
  #shape is een parametrische vorm heeft als resultaat een 2D curve
  #section is een profiel met eigenschappen HEA200, 200,200,10,10,5 en eventuele rekenkundige eigenschappen.
  #beam is een object wat in 3D zit met materiaal enz.


class CChannelParallelFlange:
    def __init__(self, name, h, b, tw, tf, r, ex):
        self.Description = "C-channel with parallel flange"
        self.ID = "C_PF"

        #parameters
        self.name = name
        self.curve = []
        self.h = h          #height
        self.b = b          #width
        self.tw = tw        #web thickness
        self.tf = tf        #flange thickness
        self.r1 = r        #web fillet
        self.ex = ex        #centroid horizontal

        #describe points
        p1 = Point2D(-ex, -h / 2)  # left bottom
        p2 = Point2D(b - ex, -h / 2)  # right bottom
        p3 = Point2D(b - ex, -h / 2 + tf)
        p4 = Point2D(-ex + tw + r, -h / 2 + tf)  # start arc
        p5 = Point2D(-ex + tw + r, -h / 2 + tf + r)  # second point arc
        p6 = Point2D(-ex + tw, -h / 2 + tf + r)  # end arc
        p7 = Point2D(-ex + tw, h / 2 - tf - r)  # start arc
        p8 = Point2D(-ex + tw + r, h / 2 - tf - r)  # second point arc
        p9 = Point2D(-ex + tw + r, h / 2 - tf)  # end arc
        p10 = Point2D(b - ex, h / 2 - tf)
        p11 = Point2D(b - ex, h / 2)  # right top
        p12 = Point2D(-ex, h / 2)  # left top

        #describe curves
        l1 = Line2D(p1, p2)
        l2 = Line2D(p2, p3)
        l3 = Line2D(p3, p4)
        l4 = Arc2D(p4, p5, p6)
        l5 = Line2D(p6, p7)
        l6 = Arc2D(p7, p8, p9)
        l7 = Line2D(p9, p10)
        l8 = Line2D(p10, p11)
        l9 = Line2D(p11, p12)
        l10 = Line2D(p12, p1)

        self.curve = PolyCurve2D().byJoinedCurves([l1, l2, l3, l4, l5, l6, l7, l8, l9, l10])

    def __str__(self):
        return "Profile(" + f"{self.name})"


class CChannelSlopedFlange:
    def __init__(self, name, h, b, tw, tf, r1, r2, tl, sa, ex):
        self.Description = "C-channel with sloped flange"
        self.ID = "C_SF"

        # parameters
        self.name = name
        self.curve = []
        self.b = b  # width
        self.h = h  # height
        self.tf = tf  # flange thickness
        self.tw = tw  # web thickness
        self.r1 = r1  # web fillet
        self.r11 = r1 / sqrt2
        self.r2 = r2  # flange fillet
        self.r21 = r2 / sqrt2
        self.tl = tl  # flange thickness location from right
        self.sa = math.radians(sa)  # the angle of sloped flange in degrees
        self.ex = ex  # centroid horizontal

        # describe points
        p1 = Point2D(-ex, -h / 2)  # left bottom
        p2 = Point2D(b - ex, -h / 2)  # right bottom
        p3 = Point2D(b - ex, -h / 2 + tf - math.tan(self.sa) * tl - r2)  # start arc
        p4 = Point2D(b - ex - r2 + self.r21, -h / 2 + tf - math.tan(self.sa) * tl - r2 + self.r21)  # second point arc
        p5 = Point2D(b - ex - r2 + math.sin(self.sa) * r2, -h / 2 + tf - math.tan(self.sa) * (tl - r2))  # end arc
        p6 = Point2D(-ex + tw + r1 - math.sin(self.sa) * r1, -h / 2 + tf + math.tan(self.sa) * (b - tl - tw - r1))  # start arc
        p7 = Point2D(-ex + tw + r1 - self.r11, -h / 2 + tf + math.tan(self.sa) * (b - tl - tw - r1) + r1 - self.r11)  # second point arc
        p8 = Point2D(-ex + tw, -h / 2 + tf + math.tan(self.sa) * (b - tl - tw) + r1)  # end arc
        p9 = Point2D(p8.x, -p8.y)  # start arc
        p10 = Point2D(p7.x, -p7.y)  # second point arc
        p11 = Point2D(p6.x, -p6.y)  # end arc
        p12 = Point2D(p5.x, -p5.y)  # start arc
        p13 = Point2D(p4.x, -p4.y)  # second point arc
        p14 = Point2D(p3.x, -p3.y)  # end arc
        p15 = Point2D(p2.x, -p2.y)  # right top
        p16 = Point2D(p1.x, -p1.y)  # left top

        # describe curves
        l1 = Line2D(p1, p2)
        l2 = Line2D(p2, p3)
        l3 = Arc2D(p3, p4, p5)
        l4 = Line2D(p5, p6)
        l5 = Arc2D(p6, p7, p8)
        l6 = Line2D(p8, p9)
        l7 = Arc2D(p9, p10, p11)
        l8 = Line2D(p11, p12)
        l9 = Arc2D(p12, p13, p14)
        l10 = Line2D(p14, p15)
        l11 = Line2D(p15, p16)
        l12 = Line2D(p16, p1)

        self.curve = PolyCurve2D().byJoinedCurves([l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12])

    def __str__(self):
        return "Profile(" + f"{self.name})"


class IShapeParallelFlange:
    def __init__(self, name, h, b, tw, tf, r):
        self.Description = "I Shape profile with parallel flange"
        self.ID = "I_PF"
        # HEA, IPE, HEB, HEM etc.

        # parameters
        self.name = name
        self.h = h  # height
        self.b = b # width
        self.tw = tw  # web thickness
        self.tf = tf  # flange thickness
        self.r = r  # web fillet
        self.r1 = r1 = r / sqrt2

        # describe points
        p1 = Point2D(b / 2, -h / 2)  # right bottom
        p2 = Point2D(b / 2, -h / 2 + tf)
        p3 = Point2D(tw / 2 + r, -h / 2 + tf)  # start arc
        p4 = Point2D(tw / 2 + r - r1, (-h / 2 + tf + r - r1))  # second point arc
        p5 = Point2D(tw / 2, -h / 2 + tf + r)  # end arc
        p6 = Point2D(tw / 2, h / 2 - tf - r)  # start arc
        p7 = Point2D(tw / 2 + r - r1, h / 2 - tf - r + r1)  # second point arc
        p8 = Point2D(tw / 2 + r, h / 2 - tf)  # end arc
        p9 = Point2D(b / 2, h / 2 - tf)
        p10 = Point2D((b / 2), (h / 2))  # right top
        p11 = Point2D(-p10.x, p10.y)  # left top
        p12 = Point2D(-p9.x, p9.y)
        p13 = Point2D(-p8.x, p8.y)  # start arc
        p14 = Point2D(-p7.x, p7.y)  # second point arc
        p15 = Point2D(-p6.x, p6.y)  # end arc
        p16 = Point2D(-p5.x, p5.y)  # start arc
        p17 = Point2D(-p4.x, p4.y)  # second point arc
        p18 = Point2D(-p3.x, p3.y)  # end arc
        p19 = Point2D(-p2.x, p2.y)
        p20 = Point2D(-p1.x, p1.y)

        # describe curves
        l1 = Line2D(p1, p2)
        l2 = Line2D(p2, p3)
        l3 = Arc2D(p3, p4, p5)
        l4 = Line2D(p5, p6)
        l5 = Arc2D(p6, p7, p8)
        l6 = Line2D(p8, p9)
        l7 = Line2D(p9, p10)
        l8 = Line2D(p10, p11)
        l9 = Line2D(p11, p12)
        l10 = Line2D(p12, p13)
        l11 = Arc2D(p13, p14, p15)
        l12 = Line2D(p15, p16)
        l13 = Arc2D(p16, p17, p18)
        l14 = Line2D(p18, p19)
        l15 = Line2D(p19, p20)
        l16 = Line2D(p20, p1)

        self.curve = PolyCurve2D().byJoinedCurves([l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12, l13, l14, l15, l16])

        def __str__(self):
            return "Profile(" + f"{self.name})"


class Rectangle:
    def __init__(self, name, b, h):
        self.Description = "Rectangle"
        self.ID = "Rec"

        # parameters
        self.name = name
        self.curve = []
        self.h = h  # height
        self.b = b  # width

        # describe points
        p1 = Point2D(b / 2, -h / 2)  # right bottom
        p2 = Point2D(b / 2, h / 2)  # right top
        p3 = Point2D(-b / 2, h / 2) # left top
        p4 = Point2D(-b / 2, -h / 2) # left bottom

        # describe curves
        l1 = Line2D(p1, p2)
        l2 = Line2D(p2, p3)
        l3 = Line2D(p3, p4)
        l4 = Line2D(p4, p1)

        self.curve = PolyCurve2D().byJoinedCurves([l1, l2, l3, l4])

        def __str__(self):
            return "Profile(" + f"{self.name})"


class Round:
    def __init__(self, name, r):
        self.Description = "Round"
        self.ID = "Rnd"

        # parameters
        self.name = name
        self.curve = []
        self.r = r  # radius
        self.data = (name, r, "Round")

        # describe points
        p1 = Point2D(r, 0)  # right middle
        p2 = Point2D(0, r)  # middle top
        p3 = Point2D(-r, 0) # left middle
        p4 = Point2D(0, -r) # middle bottom

        # describe curves
        l1 = Arc2D(p1, p2, p3)
        l2 = Arc2D(p3, p4, p1)

        self.curve = PolyCurve2D().byJoinedCurves([l1, l2])

        def __str__(self):
            return "Profile(" + f"{self.name})"

class Roundtube:
    #ToDo: add inner circle
    def __init__(self, name, d, t):
        self.Description = "Round Tube Profile"
        self.ID = "Tube"

        # parameters
        self.name = name
        self.curve = []
        self.d = d
        self.r = d/2  # radius
        self.t = t  # wall thickness
        self.data = (name, d, t, "Round Tube Profile")

        # describe points
        p1 = Point2D(r, 0)  # right middle
        p2 = Point2D(0, r)  # middle top
        p3 = Point2D(-r, 0) # left middle
        p4 = Point2D(0, -r) # middle bottom

        # describe curves
        l1 = Arc2D(p1, p2, p3)
        l2 = Arc2D(p3, p4, p1)

        self.curve = PolyCurve2D().byJoinedCurves([l1, l2])

        def __str__(self):
            return "Profile(" + f"{self.name})"


class LAngle:
    def __init__(self, name, h, b, tw, tf, r1, r2, ex, ey):
        self.Description = "LAngle"
        self.ID = "L"

        # parameters
        self.name = name
        self.curve = []
        self.b = b  # width
        self.h = h  # height
        self.tw = tw  # wall nominal thickness
        self.tf = tw
        self.r1 = r1  # inner fillet
        self.r11 = r1 / sqrt2
        self.r2 = r2  # outer fillet
        self.r21 = r2 / sqrt2
        self.ex = ex  # from left
        self.ey = ey  # from bottom

        # describe points
        p1 = Point2D(-ex, -ey)  # left bottom
        p2 = Point2D(b - ex, -ey)  # right bottom
        p3 = Point2D(b - ex, -ey + tf - r2)  # start arc
        p4 = Point2D(b - ex - r2 + self.r21, -ey + tf - r2 + self.r21)  # second point arc
        p5 = Point2D(b - ex - r2, -ey + tf)  # end arc
        p6 = Point2D(-ex + tf + r1, -ey + tf)  # start arc
        p7 = Point2D(-ex + tf + r1 - self.r11, -ey + tf + r1 - self.r11)  # second point arc
        p8 = Point2D(-ex + tf, -ey + tf + r1)  # end arc
        p9 = Point2D(-ex + tf, h - ey - r2)  # start arc
        p10 = Point2D(-ex + tf - r2 + self.r21, h - ey - r2 + self.r21)  # second point arc
        p11 = Point2D(-ex + tf - r2, h - ey)  # end arc
        p12 = Point2D(-ex, h - ey)  # left top

        # describe curves
        l1 = Line2D(p1, p2)
        l2 = Line2D(p2, p3)
        l3 = Arc2D(p3, p4, p5)
        l4 = Line2D(p5, p6)
        l5 = Arc2D(p6, p7, p8)
        l6 = Line2D(p8, p9)
        l7 = Arc2D(p9, p10, p11)
        l8 = Line2D(p11, p12)
        l9 = Line2D(p12, p1)

        self.curve = PolyCurve2D().byJoinedCurves([l1, l2, l3, l4, l5, l6, l7, l8, l9])

        def __str__(self):
            return "Profile(" + f"{self.name})"

class TProfile:
    #ToDo: inner outer fillets in polycurve
    def __init__(self, name, h, b, tw, tf, r, r1, r2, ex, ey):
        self.Description = "TProfile"
        self.ID = "T"

        # parameters
        self.name = name
        self.curve = []
        self.b = b  # width
        self.h = h  # height
        self.tw = tw  # wall nominal thickness
        self.tf = tw
        self.r = r  # inner fillet
        self.r01 = r/sqrt2
        self.r1 = r1  # outer fillet flange
        self.r11 = r1 / sqrt2
        self.r2 = r2  # outer fillet top web
        self.r21 = r2 / sqrt2
        self.ex = ex  # from left
        self.ey = ey  # from bottom

        # describe points
        p1 = Point2D(-ex, -ey)  # left bottom
        p2 = Point2D(b - ex, -ey)  # right bottom
        p3 = Point2D(b - ex, -ey + tf - r1)  # start arc
        p4 = Point2D(b - ex - r1 + self.r11, -ey + tf - r1 + self.r11)  # second point arc
        p5 = Point2D(b - ex - r1, -ey + tf)  # end arc
        p6 = Point2D(0.5 * tw + r, -ey + tf)  # start arc
        p7 = Point2D(0.5 * tw + r - self.r01, -ey + tf + r - self.r01)  # second point arc
        p8 = Point2D(0.5 * tw, -ey + tf + r)  # end arc
        p9 = Point2D(0.5 * tw, -ey + h - r2)  # start arc
        p10 = Point2D(0.5 * tw - self.r21, -ey + h - r2 + self.r21) # second point arc
        p11 = Point2D(0.5 * tw - r2, -ey + h)  # end arc

        p12 = Point2D(-p11.x,p11.y)
        p13 = Point2D(-p10.x, p10.y)
        p14 = Point2D(-p9.x, p9.y)
        p15 = Point2D(-p8.x, p8.y)
        p16 = Point2D(-p7.x, p7.y)
        p17 = Point2D(-p6.x, p6.y)
        p18 = Point2D(-p5.x, p5.y)
        p19 = Point2D(-p4.x, p4.y)
        p20 = Point2D(-p3.x, p3.y)

        # describe curves
        l1 = Line2D(p1, p2)

        l2 = Line2D(p2, p3)
        l3 = Arc2D(p3, p4, p5)
        l4 = Line2D(p5, p6)
        l5 = Arc2D(p6, p7, p8)
        l6 = Line2D(p8, p9)
        l7 = Arc2D(p9, p10, p11)
        l8 = Line2D(p11, p12)

        l9 = Arc2D(p12, p13, p14)
        l10 = Line2D(p14, p15)
        l11 = Arc2D(p15, p16, p17)
        l12 = Line2D(p17, p18)
        l13 = Arc2D(p18, p19, p20)
        l14 = Line2D(p20, p1)

        self.curve = PolyCurve2D().byJoinedCurves([l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12, l13, l14])

        def __str__(self):
            return "Profile(" + f"{self.name})"


class RectangleHollowSection:  #NOT COMPLETE YET
    def __init__(self, name, h, b, t, r1, r2):
        self.Description = "Rectangle Hollow Section"
        self.ID = "RHS"

        # parameters
        self.name = name
        self.curve = []
        self.h = h  # height
        self.b = b  # width
        self.t = t # thickness
        self.r1 = r1 # outer radius
        self.r2 = r2 # inner radius

        # describe points
        p1 = Point2D(b / 2, -h / 2)  # right bottom
        p2 = Point2D(b / 2, h / 2)  # right top
        p3 = Point2D(-b / 2, h / 2) # left top
        p4 = Point2D(-b / 2, -h / 2) # left bottom

        # describe curves
        l1 = Line2D(p1, p2)
        l2 = Line2D(p2, p3)
        l3 = Line2D(p3, p4)
        l4 = Line2D(p4, p1)

        self.curve = PolyCurve2D().byJoinedCurves([l1, l2, l3, l4])

        def __str__(self):
            return "Profile(" + f"{self.name})"
