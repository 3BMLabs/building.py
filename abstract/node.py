# [included in BP singlefile]
# [!not included in BP singlefile - start]
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


"""This module provides tools for planes
"""

__title__= "plane"
__author__ = "Maarten & Jonathan"
__url__ = "./abstract/plane.py"

import sys, os, math
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from abstract.vector import *
from geometry.point import Point
from project.fileformat import *

# [!not included in BP singlefile - end]

class Node:
    def __init__(self, point:None=Point, vector:None=Vector3, number:None=int, diameter:None=str, comments=None):
        self.id = generateID()
        self.type = self.__class__.__name__
        self.point: Point = point
        self.vector: Vector3 = vector
        self.number: int = number
        self.diameter: float = project.node_diameter
        self.comments = comments
    
    def serialize(self):
        return {
            'id': self.id,
            'type': self.type,
            'point': self.point.serialize() if self.point else None,
            'vector': self.vector.serialize() if self.vector else None,
            'number': self.number,
            'diameter': self.diameter,
            'comments': self.comments
        }
    
    @staticmethod
    def deserialize(data):
        node = Node()
        node.id = data.get('id')
        node.type = data.get('type')
        node.point = Point.deserialize(data['point']) if data.get('point') else None
        node.vector = Vector3.deserialize(data['vector']) if data.get('vector') else None
        node.number = data.get('number')
        node.diameter = data.get('diameter')
        node.comments = data.get('comments')

        return node

    #merge
    def merge(self):
        if project.node_merge == True:
            pass
        else:
            pass

    #snap
    def snap(self):
        pass

    def __str__(self) -> str:
        return f"{self.type}"