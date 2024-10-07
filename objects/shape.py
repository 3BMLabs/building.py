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

class Tshape:
    def __init__(self, name, h, b, h1, b1):
        self.Description = "T-shape"
        self.ID = "T"

        # parameters
        self.id = generateID()
        self.type = __class__.__name__
        self.name = name
        self.curve = []
        self.h = h  # height
        self.b = b  # width
        self.h1 = h1
        self.b1 = b1

        # describe points
        p1 = Point2D(b1 / 2, -h / 2)  # right bottom
        p2 = Point2D(b1 / 2, h / 2 - h1)  # right middle 1
        p3 = Point2D(b / 2, h / 2 - h1)  # right middle 2
        p4 = Point2D(b / 2, h / 2)  # right top
        p5 = Point2D(-b / 2, h / 2)  # left top
        p6 = Point2D(-b / 2, h / 2 - h1)  # left middle 2
        p7 = Point2D(-b1 / 2, h / 2 - h1)  # left middle 1
        p8 = Point2D(-b1 / 2, -h / 2)  # left bottom

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
            'h': self.h,
            'b': self.b,
            'h1': self.h1,
            'b1': self.b1,
            'curve': self.curve.serialize() if self.curve else None
        }

    @staticmethod
    def deserialize(data):
        tshape = Tshape(
            name=data.get('name'),
            h=data.get('h'),
            b=data.get('b'),
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


class Lshape:
    def __init__(self, name, h, b, h1, b1):
        self.Description = "L-shape"
        self.ID = "L"

        # parameters
        self.id = generateID()
        self.type = __class__.__name__
        self.name = name
        self.curve = []
        self.h = h  # height
        self.b = b  # width
        self.h1 = h1
        self.b1 = b1

        # describe points
        p1 = Point2D(b / 2, -h / 2)  # right bottom
        p2 = Point2D(b / 2, -h / 2 + h1)  # right middle
        p3 = Point2D(-b / 2 + b1, -h / 2 + h1)  # middle
        p4 = Point2D(-b / 2 + b1, h / 2)  # middle top
        p5 = Point2D(-b / 2, h / 2)  # left top
        p6 = Point2D(-b / 2, -h / 2)  # left bottom

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
            'h': self.h,
            'b': self.b,
            'h1': self.h1,
            'b1': self.b1,
            'curve': self.curve.serialize() if self.curve else None
        }

    @staticmethod
    def deserialize(data):
        lshape = Lshape(
            name=data.get('name'),
            h=data.get('h'),
            b=data.get('b'),
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


class Eshape:
    def __init__(self, name, h, b, h1):
        self.Description = "E-shape"
        self.ID = "E"

        # parameters
        self.id = generateID()
        self.type = __class__.__name__
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

        self.curve = PolyCurve2D().by_joined_curves(
            [l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12])

    def serialize(self):
        return {
            'Description': self.Description,
            'ID': self.ID,
            'id': self.id,
            'type': self.type,
            'name': self.name,
            'h': self.h,
            'b': self.b,
            'h1': self.h1,
            'curve': self.curve.serialize() if self.curve else None
        }

    @staticmethod
    def deserialize(data):
        eshape = Eshape(
            name=data.get('name'),
            h=data.get('h'),
            b=data.get('b'),
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


class Nshape:
    def __init__(self, name, h, b, b1):
        self.Description = "N-shape"
        self.ID = "N"

        # parameters
        self.id = generateID()
        self.type = __class__.__name__
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

        self.curve = PolyCurve2D().by_joined_curves(
            [l1, l2, l3, l4, l5, l6, l7, l8, l9, l10])

    def serialize(self):
        return {
            'Description': self.Description,
            'ID': self.ID,
            'id': self.id,
            'type': self.type,
            'name': self.name,
            'h': self.h,
            'b': self.b,
            'b1': self.b1,
            'curve': self.curve.serialize() if self.curve else None
        }

    @staticmethod
    def deserialize(data):
        nshape = Nshape(
            name=data.get('name'),
            h=data.get('h'),
            b=data.get('b'),
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


class Arrowshape:
    def __init__(self, name, l, b, b1, l1):
        self.Description = "Arrow-shape"
        self.ID = "Arrowshape"

        # parameters
        self.id = generateID()
        self.type = __class__.__name__
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

        self.curve = PolyCurve2D().by_joined_curves(
            [l1, l2, l3, l4, l5, l6, l7])

    def serialize(self):
        return {
            'Description': self.Description,
            'ID': self.ID,
            'id': self.id,
            'type': self.type,
            'name': self.name,
            'l': self.l,
            'b': self.b,
            'b1': self.b1,
            'l1': self.l1,
            'curve': self.curve.serialize() if self.curve else None
        }

    @staticmethod
    def deserialize(data):
        arrowshape = Arrowshape(
            name=data.get('name'),
            l=data.get('l'),
            b=data.get('b'),
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
