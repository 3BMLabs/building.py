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


"""This module provides classes for steel shapes
"""

__title__ = "shape"
__author__ = "Maarten & Jonathan"
__url__ = "./objects/steel_shapes.py"

import sys, math
from pathlib import Path
from objects.frame import *
from objects.shape import RectangularShape, Shape

sys.path.append(str(Path(__file__).resolve().parents[1]))

from geometry.geometry2d import *

# [!not included in BP singlefile - end]

sqrt2 = math.sqrt(2)

# Hierachie:
# point 2D
# line 2D
# PolyCurve2D 2D
# shape is een parametrische vorm heeft als resultaat een 2D curve
# section is een profiel met eigenschappen HEA200, 200,200,10,10,5 en eventuele rekenkundige eigenschappen.
# beam is een object wat in 3D zit met materiaal enz.

class SteelShape(Shape):
    def __init__(self, IFC_profile_def:string, **kwargs):
        """Creates a steelshape.

        Args:
            name (string): _description_
            description (string): _description_
            IFC_profile_def (string): _description_
            ID (_type_): HEA, IPE, HEB, HEM etc.
            height (_type_): _description_
            width (_type_): _description_
        """
        super().__init__(**kwargs)
        self.IFC_profile_def = IFC_profile_def

class RectangularSteelShape(SteelShape, RectangularShape):
    def __init__(self, ID, name: string, description:string, IFC_profile_def:string, height, width):
        super().__init__(ID=ID, name=name, description=description, IFC_profile_def=IFC_profile_def, height=height, width=width)

class CircularSteelShape(SteelShape):
    def __init__(self, ID, name: string, description:string, IFC_profile_def:string, r):
        """Creates a steelshape.

        Args:
            name (string): _description_
            description (string): _description_
            IFC_profile_def (string): _description_
            ID (_type_): HEA, IPE, HEB, HEM etc.
            height (_type_): _description_
            width (_type_): _description_
        """
        super().__init__(ID, name,description, IFC_profile_def)
        self.r = r
    
class Flange(RectangularSteelShape):
    def __init__(self, name: string, description: string, IFC_profile_def: string, ID, height, width, tw, tf):
        super().__init__(ID, name,description, IFC_profile_def, height, width)
        self.tw = tw  # web thickness
        self.tf = tf  # flange thickness

class CChannelParallelFlange(Flange):
    def __init__(self, name, height, width, tw, tf, r, ex):
        super().__init__("C_PF", name,"C-channel with parallel flange", "IfcUShapeProfileDef", height, width, tw, tf)

        # parameters
        self.type = __class__.__name__
        
        
        self.r1 = r  # web fillet
        self.ex = ex  # centroid horizontal

        # describe points
        p1 = Point2D(-ex, -height / 2)  # left bottom
        p2 = Point2D(width - ex, -height / 2)  # right bottom
        p3 = Point2D(width - ex, -height / 2 + tf)
        p4 = Point2D(-ex + tw + r, -height / 2 + tf)  # start arc
        p5 = Point2D(-ex + tw + r, -height / 2 + tf + r)  # second point arc
        p6 = Point2D(-ex + tw, -height / 2 + tf + r)  # end arc
        p7 = Point2D(-ex + tw, height / 2 - tf - r)  # start arc
        p8 = Point2D(-ex + tw + r, height / 2 - tf - r)  # second point arc
        p9 = Point2D(-ex + tw + r, height / 2 - tf)  # end arc
        p10 = Point2D(width - ex, height / 2 - tf)
        p11 = Point2D(width - ex, height / 2)  # right top
        p12 = Point2D(-ex, height / 2)  # left top

        # describe curves
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

        self.curve = PolyCurve2D().by_joined_curves(
            [l1, l2, l3, l4, l5, l6, l7, l8, l9, l10])

    def serialize(self):
        return {
            'id': self.id,
            'type': self.type,
            'Description': self.Description,
            'ID': self.ID,
            'name': self.name,
            'height': self.height,
            'width': self.width,
            'tw': self.tw,
            'tf': self.tf,
            'r1': self.r1,
            'ex': self.ex,
            'curve': self.curve.serialize() if self.curve else None
        }

    @staticmethod
    def deserialize(data):
        c_channel = CChannelParallelFlange(
            name=data.get('name'),
            height=data.get('height'),
            width=data.get('width'),
            tw=data.get('tw'),
            tf=data.get('tf'),
            r=data.get('r1'),
            ex=data.get('ex')
        )

        c_channel.Description = data.get(
            'Description', "C-channel with parallel flange")
        c_channel.ID = data.get('ID', "C_PF")
        c_channel.curve = PolyCurve2D.deserialize(
            data['curve']) if 'curve' in data else None

        return c_channel

    def __str__(self):
        return f"{self.type} ({self.name})"


class CChannelSlopedFlange(Flange):
    def __init__(self, name, height, width, tw, tf, r1, r2, tl, sa, ex):
        super().__init__(name,"C-channel with sloped flange", "IfcUShapeProfileDef", "C_SF", height, width, tw, tf)
        self.type = __class__.__name__
        
        
        self.r1 = r1  # web fillet
        self.r11 = r1 / sqrt2
        self.r2 = r2  # flange fillet
        self.r21 = r2 / sqrt2
        self.tl = tl  # flange thickness location from right
        self.sa = math.radians(sa)  # the angle of sloped flange in degrees
        self.ex = ex  # centroid horizontal
        self.IFC_profile_def = "IfcUShapeProfileDef"

        # describe points
        p1 = Point2D(-ex, -height / 2)  # left bottom
        p2 = Point2D(width - ex, -height / 2)  # right bottom
        p3 = Point2D(width - ex, -height / 2 + tf - math.tan(self.sa)
                     * tl - r2)  # start arc
        p4 = Point2D(width - ex - r2 + self.r21, -height / 2 + tf -
                     math.tan(self.sa) * tl - r2 + self.r21)  # second point arc
        p5 = Point2D(width - ex - r2 + math.sin(self.sa) * r2, -height /
                     2 + tf - math.tan(self.sa) * (tl - r2))  # end arc
        p6 = Point2D(-ex + tw + r1 - math.sin(self.sa) * r1, -height / 2 +
                     tf + math.tan(self.sa) * (width - tl - tw - r1))  # start arc
        p7 = Point2D(-ex + tw + r1 - self.r11, -height / 2 + tf + math.tan(self.sa)
                     * (width - tl - tw - r1) + r1 - self.r11)  # second point arc
        p8 = Point2D(-ex + tw, -height / 2 + tf + math.tan(self.sa)
                     * (width - tl - tw) + r1)  # end arc
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

        self.curve = PolyCurve2D().by_joined_curves(
            [l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12])

    def serialize(self):
        return {
            'Description': self.Description,
            'ID': self.ID,
            'id': self.id,
            'type': self.type,
            'name': self.name,
            'height': self.height,
            'width': self.width,
            'tw': self.tw,
            'tf': self.tf,
            'r1': self.r1,
            'r11': self.r11,
            'r2': self.r2,
            'r21': self.r21,
            'tl': self.tl,
            'sa': self.sa,
            'ex': self.ex,
            'curve': self.curve.serialize() if self.curve else None
        }

    @staticmethod
    def deserialize(data):
        c_channel_sf = CChannelSlopedFlange(
            name=data.get('name'),
            height=data.get('height'),
            width=data.get('width'),
            tw=data.get('tw'),
            tf=data.get('tf'),
            r1=data.get('r1'),
            r2=data.get('r2'),
            tl=data.get('tl'),
            sa=data.get('sa'),
            ex=data.get('ex')
        )

        c_channel_sf.Description = data.get(
            'Description', "C-channel with sloped flange")
        c_channel_sf.ID = data.get('ID', "C_SF")
        c_channel_sf.id = data.get('id')
        c_channel_sf.type = data.get('type')
        c_channel_sf.curve = PolyCurve2D.deserialize(
            data['curve']) if 'curve' in data else None

        return c_channel_sf

    def __str__(self):
        return f"{self.type} ({self.name})"


class IShapeParallelFlange(Flange):
    def __init__(self, name, height, width, tw, tf, r):
        super().__init__(name,"I Shape profile with parallel flange", "IfcUShapeProfileDef", "I_PF", height, width, tw, tf)

        self.type = __class__.__name__
        
        self.r = r  # web fillet
        self.r1 = r1 = r / sqrt2
        self.IFC_profile_def = "IfcIShapeProfileDef"

        # describe points
        p1 = Point2D(width / 2, -height / 2)  # right bottom
        p2 = Point2D(width / 2, -height / 2 + tf)
        p3 = Point2D(tw / 2 + r, -height / 2 + tf)  # start arc
        # second point arc
        p4 = Point2D(tw / 2 + r - r1, (-height / 2 + tf + r - r1))
        p5 = Point2D(tw / 2, -height / 2 + tf + r)  # end arc
        p6 = Point2D(tw / 2, height / 2 - tf - r)  # start arc
        p7 = Point2D(tw / 2 + r - r1, height / 2 - tf - r + r1)  # second point arc
        p8 = Point2D(tw / 2 + r, height / 2 - tf)  # end arc
        p9 = Point2D(width / 2, height / 2 - tf)
        p10 = Point2D((width / 2), (height / 2))  # right top
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

        self.curve = PolyCurve2D().by_joined_curves(
            [l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12, l13, l14, l15, l16])

    def serialize(self):
        return {
            'Description': self.Description,
            'ID': self.ID,
            'id': self.id,
            'type': self.type,
            'name': self.name,
            'height': self.height,
            'width': self.width,
            'tw': self.tw,
            'tf': self.tf,
            'r': self.r,
            'r1': self.r1,
            'curve': self.curve.serialize() if self.curve else None
        }

    @staticmethod
    def deserialize(data):
        i_shape_pf = IShapeParallelFlange(
            name=data.get('name'),
            height=data.get('height'),
            width=data.get('width'),
            tw=data.get('tw'),
            tf=data.get('tf'),
            r=data.get('r')
        )

        i_shape_pf.Description = data.get(
            'Description', "I Shape profile with parallel flange")
        i_shape_pf.ID = data.get('ID', "I_PF")
        i_shape_pf.id = data.get('id')
        i_shape_pf.type = data.get('type')
        i_shape_pf.r1 = data.get('r1')
        i_shape_pf.curve = PolyCurve2D.deserialize(
            data['curve']) if 'curve' in data else None

        return i_shape_pf

    def __str__(self):
        return f"{self.type} ({self.name})"


class Rectangle(RectangularSteelShape):
    def __init__(self, name, width, height):
        super().__init__(name, "Rectangle", "IfcRectangleProfileDef", "Rec", height, width)
        self.type = __class__.__name__

        # describe points
        p1 = Point2D(width / 2, -height / 2)  # right bottom
        p2 = Point2D(width / 2, height / 2)  # right top
        p3 = Point2D(-width / 2, height / 2)  # left top
        p4 = Point2D(-width / 2, -height / 2)  # left bottom

        # describe curves
        l1 = Line2D(p1, p2)
        l2 = Line2D(p2, p3)
        l3 = Line2D(p3, p4)
        l4 = Line2D(p4, p1)

        self.curve = PolyCurve2D().by_joined_curves([l1, l2, l3, l4])

    def serialize(self):
        return {
            'Description': self.Description,
            'ID': self.ID,
            'id': self.id,
            'type': self.type,
            'name': self.name,
            'height': self.height,
            'width': self.width,
            'curve': self.curve.serialize() if self.curve else None
        }

    @staticmethod
    def deserialize(data):
        rectangle = Rectangle(
            name=data.get('name'),
            width=data.get('width'),
            height=data.get('height')
        )

        rectangle.Description = data.get('Description', "Rectangle")
        rectangle.ID = data.get('ID', "Rec")
        rectangle.id = data.get('id')
        rectangle.type = data.get('type')
        rectangle.curve = PolyCurve2D.deserialize(
            data['curve']) if 'curve' in data else None

        return rectangle

    def __str__(self):
        return f"{self.type} ({self.name})"


class Round(CircularSteelShape):
    def __init__(self, name, r):
        super().__init__(name, "Round", "IfcRectangleProfileDef", "Rnd", r)

        self.type = __class__.__name__
       
        self.data = (name, r, "Round")
        dr = r / sqrt2  # grootste deel
        self.IFC_profile_def = "IfcCircleProfileDef"

        # describe points
        p1 = Point2D(r, 0)  # right middle
        p2 = Point2D(dr, dr)
        p3 = Point2D(0, r)  # middle top
        p4 = Point2D(-dr, dr)
        p5 = Point2D(-r, 0)  # left middle
        p6 = Point2D(-dr, -dr)
        p7 = Point2D(0, -r)  # middle bottom
        p8 = Point2D(dr, -dr)

        # describe curves
        l1 = Arc2D(p1, p2, p3)
        l2 = Arc2D(p3, p4, p5)
        l3 = Arc2D(p5, p6, p7)
        l4 = Arc2D(p7, p8, p1)

        self.curve = PolyCurve2D().by_joined_curves([l1, l2, l3, l4])

    def serialize(self):
        return {
            'Description': self.Description,
            'ID': self.ID,
            'id': self.id,
            'type': self.type,
            'name': self.name,
            'r': self.r,
            'data': self.data,
            'curve': self.curve.serialize() if self.curve else None
        }

    @staticmethod
    def deserialize(data):
        round_shape = Round(
            name=data.get('name'),
            r=data.get('r')
        )

        round_shape.Description = data.get('Description', "Round")
        round_shape.ID = data.get('ID', "Rnd")
        round_shape.id = data.get('id')
        round_shape.type = data.get('type')
        round_shape.data = data.get(
            'data', (data.get('name'), data.get('r'), "Round"))
        round_shape.curve = PolyCurve2D.deserialize(
            data['curve']) if 'curve' in data else None

        return round_shape

    def __str__(self):
        return f"{self.type} ({self.name})"


class Roundtube(CircularSteelShape):
    def __init__(self, name, d, t):
        super().__init__(name,"Round Tube Profile", "IfcCircleHollowProfileDef", "Tube", d / 2)

        # parameters
        self.id = generateID()
        self.type = __class__.__name__
        self.name = name
        
        self.d = d
        self.t = t  # wall thickness
        self.data = (name, d, t, "Round Tube Profile")
        dr = self.r / sqrt2  # grootste deel
        r = self.r
        ri = r-t
        dri = ri / sqrt2

        # describe points
        p1 = Point2D(r, 0)  # right middle
        p2 = Point2D(dr, dr)
        p3 = Point2D(0, r)  # middle top
        p4 = Point2D(-dr, dr)
        p5 = Point2D(-r, 0)  # left middle
        p6 = Point2D(-dr, -dr)
        p7 = Point2D(0, -r)  # middle bottom
        p8 = Point2D(dr, -dr)

        p9 = Point2D(ri, 0)  # right middle inner
        p10 = Point2D(dri, dri)
        p11 = Point2D(0, ri)  # middle top inner
        p12 = Point2D(-dri, dri)
        p13 = Point2D(-ri, 0)  # left middle inner
        p14 = Point2D(-dri, -dri)
        p15 = Point2D(0, -ri)  # middle bottom inner
        p16 = Point2D(dri, -dri)

        # describe curves
        l1 = Arc2D(p1, p2, p3)
        l2 = Arc2D(p3, p4, p5)
        l3 = Arc2D(p5, p6, p7)
        l4 = Arc2D(p7, p8, p1)

        l5 = Line2D(p1, p9)

        l6 = Arc2D(p9, p10, p11)
        l7 = Arc2D(p11, p12, p13)
        l8 = Arc2D(p13, p14, p15)
        l9 = Arc2D(p15, p16, p9)
        l10 = Line2D(p9, p1)

        self.curve = PolyCurve2D().by_joined_curves(
            [l1, l2, l3, l4, l5, l6, l7, l8, l9, l10])

    def serialize(self):
        return {
            'Description': self.Description,
            'ID': self.ID,
            'id': self.id,
            'type': self.type,
            'name': self.name,
            'd': self.d,
            'r': self.r,
            't': self.t,
            'data': self.data,
            'curve': self.curve.serialize() if self.curve else None
        }

    @staticmethod
    def deserialize(data):
        roundtube = Roundtube(
            name=data.get('name'),
            d=data.get('d'),
            t=data.get('t')
        )

        roundtube.Description = data.get('Description', "Round Tube Profile")
        roundtube.ID = data.get('ID', "Tube")
        roundtube.id = data.get('id')
        roundtube.type = data.get('type')
        roundtube.data = data.get('data', (data.get('name'), data.get(
            'd'), data.get('t'), "Round Tube Profile"))
        roundtube.curve = PolyCurve2D.deserialize(
            data['curve']) if 'curve' in data else None

        return roundtube

    def __str__(self):
        return f"{self.type} ({self.name})"


class LAngle(RectangularSteelShape):
    def __init__(self, name, height, width, tw, tf, r1, r2, ex, ey):
        super().__init__(name,"LAngle", "IfcLShapeProfileDef", "L", height, width)

        # parameters
        self.type = __class__.__name__
        
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
        p2 = Point2D(width - ex, -ey)  # right bottom
        p3 = Point2D(width - ex, -ey + tf - r2)  # start arc
        p4 = Point2D(width - ex - r2 + self.r21, -ey + tf -
                     r2 + self.r21)  # second point arc
        p5 = Point2D(width - ex - r2, -ey + tf)  # end arc
        p6 = Point2D(-ex + tf + r1, -ey + tf)  # start arc
        p7 = Point2D(-ex + tf + r1 - self.r11, -ey + tf +
                     r1 - self.r11)  # second point arc
        p8 = Point2D(-ex + tf, -ey + tf + r1)  # end arc
        p9 = Point2D(-ex + tf, height - ey - r2)  # start arc
        p10 = Point2D(-ex + tf - r2 + self.r21, height - ey -
                      r2 + self.r21)  # second point arc
        p11 = Point2D(-ex + tf - r2, height - ey)  # end arc
        p12 = Point2D(-ex, height - ey)  # left top

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

        self.curve = PolyCurve2D().by_joined_curves(
            [l1, l2, l3, l4, l5, l6, l7, l8, l9])

    def serialize(self):
        return {
            'Description': self.Description,
            'ID': self.ID,
            'id': self.id,
            'type': self.type,
            'name': self.name,
            'width': self.width,
            'height': self.height,
            'tw': self.tw,
            'tf': self.tf,
            'r1': self.r1,
            'r11': self.r11,
            'r2': self.r2,
            'r21': self.r21,
            'ex': self.ex,
            'ey': self.ey,
            'curve': self.curve.serialize() if self.curve else None
        }

    @staticmethod
    def deserialize(data):
        langle = LAngle(
            name=data.get('name'),
            height=data.get('height'),
            width=data.get('width'),
            tw=data.get('tw'),
            tf=data.get('tf'),
            r1=data.get('r1'),
            r2=data.get('r2'),
            ex=data.get('ex'),
            ey=data.get('ey')
        )

        langle.Description = data.get('Description', "LAngle")
        langle.ID = data.get('ID', "L")
        langle.id = data.get('id')
        langle.type = data.get('type')
        langle.r11 = data.get('r11')
        langle.r21 = data.get('r21')
        langle.curve = PolyCurve2D.deserialize(
            data['curve']) if 'curve' in data else None

        return langle

    def __str__(self):
        return f"{self.type} ({self.name})"


class TProfile(RectangularSteelShape):
    # ToDo: inner outer fillets in polycurve
    def __init__(self, name, height, width, tw, tf, r, r1, r2, ex, ey):
        super().__init__(name, "TProfile", "IfcTShapeProfileDef", "T", height,width)

        self.type = __class__.__name__
        
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
        p2 = Point2D(width - ex, -ey)  # right bottom
        p3 = Point2D(width - ex, -ey + tf - r1)  # start arc
        p4 = Point2D(width - ex - r1 + self.r11, -ey + tf -
                     r1 + self.r11)  # second point arc
        p5 = Point2D(width - ex - r1, -ey + tf)  # end arc
        p6 = Point2D(0.5 * tw + r, -ey + tf)  # start arc
        p7 = Point2D(0.5 * tw + r - self.r01, -ey + tf +
                     r - self.r01)  # second point arc
        p8 = Point2D(0.5 * tw, -ey + tf + r)  # end arc
        p9 = Point2D(0.5 * tw, -ey + height - r2)  # start arc
        p10 = Point2D(0.5 * tw - self.r21, -ey + height -
                      r2 + self.r21)  # second point arc
        p11 = Point2D(0.5 * tw - r2, -ey + height)  # end arc

        p12 = Point2D(-p11.x, p11.y)
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

        self.curve = PolyCurve2D().by_joined_curves(
            [l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12, l13, l14])

    def serialize(self):
        return {
            'Description': self.Description,
            'ID': self.ID,
            'id': self.id,
            'type': self.type,
            'name': self.name,
            'width': self.width,
            'height': self.height,
            'tw': self.tw,
            'tf': self.tf,
            'r': self.r,
            'r01': self.r01,
            'r1': self.r1,
            'r11': self.r11,
            'r2': self.r2,
            'r21': self.r21,
            'ex': self.ex,
            'ey': self.ey,
            'curve': self.curve.serialize() if self.curve else None
        }

    @staticmethod
    def deserialize(data):
        t_profile = TProfile(
            name=data.get('name'),
            height=data.get('height'),
            width=data.get('width'),
            tw=data.get('tw'),
            tf=data.get('tf'),
            r=data.get('r'),
            r1=data.get('r1'),
            r2=data.get('r2'),
            ex=data.get('ex'),
            ey=data.get('ey')
        )

        t_profile.Description = data.get('Description', "TProfile")
        t_profile.ID = data.get('ID', "T")
        t_profile.id = data.get('id')
        t_profile.type = data.get('type')
        t_profile.r01 = data.get('r01')
        t_profile.r11 = data.get('r11')
        t_profile.r21 = data.get('r21')
        t_profile.curve = PolyCurve2D.deserialize(
            data['curve']) if 'curve' in data else None

        return t_profile

    def __str__(self):
        return f"{self.type} ({self.name})"


class RectangleHollowSection(RectangularSteelShape):
    def __init__(self, name, height, width, t, r1, r2):
        super().__init__(name, "Rectangle Hollow Section", "IfcRectangleHollowProfileDef", "RHS", height,width)

        # parameters
        self.type = __class__.__name__
        
        self.t = t  # thickness
        self.r1 = r1  # outer radius
        self.r2 = r2  # inner radius
        dr = r1 - r1 / sqrt2
        dri = r2 - r2 / sqrt2
        bi = width-t
        hi = height-t

        # describe points
        p1 = Point2D(-width / 2 + r1, - height / 2)  # left bottom end arc
        p2 = Point2D(width / 2 - r1, - height / 2)  # right bottom start arc
        p3 = Point2D(width / 2 - dr, - height / 2 + dr)  # right bottom mid arc
        p4 = Point2D(width / 2, - height / 2 + r1)  # right bottom end arc
        p5 = Point2D(p4.x, -p4.y)  # right start arc
        p6 = Point2D(p3.x, -p3.y)  # right mid arc
        p7 = Point2D(p2.x, -p2.y)  # right end arc
        p8 = Point2D(-p7.x, p7.y)  # left start arc
        p9 = Point2D(-p6.x, p6.y)  # left mid arc
        p10 = Point2D(-p5.x, p5.y)  # left end arc
        p11 = Point2D(p10.x, -p10.y)  # right bottom start arc
        p12 = Point2D(p9.x, -p9.y)  # right bottom mid arc

        # inner part
        p13 = Point2D(-bi / 2 + r2, - hi / 2)  # left bottom end arc
        p14 = Point2D(bi / 2 - r2, - hi / 2)  # right bottom start arc
        p15 = Point2D(bi / 2 - dri, - hi / 2 + dri)  # right bottom mid arc
        p16 = Point2D(bi / 2, - hi / 2 + r2)  # right bottom end arc
        p17 = Point2D(p16.x, -p16.y)  # right start arc
        p18 = Point2D(p15.x, -p15.y)  # right mid arc
        p19 = Point2D(p14.x, -p14.y)  # right end arc
        p20 = Point2D(-p19.x, p19.y)  # left start arc
        p21 = Point2D(-p18.x, p18.y)  # left mid arc
        p22 = Point2D(-p17.x, p17.y)  # left end arc
        p23 = Point2D(p22.x, -p22.y)  # right bottom start arc
        p24 = Point2D(p21.x, -p21.y)  # right bottom mid arc

        # describe outer curves
        l1 = Line2D(p1, p2)
        l2 = Arc2D(p2, p3, p4)
        l3 = Line2D(p4, p5)
        l4 = Arc2D(p5, p6, p7)
        l5 = Line2D(p7, p8)
        l6 = Arc2D(p8, p9, p10)
        l7 = Line2D(p10, p11)
        l8 = Arc2D(p11, p12, p1)

        l9 = Line2D(p1, p13)
        # describe inner curves
        l10 = Line2D(p13, p14)
        l11 = Arc2D(p14, p15, p16)
        l12 = Line2D(p16, p17)
        l13 = Arc2D(p17, p18, p19)
        l14 = Line2D(p19, p20)
        l15 = Arc2D(p20, p21, p22)
        l16 = Line2D(p22, p23)
        l17 = Arc2D(p23, p24, p13)

        l18 = Line2D(p13, p1)

        self.curve = PolyCurve2D().by_joined_curves(
            [l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12, l13, l14, l15, l16, l17, l18])

    def serialize(self):
        return {
            'Description': self.Description,
            'ID': self.ID,
            'id': self.id,
            'type': self.type,
            'name': self.name,
            'height': self.height,
            'width': self.width,
            't': self.t,
            'r1': self.r1,
            'r2': self.r2,
            'curve': self.curve.serialize() if self.curve else None
        }

    @staticmethod
    def deserialize(data):
        rhs = RectangleHollowSection(
            name=data.get('name'),
            height=data.get('height'),
            width=data.get('width'),
            t=data.get('t'),
            r1=data.get('r1'),
            r2=data.get('r2')
        )

        rhs.Description = data.get('Description', "Rectangle Hollow Section")
        rhs.ID = data.get('ID', "RHS")
        rhs.id = data.get('id')
        rhs.type = data.get('type')
        rhs.curve = PolyCurve2D.deserialize(
            data['curve']) if 'curve' in data else None

        return rhs

    def __str__(self):
        return f"{self.type} ({self.name})"


class CProfile(RectangularSteelShape):
    def __init__(self, name, width, height, t, r1, ex):
        super().__init__(name, "Cold Formed C Profile", "Unknown", "CP", height,width)

        # parameters
        self.type = __class__.__name__
        
        self.t = t  # flange thickness
        self.r1 = r1  # outer radius
        self.r2 = r1-t  # inner radius
        r2 = r1-t

        self.ex = ex
        self.ey = height/2
        dr = r1 - r1/sqrt2
        dri = r2 - r2/sqrt2
        hi = height-t

        # describe points
        p1 = Point2D(width-ex, -height/2)  # right bottom
        p2 = Point2D(r1-ex, -height/2)
        p3 = Point2D(dr-ex, -height/2+dr)
        p4 = Point2D(0-ex, -height/2+r1)
        p5 = Point2D(p4.x, -p4.y)
        p6 = Point2D(p3.x, -p3.y)
        p7 = Point2D(p2.x, -p2.y)
        p8 = Point2D(p1.x, -p1.y)  # right top
        p9 = Point2D(width-ex, hi/2)  # right top inner
        p10 = Point2D(t+r2-ex, hi/2)
        p11 = Point2D(t+dri-ex, hi/2-dri)
        p12 = Point2D(t-ex, hi/2-r2)
        p13 = Point2D(p12.x, -p12.y)
        p14 = Point2D(p11.x, -p11.y)
        p15 = Point2D(p10.x, -p10.y)
        p16 = Point2D(p9.x, -p9.y)  # right bottom inner
        # describe outer curves
        l1 = Line2D(p1, p2)  # bottom
        l2 = Arc2D(p2, p3, p4)  # right outer fillet
        l3 = Line2D(p4, p5)  # left outer web
        l4 = Arc2D(p5, p6, p7)  # left top outer fillet
        l5 = Line2D(p7, p8)  # outer top
        l6 = Line2D(p8, p9)
        l7 = Line2D(p9, p10)
        l8 = Arc2D(p10, p11, p12)  # left top inner fillet
        l9 = Line2D(p12, p13)
        l10 = Arc2D(p13, p14, p15)  # left botom inner fillet
        l11 = Line2D(p15, p16)
        l12 = Line2D(p16, p1)

        self.curve = PolyCurve2D().by_joined_curves(
            [l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12])

    def serialize(self):
        return {
            'Description': self.Description,
            'ID': self.ID,
            'id': self.id,
            'type': self.type,
            'name': self.name,
            'height': self.height,
            'width': self.width,
            't': self.t,
            'r1': self.r1,
            'r2': self.r2,
            'ex': self.ex,
            'ey': self.ey,
            'curve': self.curve.serialize() if self.curve else None
        }

    @staticmethod
    def deserialize(data):
        c_profile = CProfile(
            name=data.get('name'),
            width=data.get('width'),
            height=data.get('height'),
            t=data.get('t'),
            r1=data.get('r1'),
            ex=data.get('ex')
        )

        c_profile.Description = data.get(
            'Description', "Cold Formed C Profile")
        c_profile.ID = data.get('ID', "CP")
        c_profile.id = data.get('id')
        c_profile.type = data.get('type')
        c_profile.r2 = data.get('r2')
        c_profile.ey = data.get('ey')
        c_profile.curve = PolyCurve2D.deserialize(
            data['curve']) if 'curve' in data else None

        return c_profile

    def __str__(self):
        return f"{self.type} ({self.name})"


class CProfileWithLips(RectangularSteelShape):
    def __init__(self, name, width, height, h1, t, r1, ex):
        super().__init__(name, "Cold Formed C Profile", "Unknown", "CP", height,width)
        
        self.Description = "Cold Formed C Profile with Lips"
        self.ID = "CPWL"

        # parameters
        self.id = generateID()
        self.type = __class__.__name__
        self.name = name
        
        self.height = height  # height
        self.width = width  # width
        self.h1 = h1  # lip length
        self.t = t  # flange thickness
        self.r1 = r1  # outer radius
        self.r2 = r1-t  # inner radius
        r2 = r1-t

        self.ex = ex
        self.ey = height/2
        dr = r1 - r1/sqrt2
        dri = r2 - r2/sqrt2
        hi = height-t
        self.IFC_profile_def = "Unknown"

        # describe points
        p1 = Point2D(width-ex-r1, -height/2)  # right bottom  before fillet
        p2 = Point2D(r1-ex, -height/2)
        p3 = Point2D(dr-ex, -height/2+dr)
        p4 = Point2D(0-ex, -height/2+r1)
        p5 = Point2D(p4.x, -p4.y)
        p6 = Point2D(p3.x, -p3.y)
        p7 = Point2D(p2.x, -p2.y)
        p8 = Point2D(p1.x, -p1.y)  # right top before fillet
        p9 = Point2D(width-ex-dr, height/2-dr)  # middle point arc
        p10 = Point2D(width-ex, height/2-r1)  # end fillet
        p11 = Point2D(width-ex, height/2-h1)
        p12 = Point2D(width-ex-t, height/2-h1)  # bottom lip
        p13 = Point2D(width-ex-t, height/2-t-r2)  # start inner fillet right top
        p14 = Point2D(width-ex-t-dri, height/2-t-dri)
        p15 = Point2D(width-ex-t-r2, height/2-t)  # end inner fillet right top
        p16 = Point2D(0-ex+t+r2, height/2-t)
        p17 = Point2D(0-ex+t+dri, height/2-t-dri)
        p18 = Point2D(0-ex+t, height/2-t-r2)

        p19 = Point2D(p18.x, -p18.y)
        p20 = Point2D(p17.x, -p17.y)
        p21 = Point2D(p16.x, -p16.y)
        p22 = Point2D(p15.x, -p15.y)
        p23 = Point2D(p14.x, -p14.y)
        p24 = Point2D(p13.x, -p13.y)
        p25 = Point2D(p12.x, -p12.y)
        p26 = Point2D(p11.x, -p11.y)
        p27 = Point2D(p10.x, -p10.y)
        p28 = Point2D(p9.x, -p9.y)

        # describe outer curves
        l1 = Line2D(p1, p2)
        l2 = Arc2D(p2, p3, p4)
        l3 = Line2D(p4, p5)
        l4 = Arc2D(p5, p6, p7)  # outer fillet right top
        l5 = Line2D(p7, p8)
        l6 = Arc2D(p8, p9, p10)
        l7 = Line2D(p10, p11)
        l8 = Line2D(p11, p12)
        l9 = Line2D(p12, p13)
        l10 = Arc2D(p13, p14, p15)
        l11 = Line2D(p15, p16)
        l12 = Arc2D(p16, p17, p18)
        l13 = Line2D(p18, p19)  # inner web
        l14 = Arc2D(p19, p20, p21)
        l15 = Line2D(p21, p22)
        l16 = Arc2D(p22, p23, p24)
        l17 = Line2D(p24, p25)
        l18 = Line2D(p25, p26)
        l19 = Line2D(p26, p27)
        l20 = Arc2D(p27, p28, p1)

        self.curve = PolyCurve2D().by_joined_curves(
            [l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12, l13, l14, l15, l16, l17, l18, l19, l20])

    def serialize(self):
        return {
            'Description': self.Description,
            'ID': self.ID,
            'id': self.id,
            'type': self.type,
            'name': self.name,
            'height': self.height,
            'width': self.width,
            'h1': self.h1,
            't': self.t,
            'r1': self.r1,
            'r2': self.r2,
            'ex': self.ex,
            'ey': self.ey,
            'curve': self.curve.serialize() if self.curve else None
        }

    @staticmethod
    def deserialize(data):
        c_profile_with_lips = CProfileWithLips(
            name=data.get('name'),
            width=data.get('width'),
            height=data.get('height'),
            h1=data.get('h1'),
            t=data.get('t'),
            r1=data.get('r1'),
            ex=data.get('ex')
        )

        c_profile_with_lips.Description = data.get(
            'Description', "Cold Formed C Profile with Lips")
        c_profile_with_lips.ID = data.get('ID', "CPWL")
        c_profile_with_lips.id = data.get('id')
        c_profile_with_lips.type = data.get('type')
        c_profile_with_lips.r2 = data.get('r2')
        c_profile_with_lips.ey = data.get('ey')
        c_profile_with_lips.curve = PolyCurve2D.deserialize(
            data['curve']) if 'curve' in data else None

        return c_profile_with_lips

    def __str__(self):
        return "Profile(" + f"{self.name})"


class LProfileColdFormed(RectangularSteelShape):
    def __init__(self, name, width, height, t, r1, ex, ey):
        super().__init__(name, "Cold Formed L Profile", "Unknown", "CF_L", height,width)

        # parameters
        self.type = __class__.__name__
        
        self.t = t  # flange thickness
        self.r1 = r1  # inner radius
        self.r2 = r1-t  # outer radius
        self.ex = ex
        self.ey = ey
        r11 = r1/math.sqrt(2)
        r2 = r1+t
        r21 = r2/math.sqrt(2)

        # describe points
        p1 = Point2D(-ex, -ey + r2)  # start arc left bottom
        p2 = Point2D(-ex + r2 - r21, -ey + r2 - r21)  # second point arc
        p3 = Point2D(-ex + r2, -ey)  # end arc
        p4 = Point2D(width - ex, -ey)  # right bottom
        p5 = Point2D(width - ex, -ey + t)
        p6 = Point2D(-ex + t + r1, -ey + t)  # start arc
        p7 = Point2D(-ex + t + r1 - r11, -ey + t +
                     r1 - r11)  # second point arc
        p8 = Point2D(-ex + t, -ey + t + r1)  # end arc
        p9 = Point2D(-ex + t, ey)
        p10 = Point2D(-ex, ey)  # left top

        l1 = Arc2D(p1, p2, p3)
        l2 = Line2D(p3, p4)
        l3 = Line2D(p4, p5)
        l4 = Line2D(p5, p6)
        l5 = Arc2D(p6, p7, p8)
        l6 = Line2D(p8, p9)
        l7 = Line2D(p9, p10)
        l8 = Line2D(p10, p1)

        self.curve = PolyCurve2D().by_joined_curves(
            [l1, l2, l3, l4, l5, l6, l7, l8])

    def serialize(self):
        return {
            'Description': self.Description,
            'ID': self.ID,
            'id': self.id,
            'type': self.type,
            'name': self.name,
            'height': self.height,
            'width': self.width,
            't': self.t,
            'r1': self.r1,
            'r2': self.r2,
            'ex': self.ex,
            'ey': self.ey,
            'curve': self.curve.serialize() if self.curve else None
        }

    @staticmethod
    def deserialize(data):
        l_profile_cold_formed = LProfileColdFormed(
            name=data.get('name'),
            width=data.get('width'),
            height=data.get('height'),
            t=data.get('t'),
            r1=data.get('r1'),
            ex=data.get('ex'),
            ey=data.get('ey')
        )

        l_profile_cold_formed.Description = data.get(
            'Description', "Cold Formed L Profile")
        l_profile_cold_formed.ID = data.get('ID', "CF_L")
        l_profile_cold_formed.id = data.get('id')
        l_profile_cold_formed.type = data.get('type')
        l_profile_cold_formed.r2 = data.get('r2')
        l_profile_cold_formed.curve = PolyCurve2D.deserialize(
            data['curve']) if 'curve' in data else None

        return l_profile_cold_formed

    def __str__(self):
        return f"{self.type} ({self.name})"


class SigmaProfileWithLipsColdFormed(RectangularSteelShape):
    def __init__(self, name, width, height, t, r1, h1, h2, h3, b2, ex):
        super().__init__(name, "Cold Formed Sigma Profile with Lips", "Unknown", "CF_SWL", height,width)

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
        self.r2 = r2 = r1+t  # outer radius
        self.ex = ex
        self.ey = ey = height/2
        self.r11 = r11 = r1/math.sqrt(2)
        self.r21 = r21 = r2/math.sqrt(2)

        p1 = Point2D(-ex + b2, -h2 / 2)
        p2 = Point2D(-ex, -ey + h3)
        p3 = Point2D(-ex, -ey + r2)  # start arc left bottom
        p4 = Point2D(-ex + r2 - r21, -ey + r2 - r21)  # second point arc
        p5 = Point2D(-ex + r2, -ey)  # end arc
        p6 = Point2D(width - ex - r2, -ey)  # start arc
        p7 = Point2D(width - ex - r2 + r21, -ey + r2 - r21)  # second point arc
        p8 = Point2D(width - ex, -ey + r2)  # end arc
        p9 = Point2D(width - ex, -ey + h1)  # end lip
        p10 = Point2D(width - ex - t, -ey + h1)
        p11 = Point2D(width - ex - t, -ey + t + r1)  # start arc
        p12 = Point2D(width - ex - t - r1 + r11, -ey +
                      t + r1 - r11)  # second point arc
        p13 = Point2D(width - ex - t - r1, -ey + t)  # end arc
        p14 = Point2D(-ex + t + r1, -ey + t)  # start arc
        p15 = Point2D(-ex + t + r1 - r11, -ey + t +
                      r1 - r11)  # second point arc
        p16 = Point2D(-ex + t, -ey + t + r1)  # end arc
        p17 = Point2D(-ex + t, -ey + h3 - h5)
        p18 = Point2D(-ex + b2 + t, -h2 / 2 - h5)
        p19 = Point2D(p18.x, -p18.y)
        p20 = Point2D(p17.x, -p17.y)
        p21 = Point2D(p16.x, -p16.y)
        p22 = Point2D(p15.x, -p15.y)
        p23 = Point2D(p14.x, -p14.y)
        p24 = Point2D(p13.x, -p13.y)
        p25 = Point2D(p12.x, -p12.y)
        p26 = Point2D(p11.x, -p11.y)
        p27 = Point2D(p10.x, -p10.y)
        p28 = Point2D(p9.x, -p9.y)
        p29 = Point2D(p8.x, -p8.y)
        p30 = Point2D(p7.x, -p7.y)
        p31 = Point2D(p6.x, -p6.y)
        p32 = Point2D(p5.x, -p5.y)
        p33 = Point2D(p4.x, -p4.y)
        p34 = Point2D(p3.x, -p3.y)
        p35 = Point2D(p2.x, -p2.y)
        p36 = Point2D(p1.x, -p1.y)

        l1 = Line2D(p1, p2)
        l2 = Line2D(p2, p3)
        l3 = Arc2D(p3, p4, p5)
        l4 = Line2D(p5, p6)
        l5 = Arc2D(p6, p7, p8)
        l6 = Line2D(p8, p9)
        l7 = Line2D(p9, p10)
        l8 = Line2D(p10, p11)
        l9 = Arc2D(p11, p12, p13)
        l10 = Line2D(p13, p14)
        l11 = Arc2D(p14, p15, p16)
        l12 = Line2D(p16, p17)
        l13 = Line2D(p17, p18)
        l14 = Line2D(p18, p19)
        l15 = Line2D(p19, p20)
        l16 = Line2D(p20, p21)
        l17 = Arc2D(p21, p22, p23)
        l18 = Line2D(p23, p24)
        l19 = Arc2D(p24, p25, p26)
        l20 = Line2D(p26, p27)
        l21 = Line2D(p27, p28)
        l22 = Line2D(p28, p29)
        l23 = Arc2D(p29, p30, p31)
        l24 = Line2D(p31, p32)
        l25 = Arc2D(p32, p33, p34)
        l26 = Line2D(p34, p35)
        l27 = Line2D(p35, p36)
        l28 = Line2D(p36, p1)

        self.curve = PolyCurve2D().by_joined_curves([l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12, l13, l14, l15, l16, l17, l18, l19, l20, l21, l22, l23,
                                                     l24, l25,
                                                     l26, l27, l28])

    def serialize(self):
        return {
            'Description': self.Description,
            'ID': self.ID,
            'id': self.id,
            'type': self.type,
            'name': self.name,
            'height': self.height,
            'width': self.width,
            't': self.t,
            'r1': self.r1,
            'h1': self.h1,
            'h2': self.h2,
            'h3': self.h3,
            'b2': self.b2,
            'ex': self.ex,
            'ey': self.ey,
            'r2': self.r2,
            'r11': self.r11,
            'r21': self.r21,
            'h4': self.h4,
            'h5': self.h5,
            'curve': self.curve.serialize() if self.curve else None
        }

    @staticmethod
    def deserialize(data):
        sigma_profile_with_lips = SigmaProfileWithLipsColdFormed(
            name=data.get('name'),
            width=data.get('width'),
            height=data.get('height'),
            t=data.get('t'),
            r1=data.get('r1'),
            h1=data.get('h1'),
            h2=data.get('h2'),
            h3=data.get('h3'),
            b2=data.get('b2'),
            ex=data.get('ex')
        )

        sigma_profile_with_lips.Description = data.get(
            'Description', "Cold Formed Sigma Profile with Lips")
        sigma_profile_with_lips.ID = data.get('ID', "CF_SWL")
        sigma_profile_with_lips.id = data.get('id')
        sigma_profile_with_lips.type = data.get('type')
        sigma_profile_with_lips.ey = data.get('ey')
        sigma_profile_with_lips.r2 = data.get('r2')
        sigma_profile_with_lips.r11 = data.get('r11')
        sigma_profile_with_lips.r21 = data.get('r21')
        sigma_profile_with_lips.h4 = data.get('h4')
        sigma_profile_with_lips.h5 = data.get('h5')
        sigma_profile_with_lips.curve = PolyCurve2D.deserialize(
            data['curve']) if 'curve' in data else None

        return sigma_profile_with_lips

    def __str__(self):
        return f"{self.type} ({self.name})"


class ZProfileColdFormed(RectangularSteelShape):
    def __init__(self, name, width, height, t, r1):
        super().__init__(name, "Cold Formed Z Profile", "Unknown", "CF_Z", height,width)

        # parameters
        self.type = __class__.__name__

        self.t = t  # flange thickness
        self.r1 = r1  # inner radius
        self.r2 = r2 = r1+t  # outer radius
        self.ex = ex = width/2
        self.ey = ey = height/2
        self.r11 = r11 = r1 / math.sqrt(2)
        self.r21 = r21 = r2 / math.sqrt(2)

        p1 = Point2D(-0.5 * t, -ey + t + r1)  # start arc
        p2 = Point2D(-0.5 * t - r1 + r11, -ey + t +
                     r1 - r11)  # second point arc
        p3 = Point2D(-0.5 * t - r1, -ey + t)  # end arc
        p4 = Point2D(-ex, -ey + t)
        p5 = Point2D(-ex, -ey)  # left bottom
        p6 = Point2D(-r2 + 0.5 * t, -ey)  # start arc
        p7 = Point2D(-r2 + 0.5 * t + r21, -ey + r2 - r21)  # second point arc
        p8 = Point2D(0.5 * t, -ey + r2)  # end arc
        p9 = Point2D(-p1.x, -p1.y)
        p10 = Point2D(-p2.x, -p2.y)
        p11 = Point2D(-p3.x, -p3.y)
        p12 = Point2D(-p4.x, -p4.y)
        p13 = Point2D(-p5.x, -p5.y)
        p14 = Point2D(-p6.x, -p6.y)
        p15 = Point2D(-p7.x, -p7.y)
        p16 = Point2D(-p8.x, -p8.y)

        l1 = Arc2D(p1, p2, p3)
        l2 = Line2D(p3, p4)
        l3 = Line2D(p4, p5)
        l4 = Line2D(p5, p6)
        l5 = Arc2D(p6, p7, p8)
        l6 = Line2D(p8, p9)
        l7 = Arc2D(p9, p10, p11)
        l8 = Line2D(p11, p12)
        l9 = Line2D(p12, p13)
        l10 = Line2D(p13, p14)
        l11 = Arc2D(p14, p15, p16)
        l12 = Line2D(p16, p1)

        self.curve = PolyCurve2D().by_joined_curves(
            [l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12])

    def serialize(self):
        return {
            'Description': self.Description,
            'ID': self.ID,
            'id': self.id,
            'type': self.type,
            'name': self.name,
            'width': self.width,
            'height': self.height,
            't': self.t,
            'r1': self.r1,
            'r2': self.r2,
            'ex': self.ex,
            'ey': self.ey,
            'r11': self.r11,
            'r21': self.r21,
            'curve': self.curve.serialize() if self.curve else None
        }

    @staticmethod
    def deserialize(data):
        z_profile_cold_formed = ZProfileColdFormed(
            name=data.get('name'),
            width=data.get('width'),
            height=data.get('height'),
            t=data.get('t'),
            r1=data.get('r1')
        )

        z_profile_cold_formed.Description = data.get(
            'Description', "Cold Formed Z Profile")
        z_profile_cold_formed.ID = data.get('ID', "CF_Z")
        z_profile_cold_formed.id = data.get('id')
        z_profile_cold_formed.type = data.get('type')
        z_profile_cold_formed.r2 = data.get('r2')
        z_profile_cold_formed.ex = data.get('ex')
        z_profile_cold_formed.ey = data.get('ey')
        z_profile_cold_formed.r11 = data.get('r11')
        z_profile_cold_formed.r21 = data.get('r21')
        z_profile_cold_formed.curve = PolyCurve2D.deserialize(
            data['curve']) if 'curve' in data else None

        return z_profile_cold_formed

    def __str__(self):
        return f"{self.type} ({self.name})"


class ZProfileWithLipsColdFormed(RectangularSteelShape):
    def __init__(self, name, width, height, t, r1, h1):
        super().__init__(name,"Cold Formed Z Profile with Lips", "Unknown", "CF_ZL", height,width)

        # parameters
        self.type = __class__.__name__
        
        self.t = t  # flange thickness
        self.h1 = h1  # lip length
        self.r1 = r1  # inner radius
        self.r2 = r2 = r1+t  # outer radius
        self.ex = ex = width/2
        self.ey = ey = height/2
        self.r11 = r11 = r1 / math.sqrt(2)
        self.r21 = r21 = r2 / math.sqrt(2)

        p1 = Point2D(-0.5*t, -ey+t+r1)  # start arc
        p2 = Point2D(-0.5*t-r1+r11, -ey+t+r1-r11)  # second point arc
        p3 = Point2D(-0.5*t-r1, -ey+t)  # end arc
        p4 = Point2D(-ex+t+r1, -ey+t)  # start arc
        p5 = Point2D(-ex+t+r1-r11, -ey+t+r1-r11)  # second point arc
        p6 = Point2D(-ex+t, -ey+t+r1)  # end arc
        p7 = Point2D(-ex+t, -ey+h1)
        p8 = Point2D(-ex, -ey+h1)
        p9 = Point2D(-ex, -ey+r2)  # start arc
        p10 = Point2D(-ex+r2-r21, -ey+r2-r21)  # second point arc
        p11 = Point2D(-ex+r2, -ey)  # end arc
        p12 = Point2D(-r2+0.5*t, -ey)  # start arc
        p13 = Point2D(-r2+0.5*t+r21, -ey+r2-r21)  # second point arc
        p14 = Point2D(0.5*t, -ey+r2)  # end arc
        p15 = Point2D(-p1.x, -p1.y)
        p16 = Point2D(-p2.x, -p2.y)
        p17 = Point2D(-p3.x, -p3.y)
        p18 = Point2D(-p4.x, -p4.y)
        p19 = Point2D(-p5.x, -p5.y)
        p20 = Point2D(-p6.x, -p6.y)
        p21 = Point2D(-p7.x, -p7.y)
        p22 = Point2D(-p8.x, -p8.y)
        p23 = Point2D(-p9.x, -p9.y)
        p24 = Point2D(-p10.x, -p10.y)
        p25 = Point2D(-p11.x, -p11.y)
        p26 = Point2D(-p12.x, -p12.y)
        p27 = Point2D(-p13.x, -p13.y)
        p28 = Point2D(-p14.x, -p14.y)

        l1 = Arc2D(p1, p2, p3)
        l2 = Line2D(p3, p4)
        l3 = Arc2D(p4, p5, p6)
        l4 = Line2D(p6, p7)
        l5 = Line2D(p7, p8)
        l6 = Line2D(p8, p9)
        l7 = Arc2D(p9, p10, p11)
        l8 = Line2D(p11, p12)
        l9 = Arc2D(p12, p13, p14)
        l10 = Line2D(p14, p15)
        l11 = Arc2D(p15, p16, p17)
        l12 = Line2D(p17, p18)
        l13 = Arc2D(p18, p19, p20)
        l14 = Line2D(p20, p21)
        l15 = Line2D(p21, p22)
        l16 = Line2D(p22, p23)
        l17 = Arc2D(p23, p24, p25)
        l18 = Line2D(p25, p26)
        l19 = Arc2D(p26, p27, p28)
        l20 = Line2D(p28, p1)

        self.curve = PolyCurve2D().by_joined_curves(
            [l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12, l13, l14, l15, l16, l17, l18, l19, l20])

    def serialize(self):
        return {
            'Description': self.Description,
            'ID': self.ID,
            'id': self.id,
            'type': self.type,
            'name': self.name,
            'width': self.width,
            'height': self.height,
            't': self.t,
            'h1': self.h1,
            'r1': self.r1,
            'r2': self.r2,
            'ex': self.ex,
            'ey': self.ey,
            'r11': self.r11,
            'r21': self.r21,
            'curve': self.curve.serialize() if self.curve else None
        }

    @staticmethod
    def deserialize(data):
        z_profile_with_lips = ZProfileWithLipsColdFormed(
            name=data.get('name'),
            width=data.get('width'),
            height=data.get('height'),
            t=data.get('t'),
            r1=data.get('r1'),
            h1=data.get('h1')
        )

        z_profile_with_lips.Description = data.get(
            'Description', "Cold Formed Z Profile with Lips")
        z_profile_with_lips.ID = data.get('ID', "CF_ZL")
        z_profile_with_lips.id = data.get('id')
        z_profile_with_lips.type = data.get('type')
        z_profile_with_lips.r2 = data.get('r2')
        z_profile_with_lips.ex = data.get('ex')
        z_profile_with_lips.ey = data.get('ey')
        z_profile_with_lips.r11 = data.get('r11')
        z_profile_with_lips.r21 = data.get('r21')
        z_profile_with_lips.curve = PolyCurve2D.deserialize(
            data['curve']) if 'curve' in data else None

        return z_profile_with_lips

    def __str__(self):
        return f"{self.type} ({self.name})"
