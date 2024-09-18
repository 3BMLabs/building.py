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


"""This module provides tools for planes
"""

__title__ = "plane"
__author__ = "Maarten & Jonathan"
__url__ = "./abstract/plane.py"

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from project.fileformat import *
from geometry.point import Point
from abstract.vector import *

# [!not included in BP singlefile - end]


class Node:
    """The `Node` class represents a geometric or structural node within a system, defined by a point in space, along with optional attributes like a direction vector, identifying number, and other characteristics."""
    def __init__(self, point=None, vector=None, number=None, distance=0.0, diameter=None, comments=None):
        """"Initializes a new Node instance.
        
        - `id` (str): A unique identifier for the node.
        - `type` (str): The class name, "Node".
        - `point` (Point, optional): The location of the node in 3D space.
        - `vector` (Vector, optional): A vector indicating the orientation or direction associated with the node.
        - `number` (any, optional): An identifying number or label for the node.
        - `distance` (float): A scalar attribute, potentially representing distance from a reference point or another node.
        - `diameter` (any, optional): A diameter associated with the node, useful in structural applications.
        - `comments` (str, optional): Additional comments or notes about the node.
        """
        self.id = generateID()
        self.point = point if isinstance(point, Point) else None
        self.vector = vector if isinstance(vector, Vector) else None
        self.number = number
        self.distance = distance
        self.diameter = diameter
        self.comments = comments

    def serialize(self) -> dict:
        """Serializes the node's attributes into a dictionary.

        This method allows for the node's properties to be easily stored or transmitted in a dictionary format.

        #### Returns:
        `dict`: A dictionary containing the serialized attributes of the node.
        """
        id_value = str(self.id) if not isinstance(
            self.id, (str, int, float)) else self.id
        return {
            'id': id_value,
            'type': self.type,
            'point': self.point.serialize() if self.point else None,
            'vector': self.vector.serialize() if self.vector else None,
            'number': self.number,
            'distance': self.distance,
            'diameter': self.diameter,
            'comments': self.comments
        }

    @staticmethod
    def deserialize(data: dict) -> 'Node':
        """Recreates a Node object from a dictionary of serialized data.

        #### Parameters:
        - data (dict): The dictionary containing the node's serialized data.

        #### Returns:
        `Node`: A new Node object initialized with the data from the dictionary.
        """
        node = Node()
        node.id = data.get('id')
        node.type = data.get('type')
        node.point = Point.deserialize(
            data['point']) if data.get('point') else None
        node.vector = Vector.deserialize(
            data['vector']) if data.get('vector') else None
        node.number = data.get('number')
        node.distance = data.get('distance')
        node.diameter = data.get('diameter')
        node.comments = data.get('comments')

        return node

    # merge
    def merge(self):
        """Merges this node with others in a project according to defined rules.

        The actual implementation of this method should consider merging nodes based on proximity or other criteria within the project context.
        """
        if project.node_merge == True:
            pass
        else:
            pass

    # snap
    def snap(self):
        """Adjusts the node's position based on snapping criteria.

        This could involve aligning the node to a grid, other nodes, or specific geometric entities.
        """
        pass

    def __str__(self) -> str:
        """Generates a string representation of the Node.

        #### Returns:
        `str`: A string that represents the Node, including its type and potentially other identifying information.
        """

        return f"{self.type}"
