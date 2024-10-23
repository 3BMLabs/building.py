# [included in BP singlefile]
# [!not included in BP singlefile - start]
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


"""This module provides classes for steel profiles
"""

__title__ = "profile"
__author__ = "Maarten & Jonathan"
__url__ = "./objects/profile.py"

import sys, os, math
from pathlib import Path

from abstract.serializable import Serializable
from geometry.curve import Line, PolyCurve
from geometry.point import Point
sys.path.append(str(Path(__file__).resolve().parents[1]))


# [!not included in BP singlefile - end]

sqrt2 = math.sqrt(2)


# Hierachie:
# point 2D
# line 2D
# PolyCurve2D 2D
# profile is een parametrische vorm heeft als resultaat een 2D curve
# section is een profiel met eigenschappen HEA200, 200,200,10,10,5 en eventuele rekenkundige eigenschappen.
# beam is een object wat in 3D zit met materiaal enz.

class Profile(Serializable):

    def __init__(self, name: str, description: str, IFC_profile_def: str, height: float, width: float,
                 tw: float = None, tf: float = None):
        """Creates a profile profile.

        Args:
            name (str): _description_
            description (str): _description_
            IFC_profile_def (str): _description_
            height (_type_): _description_
            width (_type_): _description_
        """

        self.IFC_profile_def = IFC_profile_def
        
        self.name = name
        self.description = description
        self.curve = []
        self.height = height
        self.width = width
        self.tw = tw
        self.tf = tf
        self.type = None

    def __str__(self):
        return f"{self.type} ({self.name})"

class CChannelParallelFlange(Profile):
    def __init__(self, name, height, width, tw, tf, r, ex):
        super().__init__(name, "C-channel with parallel flange", "IfcUShapeProfileDef", height, width, tw, tf)

        # parameters
        self.type = __class__.__name__

        self.r1 = r  # web fillet
        self.ex = ex  # centroid horizontal

        # describe points
        p1 = Point(-ex, -height / 2)  # left bottom
        p2 = Point(width - ex, -height / 2)  # right bottom
        p3 = Point(width - ex, -height / 2 + tf)
        p4 = Point(-ex + tw + r, -height / 2 + tf)  # start arc
        p5 = Point(-ex + tw + r, -height / 2 + tf + r)  # second point arc
        p6 = Point(-ex + tw, -height / 2 + tf + r)  # end arc
        p7 = Point(-ex + tw, height / 2 - tf - r)  # start arc
        p8 = Point(-ex + tw + r, height / 2 - tf - r)  # second point arc
        p9 = Point(-ex + tw + r, height / 2 - tf)  # end arc
        p10 = Point(width - ex, height / 2 - tf)
        p11 = Point(width - ex, height / 2)  # right top
        p12 = Point(-ex, height / 2)  # left top

        # describe curves
        l1 = Line(p1, p2)
        l2 = Line(p2, p3)
        l3 = Line(p3, p4)
        l4 = Arc2D(p4, p5, p6)
        l5 = Line(p6, p7)
        l6 = Arc2D(p7, p8, p9)
        l7 = Line(p9, p10)
        l8 = Line(p10, p11)
        l9 = Line(p11, p12)
        l10 = Line(p12, p1)

        self.curve = PolyCurve.by_joined_curves(
            [l1, l2, l3, l4, l5, l6, l7, l8, l9, l10])

class CChannelSlopedFlange(Profile):
    def __init__(self, name, height, width, tw, tf, r1, r2, tl, sa, ex):
        super().__init__(name, "C-channel with sloped flange", "IfcUShapeProfileDef", height, width, tw, tf)

        self.r1 = r1  # web fillet
        r11 = r1 / sqrt2
        self.r2 = r2  # flange fillet
        r21 = r2 / sqrt2
        self.tl = tl  # flange thickness location from right
        self.sa = math.radians(sa)  # the angle of sloped flange in degrees
        self.ex = ex  # centroid horizontal

        # describe points
        p1 = Point(-ex, -height / 2)  # left bottom
        p2 = Point(width - ex, -height / 2)  # right bottom
        p3 = Point(width - ex, -height / 2 + tf - math.tan(self.sa)
                     * tl - r2)  # start arc
        p4 = Point(width - ex - r2 + r21, -height / 2 + tf -
                     math.tan(self.sa) * tl - r2 + r21)  # second point arc
        p5 = Point(width - ex - r2 + math.sin(self.sa) * r2, -height /
                     2 + tf - math.tan(self.sa) * (tl - r2))  # end arc
        p6 = Point(-ex + tw + r1 - math.sin(self.sa) * r1, -height / 2 +
                     tf + math.tan(self.sa) * (width - tl - tw - r1))  # start arc
        p7 = Point(-ex + tw + r1 - r11, -height / 2 + tf + math.tan(self.sa)
                     * (width - tl - tw - r1) + r1 - r11)  # second point arc
        p8 = Point(-ex + tw, -height / 2 + tf + math.tan(self.sa)
                     * (width - tl - tw) + r1)  # end arc
        p9 = Point(p8.x, -p8.y)  # start arc
        p10 = Point(p7.x, -p7.y)  # second point arc
        p11 = Point(p6.x, -p6.y)  # end arc
        p12 = Point(p5.x, -p5.y)  # start arc
        p13 = Point(p4.x, -p4.y)  # second point arc
        p14 = Point(p3.x, -p3.y)  # end arc
        p15 = Point(p2.x, -p2.y)  # right top
        p16 = Point(p1.x, -p1.y)  # left top

        # describe curves
        l1 = Line(p1, p2)
        l2 = Line(p2, p3)
        l3 = Arc2D(p3, p4, p5)
        l4 = Line(p5, p6)
        l5 = Arc2D(p6, p7, p8)
        l6 = Line(p8, p9)
        l7 = Arc2D(p9, p10, p11)
        l8 = Line(p11, p12)
        l9 = Arc2D(p12, p13, p14)
        l10 = Line(p14, p15)
        l11 = Line(p15, p16)
        l12 = Line(p16, p1)

        self.curve = PolyCurve([l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12])

class IShapeParallelFlange(Profile):
    def __init__(self, name, height, width, tw, tf, r):
        super().__init__(name, "I Shape profile with parallel flange", "IfcUShapeProfileDef", height, width, tw,
                         tf)


        self.r = r  # web fillet
        self.r1 = r1 = r / sqrt2

        # describe points
        p1 = Point(width / 2, -height / 2)  # right bottom
        p2 = Point(width / 2, -height / 2 + tf)
        p3 = Point(tw / 2 + r, -height / 2 + tf)  # start arc
        # second point arc
        p4 = Point(tw / 2 + r - r1, (-height / 2 + tf + r - r1))
        p5 = Point(tw / 2, -height / 2 + tf + r)  # end arc
        p6 = Point(tw / 2, height / 2 - tf - r)  # start arc
        p7 = Point(tw / 2 + r - r1, height / 2 - tf - r + r1)  # second point arc
        p8 = Point(tw / 2 + r, height / 2 - tf)  # end arc
        p9 = Point(width / 2, height / 2 - tf)
        p10 = Point((width / 2), (height / 2))  # right top
        p11 = Point(-p10.x, p10.y)  # left top
        p12 = Point(-p9.x, p9.y)
        p13 = Point(-p8.x, p8.y)  # start arc
        p14 = Point(-p7.x, p7.y)  # second point arc
        p15 = Point(-p6.x, p6.y)  # end arc
        p16 = Point(-p5.x, p5.y)  # start arc
        p17 = Point(-p4.x, p4.y)  # second point arc
        p18 = Point(-p3.x, p3.y)  # end arc
        p19 = Point(-p2.x, p2.y)
        p20 = Point(-p1.x, p1.y)

        # describe curves
        l1 = Line(p1, p2)
        l2 = Line(p2, p3)
        l3 = Arc2D(p3, p4, p5)
        l4 = Line(p5, p6)
        l5 = Arc2D(p6, p7, p8)
        l6 = Line(p8, p9)
        l7 = Line(p9, p10)
        l8 = Line(p10, p11)
        l9 = Line(p11, p12)
        l10 = Line(p12, p13)
        l11 = Arc2D(p13, p14, p15)
        l12 = Line(p15, p16)
        l13 = Arc2D(p16, p17, p18)
        l14 = Line(p18, p19)
        l15 = Line(p19, p20)
        l16 = Line(p20, p1)

        self.curve = PolyCurve(
            [l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12, l13, l14, l15, l16])

class Rectangle(Profile):
    def __init__(self, name, width, height):
        super().__init__(name, "Rectangle", "IfcRectangleProfileDef", height, width)


        # describe points
        p1 = Point(width / 2, -height / 2)  # right bottom
        p2 = Point(width / 2, height / 2)  # right top
        p3 = Point(-width / 2, height / 2)  # left top
        p4 = Point(-width / 2, -height / 2)  # left bottom

        # describe curves
        l1 = Line(p1, p2)
        l2 = Line(p2, p3)
        l3 = Line(p3, p4)
        l4 = Line(p4, p1)

        self.curve = PolyCurve([l1, l2, l3, l4])

class Round(Profile):
    def __init__(self, name, r):
        super().__init__(name, "Round", "IfcCircleProfileDef", r*2, r*2)

        self.r = r

        dr = r / sqrt2  # grootste deel

        # describe points
        p1 = Point(r, 0)  # right middle
        p2 = Point(dr, dr)
        p3 = Point(0, r)  # middle top
        p4 = Point(-dr, dr)
        p5 = Point(-r, 0)  # left middle
        p6 = Point(-dr, -dr)
        p7 = Point(0, -r)  # middle bottom
        p8 = Point(dr, -dr)

        # describe curves
        l1 = Arc2D(p1, p2, p3)
        l2 = Arc2D(p3, p4, p5)
        l3 = Arc2D(p5, p6, p7)
        l4 = Arc2D(p7, p8, p1)

        self.curve = PolyCurve([l1, l2, l3, l4])

class Roundtube(Profile):
    def __init__(self, name, d, t):
        super().__init__(name, "Round Tube Profile", "IfcCircleHollowProfileDef", d, d)

        # parameters
        self.type = __class__.__name__
        self.r = d / 2
        self.d = d
        self.t = t  # wall thickness
        dr = self.r / sqrt2  # grootste deel
        r = self.r
        ri = r - t
        dri = ri / sqrt2

        # describe points
        p1 = Point(r, 0)  # right middle
        p2 = Point(dr, dr)
        p3 = Point(0, r)  # middle top
        p4 = Point(-dr, dr)
        p5 = Point(-r, 0)  # left middle
        p6 = Point(-dr, -dr)
        p7 = Point(0, -r)  # middle bottom
        p8 = Point(dr, -dr)

        p9 = Point(ri, 0)  # right middle inner
        p10 = Point(dri, dri)
        p11 = Point(0, ri)  # middle top inner
        p12 = Point(-dri, dri)
        p13 = Point(-ri, 0)  # left middle inner
        p14 = Point(-dri, -dri)
        p15 = Point(0, -ri)  # middle bottom inner
        p16 = Point(dri, -dri)

        # describe curves
        l1 = Arc2D(p1, p2, p3)
        l2 = Arc2D(p3, p4, p5)
        l3 = Arc2D(p5, p6, p7)
        l4 = Arc2D(p7, p8, p1)

        l5 = Line(p1, p9)

        l6 = Arc2D(p9, p10, p11)
        l7 = Arc2D(p11, p12, p13)
        l8 = Arc2D(p13, p14, p15)
        l9 = Arc2D(p15, p16, p9)
        l10 = Line(p9, p1)

        self.curve = PolyCurve(
            [l1, l2, l3, l4, l5, l6, l7, l8, l9, l10])

class LAngle(Profile):
    def __init__(self, name, height, width, tw, tf, r1, r2, ex, ey):
        super().__init__(name, "LAngle", "IfcLShapeProfileDef", height, width, tw, tf)

        # parameters
        self.type = __class__.__name__

        self.r1 = r1  # inner fillet
        r11 = r1 / sqrt2
        self.r2 = r2  # outer fillet
        r21 = r2 / sqrt2
        self.ex = ex  # from left
        self.ey = ey  # from bottom

        # describe points
        p1 = Point(-ex, -ey)  # left bottom
        p2 = Point(width - ex, -ey)  # right bottom
        p3 = Point(width - ex, -ey + tf - r2)  # start arc
        p4 = Point(width - ex - r2 + r21, -ey + tf -
                     r2 + r21)  # second point arc
        p5 = Point(width - ex - r2, -ey + tf)  # end arc
        p6 = Point(-ex + tf + r1, -ey + tf)  # start arc
        p7 = Point(-ex + tf + r1 - r11, -ey + tf +
                     r1 - r11)  # second point arc
        p8 = Point(-ex + tf, -ey + tf + r1)  # end arc
        p9 = Point(-ex + tf, height - ey - r2)  # start arc
        p10 = Point(-ex + tf - r2 + r21, height - ey -
                      r2 + r21)  # second point arc
        p11 = Point(-ex + tf - r2, height - ey)  # end arc
        p12 = Point(-ex, height - ey)  # left top

        # describe curves
        l1 = Line(p1, p2)
        l2 = Line(p2, p3)
        l3 = Arc2D(p3, p4, p5)
        l4 = Line(p5, p6)
        l5 = Arc2D(p6, p7, p8)
        l6 = Line(p8, p9)
        l7 = Arc2D(p9, p10, p11)
        l8 = Line(p11, p12)
        l9 = Line(p12, p1)

        self.curve = PolyCurve(
            [l1, l2, l3, l4, l5, l6, l7, l8, l9])

class TProfileRounded(Profile):
    # ToDo: inner outer fillets in polycurve
    def __init__(self, name, height, width, tw, tf, r, r1, r2, ex, ey):
        super().__init__(name, "TProfile", "IfcTShapeProfileDef", height, width, tw, tf)


        self.r = r  # inner fillet
        self.r01 = r / sqrt2
        self.r1 = r1  # outer fillet flange
        r11 = r1 / sqrt2
        self.r2 = r2  # outer fillet top web
        r21 = r2 / sqrt2
        self.ex = ex  # from left
        self.ey = ey  # from bottom

        # describe points
        p1 = Point(-ex, -ey)  # left bottom
        p2 = Point(width - ex, -ey)  # right bottom
        p3 = Point(width - ex, -ey + tf - r1)  # start arc
        p4 = Point(width - ex - r1 + r11, -ey + tf -
                     r1 + r11)  # second point arc
        p5 = Point(width - ex - r1, -ey + tf)  # end arc
        p6 = Point(0.5 * tw + r, -ey + tf)  # start arc
        p7 = Point(0.5 * tw + r - self.r01, -ey + tf +
                     r - self.r01)  # second point arc
        p8 = Point(0.5 * tw, -ey + tf + r)  # end arc
        p9 = Point(0.5 * tw, -ey + height - r2)  # start arc
        p10 = Point(0.5 * tw - r21, -ey + height -
                      r2 + r21)  # second point arc
        p11 = Point(0.5 * tw - r2, -ey + height)  # end arc

        p12 = Point(-p11.x, p11.y)
        p13 = Point(-p10.x, p10.y)
        p14 = Point(-p9.x, p9.y)
        p15 = Point(-p8.x, p8.y)
        p16 = Point(-p7.x, p7.y)
        p17 = Point(-p6.x, p6.y)
        p18 = Point(-p5.x, p5.y)
        p19 = Point(-p4.x, p4.y)
        p20 = Point(-p3.x, p3.y)

        # describe curves
        l1 = Line(p1, p2)

        l2 = Line(p2, p3)
        l3 = Arc2D(p3, p4, p5)
        l4 = Line(p5, p6)
        l5 = Arc2D(p6, p7, p8)
        l6 = Line(p8, p9)
        l7 = Arc2D(p9, p10, p11)
        l8 = Line(p11, p12)

        l9 = Arc2D(p12, p13, p14)
        l10 = Line(p14, p15)
        l11 = Arc2D(p15, p16, p17)
        l12 = Line(p17, p18)
        l13 = Arc2D(p18, p19, p20)
        l14 = Line(p20, p1)

        self.curve = PolyCurve(
            [l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12, l13, l14])

class RectangleHollowSection(Profile):
    def __init__(self, name, height, width, t, r1, r2):
        super().__init__(name, "Rectangle Hollow Section", "IfcRectangleHollowProfileDef", height, width, tw=t, tf=t)

        # parameters
        self.type = __class__.__name__

        self.t = t  # thickness
        self.r1 = r1  # outer radius
        self.r2 = r2  # inner radius
        dr = r1 - r1 / sqrt2
        dri = r2 - r2 / sqrt2
        bi = width - t
        hi = height - t

        # describe points
        p1 = Point(-width / 2 + r1, - height / 2)  # left bottom end arc
        p2 = Point(width / 2 - r1, - height / 2)  # right bottom start arc
        p3 = Point(width / 2 - dr, - height / 2 + dr)  # right bottom mid arc
        p4 = Point(width / 2, - height / 2 + r1)  # right bottom end arc
        p5 = Point(p4.x, -p4.y)  # right start arc
        p6 = Point(p3.x, -p3.y)  # right mid arc
        p7 = Point(p2.x, -p2.y)  # right end arc
        p8 = Point(-p7.x, p7.y)  # left start arc
        p9 = Point(-p6.x, p6.y)  # left mid arc
        p10 = Point(-p5.x, p5.y)  # left end arc
        p11 = Point(p10.x, -p10.y)  # right bottom start arc
        p12 = Point(p9.x, -p9.y)  # right bottom mid arc

        # inner part
        p13 = Point(-bi / 2 + r2, - hi / 2)  # left bottom end arc
        p14 = Point(bi / 2 - r2, - hi / 2)  # right bottom start arc
        p15 = Point(bi / 2 - dri, - hi / 2 + dri)  # right bottom mid arc
        p16 = Point(bi / 2, - hi / 2 + r2)  # right bottom end arc
        p17 = Point(p16.x, -p16.y)  # right start arc
        p18 = Point(p15.x, -p15.y)  # right mid arc
        p19 = Point(p14.x, -p14.y)  # right end arc
        p20 = Point(-p19.x, p19.y)  # left start arc
        p21 = Point(-p18.x, p18.y)  # left mid arc
        p22 = Point(-p17.x, p17.y)  # left end arc
        p23 = Point(p22.x, -p22.y)  # right bottom start arc
        p24 = Point(p21.x, -p21.y)  # right bottom mid arc

        # describe outer curves
        l1 = Line(p1, p2)
        l2 = Arc2D(p2, p3, p4)
        l3 = Line(p4, p5)
        l4 = Arc2D(p5, p6, p7)
        l5 = Line(p7, p8)
        l6 = Arc2D(p8, p9, p10)
        l7 = Line(p10, p11)
        l8 = Arc2D(p11, p12, p1)

        l9 = Line(p1, p13)
        # describe inner curves
        l10 = Line(p13, p14)
        l11 = Arc2D(p14, p15, p16)
        l12 = Line(p16, p17)
        l13 = Arc2D(p17, p18, p19)
        l14 = Line(p19, p20)
        l15 = Arc2D(p20, p21, p22)
        l16 = Line(p22, p23)
        l17 = Arc2D(p23, p24, p13)

        l18 = Line(p13, p1)

        self.curve = PolyCurve(
            [l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12, l13, l14, l15, l16, l17, l18])

class CProfile(Profile):
    def __init__(self, name, width, height, t, r1, ex):
        super().__init__(name, "Cold Formed C Profile", "Unknown", height, width, tw=t, tf=t)

        # parameters
        self.type = __class__.__name__

        self.t = t  # flange thickness
        self.r1 = r1  # outer radius
        self.r2 = r1 - t  # inner radius
        r2 = r1 - t

        self.ex = ex
        self.ey = height / 2
        dr = r1 - r1 / sqrt2
        dri = r2 - r2 / sqrt2
        hi = height - t

        # describe points
        p1 = Point(width - ex, -height / 2)  # right bottom
        p2 = Point(r1 - ex, -height / 2)
        p3 = Point(dr - ex, -height / 2 + dr)
        p4 = Point(0 - ex, -height / 2 + r1)
        p5 = Point(p4.x, -p4.y)
        p6 = Point(p3.x, -p3.y)
        p7 = Point(p2.x, -p2.y)
        p8 = Point(p1.x, -p1.y)  # right top
        p9 = Point(width - ex, hi / 2)  # right top inner
        p10 = Point(t + r2 - ex, hi / 2)
        p11 = Point(t + dri - ex, hi / 2 - dri)
        p12 = Point(t - ex, hi / 2 - r2)
        p13 = Point(p12.x, -p12.y)
        p14 = Point(p11.x, -p11.y)
        p15 = Point(p10.x, -p10.y)
        p16 = Point(p9.x, -p9.y)  # right bottom inner
        # describe outer curves
        l1 = Line(p1, p2)  # bottom
        l2 = Arc2D(p2, p3, p4)  # right outer fillet
        l3 = Line(p4, p5)  # left outer web
        l4 = Arc2D(p5, p6, p7)  # left top outer fillet
        l5 = Line(p7, p8)  # outer top
        l6 = Line(p8, p9)
        l7 = Line(p9, p10)
        l8 = Arc2D(p10, p11, p12)  # left top inner fillet
        l9 = Line(p12, p13)
        l10 = Arc2D(p13, p14, p15)  # left botom inner fillet
        l11 = Line(p15, p16)
        l12 = Line(p16, p1)

        self.curve = PolyCurve(
            [l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12])

class CProfileWithLips(Profile):
    def __init__(self, name, width, height, h1, t, r1, ex):
        super().__init__(name, "Cold Formed C Profile with Lips", "Unknown", height, width, tw=t, tf=t)

        # parameters
        self.type = __class__.__name__

        self.h1 = h1  # lip length
        self.t = t  # flange thickness
        self.r1 = r1  # outer radius
        self.r2 = r1 - t  # inner radius
        r2 = r1 - t

        self.ex = ex
        self.ey = height / 2
        dr = r1 - r1 / sqrt2
        dri = r2 - r2 / sqrt2
        hi = height - t

        # describe points
        p1 = Point(width - ex - r1, -height / 2)  # right bottom  before fillet
        p2 = Point(r1 - ex, -height / 2)
        p3 = Point(dr - ex, -height / 2 + dr)
        p4 = Point(0 - ex, -height / 2 + r1)
        p5 = Point(p4.x, -p4.y)
        p6 = Point(p3.x, -p3.y)
        p7 = Point(p2.x, -p2.y)
        p8 = Point(p1.x, -p1.y)  # right top before fillet
        p9 = Point(width - ex - dr, height / 2 - dr)  # middle point arc
        p10 = Point(width - ex, height / 2 - r1)  # end fillet
        p11 = Point(width - ex, height / 2 - h1)
        p12 = Point(width - ex - t, height / 2 - h1)  # bottom lip
        p13 = Point(width - ex - t, height / 2 - t - r2)  # start inner fillet right top
        p14 = Point(width - ex - t - dri, height / 2 - t - dri)
        p15 = Point(width - ex - t - r2, height / 2 - t)  # end inner fillet right top
        p16 = Point(0 - ex + t + r2, height / 2 - t)
        p17 = Point(0 - ex + t + dri, height / 2 - t - dri)
        p18 = Point(0 - ex + t, height / 2 - t - r2)

        p19 = Point(p18.x, -p18.y)
        p20 = Point(p17.x, -p17.y)
        p21 = Point(p16.x, -p16.y)
        p22 = Point(p15.x, -p15.y)
        p23 = Point(p14.x, -p14.y)
        p24 = Point(p13.x, -p13.y)
        p25 = Point(p12.x, -p12.y)
        p26 = Point(p11.x, -p11.y)
        p27 = Point(p10.x, -p10.y)
        p28 = Point(p9.x, -p9.y)

        # describe outer curves
        l1 = Line(p1, p2)
        l2 = Arc2D(p2, p3, p4)
        l3 = Line(p4, p5)
        l4 = Arc2D(p5, p6, p7)  # outer fillet right top
        l5 = Line(p7, p8)
        l6 = Arc2D(p8, p9, p10)
        l7 = Line(p10, p11)
        l8 = Line(p11, p12)
        l9 = Line(p12, p13)
        l10 = Arc2D(p13, p14, p15)
        l11 = Line(p15, p16)
        l12 = Arc2D(p16, p17, p18)
        l13 = Line(p18, p19)  # inner web
        l14 = Arc2D(p19, p20, p21)
        l15 = Line(p21, p22)
        l16 = Arc2D(p22, p23, p24)
        l17 = Line(p24, p25)
        l18 = Line(p25, p26)
        l19 = Line(p26, p27)
        l20 = Arc2D(p27, p28, p1)

        self.curve = PolyCurve(
            [l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12, l13, l14, l15, l16, l17, l18, l19, l20])

class LProfileColdFormed(Profile):
    def __init__(self, name, width, height, t, r1, ex, ey):
        super().__init__(name, "Cold Formed L Profile", "Unknown", height, width, tw=t, tf=t)

        # parameters
        self.type = __class__.__name__

        self.t = t  # flange thickness
        self.r1 = r1  # inner radius
        self.r2 = r1 - t  # outer radius
        self.ex = ex
        self.ey = ey
        r11 = r1 / math.sqrt(2)
        r2 = r1 + t
        r21 = r2 / math.sqrt(2)

        # describe points
        p1 = Point(-ex, -ey + r2)  # start arc left bottom
        p2 = Point(-ex + r2 - r21, -ey + r2 - r21)  # second point arc
        p3 = Point(-ex + r2, -ey)  # end arc
        p4 = Point(width - ex, -ey)  # right bottom
        p5 = Point(width - ex, -ey + t)
        p6 = Point(-ex + t + r1, -ey + t)  # start arc
        p7 = Point(-ex + t + r1 - r11, -ey + t +
                     r1 - r11)  # second point arc
        p8 = Point(-ex + t, -ey + t + r1)  # end arc
        p9 = Point(-ex + t, ey)
        p10 = Point(-ex, ey)  # left top

        l1 = Arc2D(p1, p2, p3)
        l2 = Line(p3, p4)
        l3 = Line(p4, p5)
        l4 = Line(p5, p6)
        l5 = Arc2D(p6, p7, p8)
        l6 = Line(p8, p9)
        l7 = Line(p9, p10)
        l8 = Line(p10, p1)

        self.curve = PolyCurve(
            [l1, l2, l3, l4, l5, l6, l7, l8])

class SigmaProfileWithLipsColdFormed(Profile):
    def __init__(self, name, width, height, t, r1, h1, h2, h3, b2, ex):
        super().__init__(name, "Cold Formed Sigma Profile with Lips", "Unknown", height, width, tw=t, tf=t)

        # parameters
        self.type = __class__.__name__

        self.h1 = h1  # LipLength
        self.h2 = h2  # MiddleBendLength
        self.h3 = h3  # TopBendLength
        self.h4 = h4 = (height - h2 - h3 * 2) / 2
        self.h5 = h5 = math.tan(0.5 * math.atan(b2 / h4)) * t
        self.b2 = b2  # MiddleBendWidth
        self.t = t  # flange thickness
        self.r1 = r1  # inner radius
        self.r2 = r2 = r1 + t  # outer radius
        self.ex = ex
        self.ey = ey = height / 2
        r11 = r11 = r1 / math.sqrt(2)
        r21 = r21 = r2 / math.sqrt(2)

        p1 = Point(-ex + b2, -h2 / 2)
        p2 = Point(-ex, -ey + h3)
        p3 = Point(-ex, -ey + r2)  # start arc left bottom
        p4 = Point(-ex + r2 - r21, -ey + r2 - r21)  # second point arc
        p5 = Point(-ex + r2, -ey)  # end arc
        p6 = Point(width - ex - r2, -ey)  # start arc
        p7 = Point(width - ex - r2 + r21, -ey + r2 - r21)  # second point arc
        p8 = Point(width - ex, -ey + r2)  # end arc
        p9 = Point(width - ex, -ey + h1)  # end lip
        p10 = Point(width - ex - t, -ey + h1)
        p11 = Point(width - ex - t, -ey + t + r1)  # start arc
        p12 = Point(width - ex - t - r1 + r11, -ey +
                      t + r1 - r11)  # second point arc
        p13 = Point(width - ex - t - r1, -ey + t)  # end arc
        p14 = Point(-ex + t + r1, -ey + t)  # start arc
        p15 = Point(-ex + t + r1 - r11, -ey + t +
                      r1 - r11)  # second point arc
        p16 = Point(-ex + t, -ey + t + r1)  # end arc
        p17 = Point(-ex + t, -ey + h3 - h5)
        p18 = Point(-ex + b2 + t, -h2 / 2 - h5)
        p19 = Point(p18.x, -p18.y)
        p20 = Point(p17.x, -p17.y)
        p21 = Point(p16.x, -p16.y)
        p22 = Point(p15.x, -p15.y)
        p23 = Point(p14.x, -p14.y)
        p24 = Point(p13.x, -p13.y)
        p25 = Point(p12.x, -p12.y)
        p26 = Point(p11.x, -p11.y)
        p27 = Point(p10.x, -p10.y)
        p28 = Point(p9.x, -p9.y)
        p29 = Point(p8.x, -p8.y)
        p30 = Point(p7.x, -p7.y)
        p31 = Point(p6.x, -p6.y)
        p32 = Point(p5.x, -p5.y)
        p33 = Point(p4.x, -p4.y)
        p34 = Point(p3.x, -p3.y)
        p35 = Point(p2.x, -p2.y)
        p36 = Point(p1.x, -p1.y)

        l1 = Line(p1, p2)
        l2 = Line(p2, p3)
        l3 = Arc2D(p3, p4, p5)
        l4 = Line(p5, p6)
        l5 = Arc2D(p6, p7, p8)
        l6 = Line(p8, p9)
        l7 = Line(p9, p10)
        l8 = Line(p10, p11)
        l9 = Arc2D(p11, p12, p13)
        l10 = Line(p13, p14)
        l11 = Arc2D(p14, p15, p16)
        l12 = Line(p16, p17)
        l13 = Line(p17, p18)
        l14 = Line(p18, p19)
        l15 = Line(p19, p20)
        l16 = Line(p20, p21)
        l17 = Arc2D(p21, p22, p23)
        l18 = Line(p23, p24)
        l19 = Arc2D(p24, p25, p26)
        l20 = Line(p26, p27)
        l21 = Line(p27, p28)
        l22 = Line(p28, p29)
        l23 = Arc2D(p29, p30, p31)
        l24 = Line(p31, p32)
        l25 = Arc2D(p32, p33, p34)
        l26 = Line(p34, p35)
        l27 = Line(p35, p36)
        l28 = Line(p36, p1)

        self.curve = PolyCurve(
            [l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12, l13, l14, l15, l16, l17, l18, l19, l20, l21, l22, l23,
             l24, l25,
             l26, l27, l28])

class ZProfileColdFormed(Profile):
    def __init__(self, name, width, height, t, r1):
        super().__init__(name, "Cold Formed Z Profile", "Unknown", height, width, tw=t, tf=t)

        # parameters
        self.type = __class__.__name__

        self.t = t  # flange thickness
        self.r1 = r1  # inner radius
        self.r2 = r2 = r1 + t  # outer radius
        self.ex = ex = width / 2
        self.ey = ey = height / 2
        r11 = r11 = r1 / math.sqrt(2)
        r21 = r21 = r2 / math.sqrt(2)

        p1 = Point(-0.5 * t, -ey + t + r1)  # start arc
        p2 = Point(-0.5 * t - r1 + r11, -ey + t +
                     r1 - r11)  # second point arc
        p3 = Point(-0.5 * t - r1, -ey + t)  # end arc
        p4 = Point(-ex, -ey + t)
        p5 = Point(-ex, -ey)  # left bottom
        p6 = Point(-r2 + 0.5 * t, -ey)  # start arc
        p7 = Point(-r2 + 0.5 * t + r21, -ey + r2 - r21)  # second point arc
        p8 = Point(0.5 * t, -ey + r2)  # end arc
        p9 = Point(-p1.x, -p1.y)
        p10 = Point(-p2.x, -p2.y)
        p11 = Point(-p3.x, -p3.y)
        p12 = Point(-p4.x, -p4.y)
        p13 = Point(-p5.x, -p5.y)
        p14 = Point(-p6.x, -p6.y)
        p15 = Point(-p7.x, -p7.y)
        p16 = Point(-p8.x, -p8.y)

        l1 = Arc2D(p1, p2, p3)
        l2 = Line(p3, p4)
        l3 = Line(p4, p5)
        l4 = Line(p5, p6)
        l5 = Arc2D(p6, p7, p8)
        l6 = Line(p8, p9)
        l7 = Arc2D(p9, p10, p11)
        l8 = Line(p11, p12)
        l9 = Line(p12, p13)
        l10 = Line(p13, p14)
        l11 = Arc2D(p14, p15, p16)
        l12 = Line(p16, p1)

        self.curve = PolyCurve(
            [l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12])

class ZProfileWithLipsColdFormed(Profile):
    def __init__(self, name, width, height, t, r1, h1):
        super().__init__(name, "Cold Formed Z Profile with Lips", "Unknown", height, width, tw=t, tf=t)

        # parameters
        self.type = __class__.__name__

        self.t = t  # flange thickness
        self.h1 = h1  # lip length
        self.r1 = r1  # inner radius
        self.r2 = r2 = r1 + t  # outer radius
        self.ex = ex = width / 2
        self.ey = ey = height / 2
        r11 = r11 = r1 / math.sqrt(2)
        r21 = r21 = r2 / math.sqrt(2)

        p1 = Point(-0.5 * t, -ey + t + r1)  # start arc
        p2 = Point(-0.5 * t - r1 + r11, -ey + t + r1 - r11)  # second point arc
        p3 = Point(-0.5 * t - r1, -ey + t)  # end arc
        p4 = Point(-ex + t + r1, -ey + t)  # start arc
        p5 = Point(-ex + t + r1 - r11, -ey + t + r1 - r11)  # second point arc
        p6 = Point(-ex + t, -ey + t + r1)  # end arc
        p7 = Point(-ex + t, -ey + h1)
        p8 = Point(-ex, -ey + h1)
        p9 = Point(-ex, -ey + r2)  # start arc
        p10 = Point(-ex + r2 - r21, -ey + r2 - r21)  # second point arc
        p11 = Point(-ex + r2, -ey)  # end arc
        p12 = Point(-r2 + 0.5 * t, -ey)  # start arc
        p13 = Point(-r2 + 0.5 * t + r21, -ey + r2 - r21)  # second point arc
        p14 = Point(0.5 * t, -ey + r2)  # end arc
        p15 = Point(-p1.x, -p1.y)
        p16 = Point(-p2.x, -p2.y)
        p17 = Point(-p3.x, -p3.y)
        p18 = Point(-p4.x, -p4.y)
        p19 = Point(-p5.x, -p5.y)
        p20 = Point(-p6.x, -p6.y)
        p21 = Point(-p7.x, -p7.y)
        p22 = Point(-p8.x, -p8.y)
        p23 = Point(-p9.x, -p9.y)
        p24 = Point(-p10.x, -p10.y)
        p25 = Point(-p11.x, -p11.y)
        p26 = Point(-p12.x, -p12.y)
        p27 = Point(-p13.x, -p13.y)
        p28 = Point(-p14.x, -p14.y)

        l1 = Arc2D(p1, p2, p3)
        l2 = Line(p3, p4)
        l3 = Arc2D(p4, p5, p6)
        l4 = Line(p6, p7)
        l5 = Line(p7, p8)
        l6 = Line(p8, p9)
        l7 = Arc2D(p9, p10, p11)
        l8 = Line(p11, p12)
        l9 = Arc2D(p12, p13, p14)
        l10 = Line(p14, p15)
        l11 = Arc2D(p15, p16, p17)
        l12 = Line(p17, p18)
        l13 = Arc2D(p18, p19, p20)
        l14 = Line(p20, p21)
        l15 = Line(p21, p22)
        l16 = Line(p22, p23)
        l17 = Arc2D(p23, p24, p25)
        l18 = Line(p25, p26)
        l19 = Arc2D(p26, p27, p28)
        l20 = Line(p28, p1)

        self.curve = PolyCurve(
            [l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12, l13, l14, l15, l16, l17, l18, l19, l20])

class TProfile(Profile):
    def __init__(self, name, height, width, h1:float, b1:float):
        super().__init__(name, "T-profile", "Unknown", height, width)

        # parameters
        self.type = __class__.__name__
        self.h1 = h1
        self.b1 = b1

        # describe points
        p1 = Point(b1 / 2, -height / 2)  # right bottom
        p2 = Point(b1 / 2, height / 2 - h1)  # right middle 1
        p3 = Point(width / 2, height / 2 - h1)  # right middle 2
        p4 = Point(width / 2, height / 2)  # right top
        p5 = Point(-width / 2, height / 2)  # left top
        p6 = Point(-width / 2, height / 2 - h1)  # left middle 2
        p7 = Point(-b1 / 2, height / 2 - h1)  # left middle 1
        p8 = Point(-b1 / 2, -height / 2)  # left bottom

        # describe curves
        l1 = Line(p1, p2)
        l2 = Line(p2, p3)
        l3 = Line(p3, p4)
        l4 = Line(p4, p5)
        l5 = Line(p5, p6)
        l6 = Line(p6, p7)
        l7 = Line(p7, p8)
        l8 = Line(p8, p1)

        self.curve = PolyCurve(
            [l1, l2, l3, l4, l5, l6, l7, l8])

class LProfile(Profile):
    def __init__(self, name, height, width, h1:float, b1:float):
        super().__init__(name, "L-profile", "Unknown", height, width)

        # parameters
        self.type = __class__.__name__
        self.h1 = h1
        self.b1 = b1

        # describe points
        p1 = Point(width / 2, -height / 2)  # right bottom
        p2 = Point(width / 2, -height / 2 + h1)  # right middle
        p3 = Point(-width / 2 + b1, -height / 2 + h1)  # middle
        p4 = Point(-width / 2 + b1, height / 2)  # middle top
        p5 = Point(-width / 2, height / 2)  # left top
        p6 = Point(-width / 2, -height / 2)  # left bottom

        # describe curves
        l1 = Line(p1, p2)
        l2 = Line(p2, p3)
        l3 = Line(p3, p4)
        l4 = Line(p4, p5)
        l5 = Line(p5, p6)
        l6 = Line(p6, p1)

        self.curve = PolyCurve([l1, l2, l3, l4, l5, l6])

class EProfile(Serializable):
    def __init__(self, name, height, width, h1):
        super().__init__(name, "E-profile", "Unknown", height, width)

        # parameters
        self.type = __class__.__name__
        self.h1 = h1

        # describe points
        p1 = Point(width / 2, -height / 2)  # right bottom
        p2 = Point(width / 2, -height / 2 + h1)
        p3 = Point(-width / 2 + h1, -height / 2 + h1)
        p4 = Point(-width / 2 + h1, -h1 / 2)
        p5 = Point(width / 2, -h1 / 2)
        p6 = Point(width / 2, h1 / 2)
        p7 = Point(-width / 2 + h1, h1 / 2)
        p8 = Point(-width / 2 + h1, height / 2 - h1)
        p9 = Point(width / 2, height / 2 - h1)
        p10 = Point(width / 2, height / 2)
        p11 = Point(-width / 2, height / 2)
        p12 = Point(-width / 2, -height / 2)

        # describe curves
        l1 = Line(p1, p2)
        l2 = Line(p2, p3)
        l3 = Line(p3, p4)
        l4 = Line(p4, p5)
        l5 = Line(p5, p6)
        l6 = Line(p6, p7)
        l7 = Line(p7, p8)
        l8 = Line(p8, p9)
        l9 = Line(p9, p10)
        l10 = Line(p10, p11)
        l11 = Line(p11, p12)
        l12 = Line(p12, p1)

        self.curve = PolyCurve(
            [l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12])

class NProfile(Serializable):
    def __init__(self, name, height, width, b1):
        super().__init__(name, "N-profile", "Unknown", height, width)

        # parameters
        self.type = __class__.__name__
        self.b1 = b1

        # describe points
        p1 = Point(width / 2, -height / 2)  # right bottom
        p2 = Point(width / 2, height / 2)
        p3 = Point(width / 2 - b1, height / 2)
        p4 = Point(width / 2 - b1, -height / 2 + b1 * 2)
        p5 = Point(-width / 2 + b1, height / 2)
        p6 = Point(-width / 2, height / 2)
        p7 = Point(-width / 2, -height / 2)
        p8 = Point(-width / 2 + b1, -height / 2)
        p9 = Point(-width / 2 + b1, height / 2 - b1 * 2)
        p10 = Point(width / 2 - b1, -height / 2)

        # describe curves
        l1 = Line(p1, p2)
        l2 = Line(p2, p3)
        l3 = Line(p3, p4)
        l4 = Line(p4, p5)
        l5 = Line(p5, p6)
        l6 = Line(p6, p7)
        l7 = Line(p7, p8)
        l8 = Line(p8, p9)
        l9 = Line(p9, p10)
        l10 = Line(p10, p1)

        self.curve = PolyCurve(
            [l1, l2, l3, l4, l5, l6, l7, l8, l9, l10])


class ArrowProfile(Profile):
    def __init__(self, name, length, width, b1, l1):
        super().__init__(name, "Arrow-profile", "Unknown", length, width)
        
        # parameters
        
        self.length = length  # length
        self.b1 = b1
        self.l1 = l1

        # describe points
        p1 = Point(0, length / 2)  # top middle
        p2 = Point(width / 2, -length / 2 + l1)
        # p3 = Point(b1 / 2, -length / 2 + l1)
        p3 = Point(b1 / 2, (-length / 2 + l1) + (length / 2) / 4)
        p4 = Point(b1 / 2, -length / 2)
        p5 = Point(-b1 / 2, -length / 2)
        # p6 = Point(-b1 / 2, -length / 2 + l1)
        p6 = Point(-b1 / 2, (-length / 2 + l1) + (length / 2) / 4)
        p7 = Point(-width / 2, -length / 2 + l1)

        # describe curves
        l1 = Line(p1, p2)
        l2 = Line(p2, p3)
        l3 = Line(p3, p4)
        l4 = Line(p4, p5)
        l5 = Line(p5, p6)
        l6 = Line(p6, p7)
        l7 = Line(p7, p1)

        self.curve = PolyCurve(
            [l1, l2, l3, l4, l5, l6, l7])
