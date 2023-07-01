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


"""This module provides tools for creating simple systems
-planar
-one direction
"""

__title__= "systemsimple"
__author__ = "Maarten"
__url__ = "./geometry/systemsimple.py"

from geometry.curve import *
from abstract.coordinatesystem import *
from abstract.interval import *


class System:
    #Generic class for systems
    def __init__(self):
        self.name = None
        self.id = helper.generateID()
        self.polycurve = None
        self.direction: Vector3 = Vector3(1,0,0)


class DivisionSystem:
    # This class provides divisionsystems

    def __init__(self):
        self.name = None
        self.id = helper.generateID()
        self.system_length: float = 100
        self.spacing: float = 10
        self.distance_first: float = 5
        self.width_stud: float = 10
        self.fixed_number: int = 2
        self.modifier: int = 0
        self.distances = []
        self.system: str = "fixed_distance_unequal_division"

    def __fixed_number_equal_spacing(self):
        self.name = "fixed_number_equal_spacing"
        self.distances = Interval.bystartendcount(0, self.system_length, self.fixed_number)
        self.spacing = self.system_length / self.fixed_number
        self.modifier = 0
        self.distance_first = self.spacing

    def __fixed_distance_unequal_division(self):
        self.name = "fixed_distance_unequal_division"
        rest_length = self.system_length - self.distance_first
        number_of_studs = int(rest_length / self.spacing)
        number_of_studs = number_of_studs + self.modifier
        distance = self.distance_first
        for i in range(number_of_studs):
            self.distances.append(distance)
            distance = distance + self.spacing

    def __fixed_distance_equal_division(self):
        self.name = "fixed_distance_equal_division"
        number_of_studs = int(self.system_length / self.spacing)
        number_of_studs = number_of_studs + self.modifier
        sum_length_studs_x_spacing = (number_of_studs - 1) * self.spacing
        rest_length = self.system_length - sum_length_studs_x_spacing
        distance = rest_length / 2
        for i in range(number_of_studs):
            self.distances.append(distance)
            distance = distance + self.spacing

    def by_fixed_distance_unequal_division(self, length, spacing, distance_first, modifier):
        self.system_length = length
        self.modifier = modifier
        self.spacing = spacing
        self.distance_first = distance_first
        self.system = "fixed_distance_unequal_division"
        self.__fixed_distance_unequal_division()
        return self

    @staticmethod
    def by_fixed_distance_equal_division(length, spacing):
        obj = DivisionSystem()
        obj.system_length = length
        obj.spacing = spacing
        obj.system = "by_fixed_distance_equal_division"
        return obj

        #  fixed_number_equal_spacing
        #  fixed_number_equal_interior_fill
        #  maximum_spacing_equal_division
        #  maximum_spacing_unequal_division
        #  minimum_spacing_equal_division
        #  minimum_spacing_unequal_division

class RectangleSystem:
    #Main direction parallel to height direction vector
    def __init__(self):
        self.name = None
        self.id = helper.generateID()
        self.height = 3000
        self.width = 1000
        self.coordinatesystem = CSGlobal
        self.openings = []
        self.subsystems = []
        self.division_system: DivisionSystem = None

   def geom_substem:


