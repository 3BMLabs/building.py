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


"""This module provides tools for creating simple systems
-planar
-one direction
"""

__title__= "systemsimple"
__author__ = "Maarten"
__url__ = "./geometry/systemsimple.py"

from abstract.interval import *
from objects.frame import *
from objects.panel import *

# [!not included in BP singlefile - end]

class System:
    #Generic class for systems
    def __init__(self):
        self.name = None
        self.id = generateID()
        self.polycurve = None
        self.direction: Vector3 = Vector3(1,0,0)


class DivisionSystem:
    # This class provides divisionsystems. It returns lists with floats based on a length.

    def __init__(self):
        self.name = None
        self.id = generateID()
        self.system_length: float = 100
        self.spacing: float = 10
        self.distance_first: float = 5
        self.width_stud: float = 10
        self.fixed_number: int = 2
        self.modifier: int = 0
        self.distances = [] #List with sum of distances
        self.spaces = [] #List with spaces between every divison
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
        for i in range(number_of_studs+1):
            if distance < self.system_length:
                self.distances.append(distance)
            else: break
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

    def by_fixed_distance_equal_division(self, length, spacing, modifier):
        self.system_length = length
        self.modifier = modifier
        self.spacing = spacing
        self.system = "fixed_distance_equal_division"
        self.__fixed_distance_equal_division()
        return self

    def by_fixed_number_equal_spacing(self, length, number):
        self.system_length = length
        self.system = "fixed_number_equal_spacing"
        self.spacing = length/number
        self.modifier = 0
        distance = self.spacing
        for i in range(number-1):
            self.distances.append(distance)
            distance = distance + self.spacing
        self.distance_first = self.spacing
        return self

        #  fixed_number_equal_interior_fill
        #  maximum_spacing_equal_division
        #  maximum_spacing_unequal_division
        #  minimum_spacing_equal_division
        #  minimum_spacing_unequal_division

class RectangleSystem:
    #Reclangle Left Bottom is in Local XYZ. Main direction parallel to height direction vector. Top is z=0
    def __init__(self):
        self.name = None
        self.id = generateID()
        self.height = 3000
        self.width = 2000
        self.bottom_frame_type = Rectangle("bottom_frame_type", 38, 184)
        self.top_frame_type = Rectangle("top_frame_type", 38, 184)
        self.left_frame_type = Rectangle("left_frame_type", 38, 184)
        self.right_frame_type = Rectangle("left_frame_type", 38, 184)
        self.inner_frame_type = Rectangle("inner_frame_type", 38, 184)

        self.material = BaseTimber
        self.inner_width: float =  0
        self.inner_height: float =  0
        self.coordinatesystem = CSGlobal
        self.local_coordinate_system = CSGlobal
        #self.openings = []
        #self.subsystems = []
        self.division_system = None
        self.inner_frame_objects = []
        self.outer_frame_objects = []
        self.panel_objects = []
        self.symbolic_inner_mother_surface = None
        self.symbolic_inner_panels = None
        self.symbolic_outer_grids = []
        self.symbolic_inner_grids = []

    def __inner_panels(self):
        #First Inner panel
        i = self.division_system.distances[0]
        point1 = self.mother_surface_origin_point_x_zero
        point2 = Point.translate(self.mother_surface_origin_point_x_zero, Vector3(i - self.inner_frame_type.b * 0.5, 0, 0))
        point3 = Point.translate(self.mother_surface_origin_point_x_zero,
                                 Vector3(i - self.inner_frame_type.b * 0.5, self.inner_height, 0))
        point4 = Point.translate(self.mother_surface_origin_point_x_zero, Vector3(0, self.inner_height, 0))
        self.panel_objects.append(
            Panel.byPolyCurveThickness(
                PolyCurve.byPoints([point1, point2, point3, point4, point1]), 184, 0, "innerpanel",
                rgb_to_int([255, 240, 160]))
        )
        count = 0
        # In between
        for i in self.division_system.distances:
            try:
                point1 = Point.translate(self.mother_surface_origin_point_x_zero,Vector3(self.division_system.distances[count]+self.inner_frame_type.b*0.5,0,0))
                point2 = Point.translate(self.mother_surface_origin_point_x_zero,Vector3(self.division_system.distances[count+1]-self.inner_frame_type.b*0.5,0,0))
                point3 = Point.translate(self.mother_surface_origin_point_x_zero,Vector3(self.division_system.distances[count+1]-self.inner_frame_type.b*0.5,self.inner_height,0))
                point4 = Point.translate(self.mother_surface_origin_point_x_zero,Vector3(self.division_system.distances[count]+self.inner_frame_type.b*0.5, self.inner_height, 0))
                self.panel_objects.append(
                    Panel.byPolyCurveThickness(
                        PolyCurve.byPoints([point1,point2,point3,point4,point1]),184,0,"innerpanel",rgb_to_int([255,240,160]))
                    )
                count = count + 1
            except:
                #Last panel
                point1 = Point.translate(self.mother_surface_origin_point_x_zero,Vector3(self.division_system.distances[count]+self.inner_frame_type.b*0.5,0,0))
                point2 = Point.translate(self.mother_surface_origin_point_x_zero,Vector3(self.inner_width+self.left_frame_type.b,0,0))
                point3 = Point.translate(self.mother_surface_origin_point_x_zero,Vector3(self.inner_width+self.left_frame_type.b,self.inner_height,0))
                point4 = Point.translate(self.mother_surface_origin_point_x_zero,Vector3(self.division_system.distances[count]+self.inner_frame_type.b*0.5, self.inner_height, 0))
                self.panel_objects.append(
                    Panel.byPolyCurveThickness(
                        PolyCurve.byPoints([point1,point2,point3,point4,point1]),184,0,"innerpanel",rgb_to_int([255,240,160]))
                    )
                count = count + 1

    def __inner_mother_surface(self):
        #Inner mother surface is the surface within the outer frames dependent on the width of the outer frametypes.
        self.inner_width = self.width-self.left_frame_type.b-self.right_frame_type.b
        self.inner_height = self.height-self.top_frame_type.b-self.bottom_frame_type.b
        self.mother_surface_origin_point = Point(self.left_frame_type.b,self.bottom_frame_type.b,0)
        self.mother_surface_origin_point_x_zero = Point(0,self.bottom_frame_type.b,0)
        self.symbolic_inner_mother_surface = PolyCurve.byPoints(
            [self.mother_surface_origin_point,
             Point.translate(self.mother_surface_origin_point,Vector3(self.inner_width,0,0)),
             Point.translate(self.mother_surface_origin_point,Vector3(self.inner_width,self.inner_height,0)),
             Point.translate(self.mother_surface_origin_point, Vector3(0, self.inner_height, 0)),
             self.mother_surface_origin_point]
        )

    def __inner_frames(self):
        for i in self.division_system.distances:
            start_point = Point.translate(self.mother_surface_origin_point_x_zero,Vector3(i,0,0))
            end_point = Point.translate(self.mother_surface_origin_point_x_zero,Vector3(i,self.inner_height,0))
            self.inner_frame_objects.append(
                Frame.byStartpointEndpointCurveJustifiction(start_point,end_point, self.inner_frame_type.curve, "innerframe","center","top", 0,self.material)
            )
            self.symbolic_inner_grids.append(Line(start=start_point,end=end_point))

    def __outer_frames(self):
        bottomframe = Frame.byStartpointEndpointCurveJustifiction(Point(0,0,0),Point(self.width,0,0), self.bottom_frame_type.curve, "bottomframe","left","top", 0,self.material)
        self.symbolic_outer_grids.append(Line(start=Point(0,0,0), end=Point(self.width,0,0)))

        topframe = Frame.byStartpointEndpointCurveJustifiction(Point(0,self.height,0),Point(self.width,self.height,0), self.top_frame_type.curve, "bottomframe","right","top", 0,self.material)
        self.symbolic_outer_grids.append(Line(start=Point(0,self.height,0), end=Point(self.width,self.height,0)))

        leftframe = Frame.byStartpointEndpointCurveJustifiction(Point(0,self.bottom_frame_type.b,0),Point(0,self.height-self.top_frame_type.b,0), self.left_frame_type.curve, "leftframe","right","top", 0,self.material)
        self.symbolic_outer_grids.append(Line(start=Point(0,self.bottom_frame_type.b,0), end=Point(0,self.height-self.top_frame_type.b,0)))

        rightframe = Frame.byStartpointEndpointCurveJustifiction(Point(self.width,self.bottom_frame_type.b,0),Point(self.width,self.height-self.top_frame_type.b,0), self.right_frame_type.curve, "leftframe","left","top", 0,self.material)
        self.symbolic_outer_grids.append(Line(start=Point(self.width,self.bottom_frame_type.b,0), end=Point(self.width,self.height-self.top_frame_type.b,0)))

        self.outer_frame_objects.append(bottomframe)
        self.outer_frame_objects.append(topframe)
        self.outer_frame_objects.append(leftframe)
        self.outer_frame_objects.append(rightframe)
    def by_width_height_divisionsystem_studtype(self,width,height,framewidth,frameheight,division_system,filling):
        self.width = width
        self.height = height
        self.bottom_frame_type = Rectangle("bottom_frame_type", framewidth, frameheight)
        self.top_frame_type = Rectangle("top_frame_type", framewidth, frameheight)
        self.left_frame_type = Rectangle("left_frame_type", framewidth, frameheight)
        self.right_frame_type = Rectangle("left_frame_type", framewidth, frameheight)
        self.inner_frame_type = Rectangle("inner_frame_type", framewidth, frameheight)
        self.division_system = division_system
        self.__inner_mother_surface()
        self.__inner_frames()
        self.__outer_frames()
        if filling:
            self.__inner_panels()
        else:
            pass
        return self


#   def geom_substem:


