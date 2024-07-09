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
__author__ = "Joas"
__url__ = "./objects/shape.py"

import sys, math
from pathlib import Path
from objects.frame import *

sys.path.append(str(Path(__file__).resolve().parents[1]))

from geometry.geometry2d import *

# [!not included in BP singlefile - end]

sqrt2 = math.sqrt(2)

class Shape(Serializable):
    def __init__(self, ID, name:string, description:string):
        super().__init__()
        self.ID = ID
        self.name = name
        self.description = description
        self.curve = []

#define rectangularshape as a separate class for now, to make multiple inheritance easier
class RectangularShape(Shape):
    def __init__(self, height, width, **kwargs):
        super().__init__(**kwargs)
        self.height = height
        self.width = width

class Tshape(RectangularShape):
    def __init__(self, name, height, width, h1, b1):
        super().__init__("T", name, "T-shape")

        # parameters
        self.type = __class__.__name__
        self.height = height  # height
        self.width = width  # width
        self.h1 = h1
        self.b1 = b1

        # describe points
        p1 = Point2D(b1 / 2, -height / 2)  # right bottom
        p2 = Point2D(b1 / 2, height / 2 - h1)  # right middle 1
        p3 = Point2D(width / 2, height / 2 - h1)  # right middle 2
        p4 = Point2D(width / 2, height / 2)  # right top
        p5 = Point2D(-width / 2, height / 2)  # left top
        p6 = Point2D(-width / 2, height / 2 - h1)  # left middle 2
        p7 = Point2D(-b1 / 2, height / 2 - h1)  # left middle 1
        p8 = Point2D(-b1 / 2, -height / 2)  # left bottom

        # describe curves
        l1 = Line2D(p1, p2)
        l2 = Line2D(p2, p3)
        l3 = Line2D(p3, p4)
        l4 = Line2D(p4, p5)
        l5 = Line2D(p5, p6)
        l6 = Line2D(p6, p7)
        l7 = Line2D(p7, p8)
        l8 = Line2D(p8, p1)

        self.curve = PolyCurve2D().by_joined_curves(
            [l1, l2, l3, l4, l5, l6, l7, l8])

    def serialize(self):
        id_value = str(self.id) if not isinstance(
            self.id, (str, int, float)) else self.id
        return {
            'id': id_value,
            'type': self.type,
            'Description': self.Description,
            'ID': self.ID,
            'name': self.name,
            'height': self.height,
            'width': self.width,
            'h1': self.h1,
            'b1': self.b1,
            'curve': self.curve.serialize() if self.curve else None
        }

    @staticmethod
    def deserialize(data):
        tshape = Tshape(
            name=data.get('name'),
            height=data.get('height'),
            width=data.get('width'),
            h1=data.get('h1'),
            b1=data.get('b1')
        )

        tshape.Description = data.get('Description', "T-shape")
        tshape.ID = data.get('ID', "T")
        tshape.curve = PolyCurve2D.deserialize(
            data['curve']) if 'curve' in data else None

        return tshape

    def __str__(self):
        return "Profile(" + f"{self.name})"


class Lshape(RectangularShape):
    def __init__(self, name, height, width, h1, b1):
        super().__init__(ID = "L", name=name, Description="L-shape", height=height,width=width)

        # parameters
        self.type = __class__.__name__
        self.h1 = h1
        self.b1 = b1

        # describe points
        p1 = Point2D(width / 2, -height / 2)  # right bottom
        p2 = Point2D(width / 2, -height / 2 + h1)  # right middle
        p3 = Point2D(-width / 2 + b1, -height / 2 + h1)  # middle
        p4 = Point2D(-width / 2 + b1, height / 2)  # middle top
        p5 = Point2D(-width / 2, height / 2)  # left top
        p6 = Point2D(-width / 2, -height / 2)  # left bottom

        # describe curves
        l1 = Line2D(p1, p2)
        l2 = Line2D(p2, p3)
        l3 = Line2D(p3, p4)
        l4 = Line2D(p4, p5)
        l5 = Line2D(p5, p6)
        l6 = Line2D(p6, p1)

        self.curve = PolyCurve2D().by_joined_curves([l1, l2, l3, l4, l5, l6])

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
            'b1': self.b1,
            'curve': self.curve.serialize() if self.curve else None
        }

    @staticmethod
    def deserialize(data):
        lshape = Lshape(
            name=data.get('name'),
            height=data.get('height'),
            width=data.get('width'),
            h1=data.get('h1'),
            b1=data.get('b1')
        )

        lshape.Description = data.get('Description', "L-shape")
        lshape.ID = data.get('ID', "L")
        lshape.id = data.get('id')
        lshape.type = data.get('type')
        lshape.curve = PolyCurve2D.deserialize(
            data['curve']) if 'curve' in data else None

        return lshape

    def __str__(self):
        return "Profile(" + f"{self.name})"


class Eshape(Serializable):
    def __init__(self, name, height, width, h1):
        super().__init__(ID = "E", name=name, Description="E-shape", height=height,width=width)

        # parameters
        self.type = __class__.__name__
        self.h1 = h1

        # describe points
        p1 = Point2D(width / 2, -height / 2)  # right bottom
        p2 = Point2D(width / 2, -height / 2 + h1)
        p3 = Point2D(-width / 2 + h1, -height / 2 + h1)
        p4 = Point2D(-width / 2 + h1, -h1 / 2)
        p5 = Point2D(width / 2, -h1 / 2)
        p6 = Point2D(width / 2, h1 / 2)
        p7 = Point2D(-width / 2 + h1, h1 / 2)
        p8 = Point2D(-width / 2 + h1, height / 2 - h1)
        p9 = Point2D(width / 2, height / 2 - h1)
        p10 = Point2D(width / 2, height / 2)
        p11 = Point2D(-width / 2, height / 2)
        p12 = Point2D(-width / 2, -height / 2)

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
            'h1': self.h1,
            'curve': self.curve.serialize() if self.curve else None
        }

    @staticmethod
    def deserialize(data):
        eshape = Eshape(
            name=data.get('name'),
            height=data.get('height'),
            width=data.get('width'),
            h1=data.get('h1')
        )

        eshape.Description = data.get('Description', "E-shape")
        eshape.ID = data.get('ID', "E")
        eshape.id = data.get('id')
        eshape.type = data.get('type')
        eshape.curve = PolyCurve2D.deserialize(
            data['curve']) if 'curve' in data else None

        return eshape

    def __str__(self):
        return "Profile(" + f"{self.name})"


class Nshape(Serializable):
    def __init__(self, name, height, width, b1):
        super().__init__(ID = "N", name=name, Description="N-shape", height=height,width=width)

        # parameters
        self.type = __class__.__name__
        self.b1 = b1

        # describe points
        p1 = Point2D(width / 2, -height / 2)  # right bottom
        p2 = Point2D(width / 2, height / 2)
        p3 = Point2D(width / 2 - b1, height / 2)
        p4 = Point2D(width / 2 - b1, -height / 2 + b1 * 2)
        p5 = Point2D(-width / 2 + b1, height / 2)
        p6 = Point2D(-width / 2, height / 2)
        p7 = Point2D(-width / 2, -height / 2)
        p8 = Point2D(-width / 2 + b1, -height / 2)
        p9 = Point2D(-width / 2 + b1, height / 2 - b1 * 2)
        p10 = Point2D(width / 2 - b1, -height / 2)

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

        self.curve = PolyCurve2D().by_joined_curves(
            [l1, l2, l3, l4, l5, l6, l7, l8, l9, l10])

    def serialize(self):
        return {
            'Description': self.Description,
            'ID': self.ID,
            'id': self.id,
            'type': self.type,
            'name': self.name,
            'height': self.height,
            'width': self.width,
            'b1': self.b1,
            'curve': self.curve.serialize() if self.curve else None
        }

    @staticmethod
    def deserialize(data):
        nshape = Nshape(
            name=data.get('name'),
            height=data.get('height'),
            width=data.get('width'),
            b1=data.get('b1')
        )

        nshape.Description = data.get('Description', "N-shape")
        nshape.ID = data.get('ID', "N")
        nshape.id = data.get('id')
        nshape.type = data.get('type')
        nshape.curve = PolyCurve2D.deserialize(
            data['curve']) if 'curve' in data else None

        return nshape

    def __str__(self):
        return "Profile(" + f"{self.name})"


class Arrowshape(Shape):
    def __init__(self, name, length, width, b1, l1):
        
        super().__init__(ID = "Arrowshape", name=name, Description="Arrow-shape")

        # parameters
        self.id = generateID()
        self.type = __class__.__name__
        self.length = length  # length
        self.width = width  # width
        self.b1 = b1
        self.l1 = l1

        # describe points
        p1 = Point2D(0, length / 2)  # top middle
        p2 = Point2D(width / 2, -length / 2 + l1)
        # p3 = Point2D(b1 / 2, -length / 2 + l1)
        p3 = Point2D(b1 / 2, (-length / 2 + l1) + (length / 2) / 4)
        p4 = Point2D(b1 / 2, -length / 2)
        p5 = Point2D(-b1 / 2, -length / 2)
        # p6 = Point2D(-b1 / 2, -length / 2 + l1)
        p6 = Point2D(-b1 / 2, (-length / 2 + l1) + (length / 2) / 4)
        p7 = Point2D(-width / 2, -length / 2 + l1)

        # describe curves
        l1 = Line2D(p1, p2)
        l2 = Line2D(p2, p3)
        l3 = Line2D(p3, p4)
        l4 = Line2D(p4, p5)
        l5 = Line2D(p5, p6)
        l6 = Line2D(p6, p7)
        l7 = Line2D(p7, p1)

        self.curve = PolyCurve2D().by_joined_curves(
            [l1, l2, l3, l4, l5, l6, l7])

    def serialize(self):
        return {
            'Description': self.Description,
            'ID': self.ID,
            'id': self.id,
            'type': self.type,
            'name': self.name,
            'length': self.length,
            'width': self.width,
            'b1': self.b1,
            'l1': self.l1,
            'curve': self.curve.serialize() if self.curve else None
        }

    @staticmethod
    def deserialize(data):
        arrowshape = Arrowshape(
            name=data.get('name'),
            length=data.get('length'),
            width=data.get('width'),
            b1=data.get('b1'),
            l1=data.get('l1')
        )

        arrowshape.Description = data.get('Description', "Arrow-shape")
        arrowshape.ID = data.get('ID', "Arrowshape")
        arrowshape.id = data.get('id')
        arrowshape.type = data.get('type')
        arrowshape.curve = PolyCurve2D.deserialize(
            data['curve']) if 'curve' in data else None

        return arrowshape

    def __str__(self):
        return "Profile(" + f"{self.name})"
