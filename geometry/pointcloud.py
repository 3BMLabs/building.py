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


"""This module provides tools to create a pointcloud
"""

__title__ = "pointcloud"
__author__ = "Maarten & Jonathan"
__url__ = "./geometry/pointcloud.py"


import sys
from pathlib import Path

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

from packages.helper import *


class PointCloud:
    """Represents a collection of points in space as a point cloud."""
    
    def __init__(self, points: list) -> 'PointCloud':
        """Initializes a PointCloud object with a list of points.

        #### Parameters:
        - `points` (list): An optional list of points to initialize the point cloud. Each point can be an instance of a Point class or a tuple/list of coordinates.

        Initializes the PointCloud's attributes and sets up the list of points based on the input provided. The ID is generated to uniquely identify the point cloud.
        """
        self.type = __class__.__name__
        self.points = []
        self.id = generateID()

    def __str__(self) -> str:
        """Generates a string representation of the PointCloud object.

        #### Returns:
        `str`: A string representation of the PointCloud, including its class name and the list of points it contains.

        This method facilitates easy printing and logging of PointCloud objects, showing the collection of points within the cloud in a readable format.
        """
        return f"{__class__.__name__}({self.points})"
