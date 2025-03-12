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


"""This module provides tools for creating simple systems
-planar
-one direction
"""

__title__ = "systemsimple"
__author__ = "Maarten"
__url__ = "./geometry/systemsimple.py"

import sys

from abstract.interval import Interval
from abstract.vector import Point, Vector
from construction.beam import Beam
from construction.panel import Panel
from construction.profile import RectangleProfile
from geometry.curve import Line, PolyCurve
from geometry.rect import Rect
from library.material import BaseBrick, BaseBrickYellow, BaseTimber, rgb_to_int








# [!not included in BP singlefile - end]


class System:
	"""Represents a generic system with a defined direction."""
	def __init__(self):
		"""Initializes a new System instance.
		
		- `type` (str): The class name, indicating the object type as "System".
		- `name` (str, optional): The name of the system.
		- `id` (str): A unique identifier for the system instance.
		- `polycurve` (PolyCurve, optional): An optional PolyCurve associated with the system.
		- `direction` (Vector): A Vector indicating the primary direction of the system.
		"""
		self.name = None
		
		self.polycurve = None
		self.direction: Vector = Vector(1, 0, 0)


class DivisionSystem:
	# This class provides divisionsystems. It returns lists with floats based on a length.
	"""The `DivisionSystem` class manages division systems, providing functionalities to calculate divisions and spacings based on various criteria."""
	def __init__(self):
		"""Initializes a new DivisionSystem instance.

		- `type` (str): The class name, "DivisionSystem".
		- `name` (str): The name of the division system.
		- `id` (str): A unique identifier for the division system instance.
		- `system_length` (float): The total length of the system to be divided.
		- `spacing` (float): The spacing between divisions.
		- `distance_first` (float): The distance of the first division from the start of the system.
		- `width_stud` (float): The width of a stud, applicable in certain division strategies.
		- `fixed_number` (int): A fixed number of divisions.
		- `modifier` (int): A modifier value that adjusts the number of divisions or their placement.
		- `distances` (list): A list containing the cumulative distances of each division from the start.
		- `spaces` (list): A list containing the spaces between each division.
		- `system` (str): A string indicating the current system strategy (e.g., "fixed_distance_unequal_division").
		"""
		self.name = None
		
		self.system_length: float = 100
		self.spacing: float = 10
		self.distance_first: float = 5
		self.width_stud: float = 10
		self.fixed_number: int = 2
		self.modifier: int = 0
		self.distances = []  # List with sum of distances
		self.spaces = []  # List with spaces between every divison
		self.system: str = "fixed_distance_unequal_division"

	def __fixed_number_equal_spacing(self):
		"""Calculates divisions based on a fixed number with equal spacing.
		This internal method sets up divisions across the system length, ensuring each division is equally spaced. It is triggered by configurations that require a fixed number of divisions, automatically adjusting the spacing to fit the total length.

		#### Effects:
		- Sets the division system name to "fixed_number_equal_spacing".
		- Calculates equal spacing between divisions based on the total system length and the fixed number of divisions.
		- Resets the modifier to 0, as it is not applicable in this configuration.
		- Assigns the calculated spacing to `distance_first` to maintain consistency at the start of the system.
		"""
		self.name = "fixed_number_equal_spacing"
		self.distances = Interval.by_start_end_count(
			0, self.system_length, self.fixed_number)
		self.spacing = self.system_length / self.fixed_number
		self.modifier = 0
		self.distance_first = self.spacing

	def __fixed_distance_unequal_division(self):
		"""Configures divisions with a fixed starting distance followed by unequal divisions.
		This internal method configures the division system to start with a specified distance for the first division, then continues with divisions spaced according to `spacing`. If the total length cannot be evenly divided, the last division's spacing may differ.

		#### Effects:
		- Sets the division system name to "fixed_distance_unequal_division".
		- Calculates the number of divisions based on the spacing and the total system length minus the first division's distance.
		- Generates a list of distances where each division should occur, considering the initial distance and spacing.
		"""
		self.name = "fixed_distance_unequal_division"
		rest_length = self.system_length - self.distance_first
		number_of_studs = int(rest_length / self.spacing)
		number_of_studs = number_of_studs + self.modifier
		distance = self.distance_first
		for i in range(number_of_studs+1):
			if distance < self.system_length:
				self.distances.append(distance)
			else:
				break
			distance = distance + self.spacing

	def __fixed_distance_equal_division(self):
		"""Creates divisions with equal spacing across the total system length.
		An internal method that evenly distributes divisions across the system's length. It takes into account the total length and the desired spacing to calculate the number of divisions, ensuring they are equally spaced.

		#### Effects:
		- Sets the division system name to "fixed_distance_equal_division".
		- Calculates the number of divisions based on the desired spacing and total length.
		- Determines the starting distance for the first division to ensure all divisions, including the first and last, are equally spaced within the system length.
		"""
		self.name = "fixed_distance_equal_division"
		number_of_studs = int(self.system_length / self.spacing)
		number_of_studs = number_of_studs + self.modifier
		sum_length_studs_x_spacing = (number_of_studs - 1) * self.spacing
		rest_length = self.system_length - sum_length_studs_x_spacing
		distance = rest_length / 2
		for i in range(number_of_studs):
			self.distances.append(distance)
			distance = distance + self.spacing

	def by_fixed_distance_unequal_division(self, length: float, spacing: float, distance_first: float, modifier: int) -> 'DivisionSystem':
		"""Configures the division system for unequal divisions with a specified distance first.
		This method sets up the division system to calculate divisions based on a fixed initial distance, followed by unevenly spaced divisions according to the specified parameters.

		#### Parameters:
		- `length` (float): The total length of the system to be divided.
		- `spacing` (float): The target spacing between divisions.
		- `distance_first` (float): The distance of the first division from the system's start.
		- `modifier` (int): An integer modifier to adjust the calculation of divisions.

		#### Returns:
		`DivisionSystem`: The instance itself, updated with the new division configuration.

		#### Example usage:
		```python
		division_system = DivisionSystem()
		division_system.by_fixed_distance_unequal_division(100, 10, 5, 0)
		```
		"""
		self.system_length = length
		self.modifier = modifier
		self.spacing = spacing
		self.distance_first = distance_first
		self.system = "fixed_distance_unequal_division"
		self.__fixed_distance_unequal_division()
		return self

	def by_fixed_distance_equal_division(self, length: float, spacing: float, modifier: int) -> 'DivisionSystem':
		"""Configures the division system for equal divisions with fixed spacing.
		This method sets up the division system to calculate divisions based on a fixed spacing between each division across the total system length. The modifier can adjust the calculation slightly but maintains equal spacing.

		#### Parameters:
		- `length` (float): The total length of the system to be divided.
		- `spacing` (float): The spacing between each division.
		- `modifier` (int): An integer modifier to fine-tune the division process.

		#### Returns:
		`DivisionSystem`: The instance itself, updated with the new division configuration.

		#### Example usage:
		```python
		division_system = DivisionSystem()
		division_system.by_fixed_distance_equal_division(100, 10, 0)
		```
		"""
		self.system_length = length
		self.modifier = modifier
		self.spacing = spacing
		self.system = "fixed_distance_equal_division"
		self.__fixed_distance_equal_division()
		return self

	def by_fixed_number_equal_spacing(self, length: float, number: int) -> 'DivisionSystem':
		"""Establishes the division system for a fixed number of divisions with equal spacing.
		This method arranges for a certain number of divisions to be spaced equally across the system length. It calculates the required spacing based on the total length and desired number of divisions.

		#### Parameters:
		- `length` (float): The total length of the system to be divided.
		- `number` (int): The fixed number of divisions to be created.

		#### Returns:
		`DivisionSystem`: The instance itself, updated with the new division configuration.

		#### Example usage:
		```python
		division_system = DivisionSystem()
		division_system.by_fixed_number_equal_spacing(100, 5)
		```
		"""
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
	# Reclangle Left Bottom is in Local XYZ. Main direction parallel to height direction vector. Top is z=0
	"""The `RectangleSystem` class is designed to represent and manipulate rectangular systems, focusing on dimensions, frame types, and panel arrangements within a specified coordinate system."""
	def __init__(self):
		"""Initializes a new RectangleSystem instance.
		
		- `type` (str): Class name, indicating the object type as "RectangleSystem".
		- `name` (str, optional): The name of the rectangle system.
		- `id` (str): A unique identifier for the rectangle system instance.
		- `height` (float): The height of the rectangle system.
		- `width` (float): The width of the rectangle system.
		- `bottom_frame_type` (Rectangle): A `Rectangle` instance for the bottom frame type.
		- `top_frame_type` (Rectangle): A `Rectangle` instance for the top frame type.
		- `left_frame_type` (Rectangle): A `Rectangle` instance for the left frame type.
		- `right_frame_type` (Rectangle): A `Rectangle` instance for the right frame type.
		- `inner_frame_type` (Rectangle): A `Rectangle` instance for the inner frame type.
		- `material` (BaseTimber): The material used for the system, pre-defined as `BaseTimber`.
		- `inner_width` (float): The computed inner width of the rectangle system, excluding the width of the left and right frames.
		- `inner_height` (float): The computed inner height of the rectangle system, excluding the height of the top and bottom frames.
		- `coordinatesystem` (CSGlobal): A global coordinate system applied to the rectangle system.
		- `local_coordinate_system` (CSGlobal): A local coordinate system specific to the rectangle system.
		- `division_system` (DivisionSystem, optional): A `DivisionSystem` instance to manage divisions within the rectangle system.
		- `inner_frame_objects` (list): A list of inner frame objects within the rectangle system.
		- `outer_frame_objects` (list): A list of outer frame objects.
		- `panel_objects` (list): A list of panel objects used within the system.
		- `symbolic_inner_mother_surface` (PolyCurve, optional): A symbolic representation of the inner mother surface.
		- `symbolic_inner_panels` (list, optional): Symbolic representations of inner panels.
		- `symbolic_outer_grids` (list): Symbolic representations of outer grids.
		- `symbolic_inner_grids` (list): Symbolic representations of inner grids.
		"""
		self.name = None
		
		self.height = 3000
		self.width = 2000
		self.bottom_frame_type = RectangleProfile("bottom_frame_type", 38, 184)
		self.top_frame_type = RectangleProfile("top_frame_type", 38, 184)
		self.left_frame_type = RectangleProfile("left_frame_type", 38, 184)
		self.right_frame_type = RectangleProfile("left_frame_type", 38, 184)
		self.inner_frame_type = RectangleProfile("inner_frame_type", 38, 184)

		self.material = BaseTimber
		self.inner_width: float = 0
		self.inner_height: float = 0
		# self.openings = []
		# self.subsystems = []
		self.division_system = None
		self.inner_frame_objects = []
		self.outer_frame_objects = []
		self.panel_objects = []
		self.symbolic_inner_mother_surface = None
		self.symbolic_inner_panels = None
		self.symbolic_outer_grids = []
		self.symbolic_inner_grids = []

	def __inner_panels(self):
		"""Calculates and creates inner panel objects for the RectangleSystem.
		This method iteratively calculates the positions and dimensions of inner panels based on the division system's distances and the inner frame type's width. It populates the `panel_objects` list with created panels.

		#### Effects:
		- Populates `panel_objects` with Panel instances representing the inner panels of the rectangle system.
		"""
		# First Inner panel
		i = self.division_system.distances[0]
		point1 = self.mother_surface_origin_point_x_zero
		point2 = Point.translate(self.mother_surface_origin_point_x_zero, Vector(
			i - self.inner_frame_type.b * 0.5, 0, 0))
		point3 = Point.translate(self.mother_surface_origin_point_x_zero,
								 Vector(i - self.inner_frame_type.b * 0.5, self.inner_height, 0))
		point4 = Point.translate(
			self.mother_surface_origin_point_x_zero, Vector(0, self.inner_height, 0))
		self.panel_objects.append(
			Panel.by_polycurve_thickness(
				PolyCurve.by_points(
					[point1, point2, point3, point4, point1]), 184, 0, "innerpanel",
				rgb_to_int([255, 240, 160]))
		)
		count = 0
		# In between
		for i in self.division_system.distances:
			try:
				point1 = Point.translate(self.mother_surface_origin_point_x_zero, Vector(
					self.division_system.distances[count]+self.inner_frame_type.b*0.5, 0, 0))
				point2 = Point.translate(self.mother_surface_origin_point_x_zero, Vector(
					self.division_system.distances[count+1]-self.inner_frame_type.b*0.5, 0, 0))
				point3 = Point.translate(self.mother_surface_origin_point_x_zero, Vector(
					self.division_system.distances[count+1]-self.inner_frame_type.b*0.5, self.inner_height, 0))
				point4 = Point.translate(self.mother_surface_origin_point_x_zero, Vector(
					self.division_system.distances[count]+self.inner_frame_type.b*0.5, self.inner_height, 0))
				self.panel_objects.append(
					Panel.by_polycurve_thickness(
						PolyCurve.by_points([point1, point2, point3, point4, point1]), 184, 0, "innerpanel", rgb_to_int([255, 240, 160]))
				)
				count = count + 1
			except:
				# Last panel
				point1 = Point.translate(self.mother_surface_origin_point_x_zero, Vector(
					self.division_system.distances[count]+self.inner_frame_type.b*0.5, 0, 0))
				point2 = Point.translate(self.mother_surface_origin_point_x_zero, Vector(
					self.inner_width+self.left_frame_type.b, 0, 0))
				point3 = Point.translate(self.mother_surface_origin_point_x_zero, Vector(
					self.inner_width+self.left_frame_type.b, self.inner_height, 0))
				point4 = Point.translate(self.mother_surface_origin_point_x_zero, Vector(
					self.division_system.distances[count]+self.inner_frame_type.b*0.5, self.inner_height, 0))
				self.panel_objects.append(
					Panel.by_polycurve_thickness(
						PolyCurve.by_points([point1, point2, point3, point4, point1]), 184, 0, "innerpanel", rgb_to_int([255, 240, 160]))
				)
				count = count + 1

	def __inner_mother_surface(self):
		"""Determines the inner mother surface dimensions and creates its symbolic representation.
		Calculates the inner width and height by subtracting the frame widths from the total width and height. It then constructs a symbolic PolyCurve representing the mother surface within the rectangle system's frames.

		#### Effects:
		- Updates `inner_width` and `inner_height` attributes based on frame dimensions.
		- Creates a symbolic PolyCurve `symbolic_inner_mother_surface` representing the inner mother surface.
		"""
		# Inner mother surface is the surface within the outer frames dependent on the width of the outer frametypes.
		self.inner_width = self.width-self.left_frame_type.b-self.right_frame_type.b
		self.inner_height = self.height-self.top_frame_type.b-self.bottom_frame_type.b
		self.mother_surface_origin_point = Point(
			self.left_frame_type.b, self.bottom_frame_type.b, 0)
		self.mother_surface_origin_point_x_zero = Point(
			0, self.bottom_frame_type.b, 0)
		self.symbolic_inner_mother_surface = PolyCurve.by_points(
			[self.mother_surface_origin_point,
			 Point.translate(self.mother_surface_origin_point,
							 Vector(self.inner_width, 0, 0)),
			 Point.translate(self.mother_surface_origin_point, Vector(
				 self.inner_width, self.inner_height, 0)),
			 Point.translate(self.mother_surface_origin_point,
							 Vector(0, self.inner_height, 0)),
			 self.mother_surface_origin_point]
		)

	def __inner_frames(self):
		"""Creates inner frame objects based on division distances within the rectangle system.
		Utilizes the division distances to place vertical frames across the inner width of the rectangle system. These frames are represented both as Frame objects within the system and as symbolic lines for visualization.

		#### Effects:
		- Generates Frame objects for each division, placing them vertically within the rectangle system.
		- Populates `inner_frame_objects` with these Frame instances.
		- Adds symbolic representations of these frames to `symbolic_inner_grids`.
		"""
		for i in self.division_system.distances:
			start_point = Point.translate(
				self.mother_surface_origin_point_x_zero, Vector(i, 0, 0))
			end_point = Point.translate(
				self.mother_surface_origin_point_x_zero, Vector(i, self.inner_height, 0))
			self.inner_frame_objects.append(
				Beam.by_start_point_endpoint_curve_justification(
					start_point, end_point, self.inner_frame_type.curve, "innerframe", "center", "top", 0, self.material)
			)
			self.symbolic_inner_grids.append(
				Line(start=start_point, end=end_point))

	def __outer_frames(self):
		"""Generates the outer frame objects for the rectangle system.
		Creates Frame objects for the bottom, top, left, and right boundaries of the rectangle system. Each frame is defined by its start and end points, along with its type and material. Symbolic lines representing these frames are also generated for visualization.

		#### Effects:
		- Creates Frame instances for the outer boundaries of the rectangle system and adds them to `outer_frame_objects`.
		- Generates symbolic Line instances for each outer frame and adds them to `symbolic_outer_grids`.
		"""
		bottomframe = Beam.by_start_point_endpoint_curve_justification(Point(0, 0, 0), Point(
			self.width, 0, 0), self.bottom_frame_type.curve, "bottomframe", "left", "top", 0, self.material)
		self.symbolic_outer_grids.append(
			Line(start=Point(0, 0, 0), end=Point(self.width, 0, 0)))

		topframe = Beam.by_start_point_endpoint_curve_justification(Point(0, self.height, 0), Point(
			self.width, self.height, 0), self.top_frame_type.curve, "bottomframe", "right", "top", 0, self.material)
		self.symbolic_outer_grids.append(
			Line(start=Point(0, self.height, 0), end=Point(self.width, self.height, 0)))

		leftframe = Beam.by_start_point_endpoint_curve_justification(Point(0, self.bottom_frame_type.b, 0), Point(
			0, self.height-self.top_frame_type.b, 0), self.left_frame_type.curve, "leftframe", "right", "top", 0, self.material)
		self.symbolic_outer_grids.append(Line(start=Point(
			0, self.bottom_frame_type.b, 0), end=Point(0, self.height-self.top_frame_type.b, 0)))

		rightframe = Beam.by_start_point_endpoint_curve_justification(Point(self.width, self.bottom_frame_type.b, 0), Point(
			self.width, self.height-self.top_frame_type.b, 0), self.right_frame_type.curve, "leftframe", "left", "top", 0, self.material)
		self.symbolic_outer_grids.append(Line(start=Point(self.width, self.bottom_frame_type.b, 0), end=Point(
			self.width, self.height-self.top_frame_type.b, 0)))

		self.outer_frame_objects.append(bottomframe)
		self.outer_frame_objects.append(topframe)
		self.outer_frame_objects.append(leftframe)
		self.outer_frame_objects.append(rightframe)

	def by_width_height_divisionsystem_studtype(self, width: float, height: float, frame_width: float, frame_height: float, division_system: DivisionSystem, filling: bool) -> 'RectangleSystem':
		"""Configures the rectangle system with specified dimensions, division system, and frame types.
		This method sets the dimensions of the rectangle system, configures the frame types based on the provided dimensions, and applies a division system to generate inner frames. Optionally, it can also fill the system with panels based on the inner divisions.

		#### Parameters:
		- `width` (float): The width of the rectangle system.
		- `height` (float): The height of the rectangle system.
		- `frame_width` (float): The width of the frame elements.
		- `frame_height` (float): The height (thickness) of the frame elements.
		- `division_system` (DivisionSystem): The division system to apply for inner divisions.
		- `filling` (bool): A flag indicating whether to fill the divided areas with panels.

		#### Returns:
		`RectangleSystem`: The instance itself, updated with the new configuration.

		#### Example usage:
		```python
		rectangle_system = RectangleSystem()
		rectangle_system.by_width_height_divisionsystem_studtype(2000, 3000, 38, 184, divisionSystem, True)
		```
		"""
		self.width = width
		self.height = height
		self.bottom_frame_type = RectangleProfile(
			"bottom_frame_type", frame_width, frame_height)
		self.top_frame_type = RectangleProfile(
			"top_frame_type", frame_width, frame_height)
		self.left_frame_type = RectangleProfile(
			"left_frame_type", frame_width, frame_height)
		self.right_frame_type = RectangleProfile(
			"left_frame_type", frame_width, frame_height)
		self.inner_frame_type = RectangleProfile(
			"inner_frame_type", frame_width, frame_height)
		self.division_system = division_system
		self.__inner_mother_surface()
		self.__inner_frames()
		self.__outer_frames()
		if filling:
			self.__inner_panels()
		else:
			pass
		return self


class pattern_system:
	"""The `pattern_system` class is designed to define and manipulate patterns for architectural or design applications. It is capable of generating various patterns based on predefined or dynamically generated parameters."""
	def __init__(self):
		"""Initializes a new pattern_system instance."""
		self.name = None
		
		self.pattern = None
		self.basepanels = []  # contains a list with basepanels of the system
		# contains a list sublists with Vector which represent the repetition of the system
		self.vectors = []

	def stretcher_bond_with_joint(self, name: str, brick_width: float, brick_length: float, brick_height: float, joint_width: float, joint_height: float):
		"""Configures a stretcher bond pattern with joints for the pattern_system.
		Establishes the fundamental vectors and base panels for a stretcher bond, taking into account brick dimensions and joint sizes. This pattern alternates bricks in each row, offsetting them by half a brick length.

		#### Parameters:
		- `name` (str): Name of the pattern configuration.
		- `brick_width` (float): Width of the brick.
		- `brick_length` (float): Length of the brick.
		- `brick_height` (float): Height of the brick.
		- `joint_width` (float): Width of the joint between bricks.
		- `joint_height` (float): Height of the joint between brick layers.

		#### Returns:
		The instance itself, updated with the stretcher bond pattern configuration.
	
		#### Example usage:
		```python

		```
		"""
		self.name = name
		# Vectors of panel 1
		V1 = Vector(0, (brick_height + joint_height)*2, 0)  # dy
		V2 = Vector(brick_length+joint_width, 0, 0)  # dx
		self.vectors.append([V1, V2])

		# Vectors of panel 2
		V3 = Vector(0, (brick_height + joint_height) * 2, 0)  # dy
		V4 = Vector(brick_length + joint_width, 0, 0)  # dx
		self.vectors.append([V3, V4])

		dx = (brick_length+joint_width)/2
		dy = brick_height+joint_height

		PC1 = PolyCurve().by_points([Point(0, 0, 0), Point(0, brick_height, 0), Point(
			brick_length, brick_height, 0), Point(brick_length, 0, 0), Point(0, 0, 0)])
		PC2 = PolyCurve().by_points([Point(dx, dy, 0), Point(dx, brick_height+dy, 0), Point(
			brick_length+dx, brick_height+dy, 0), Point(brick_length+dx, dy, 0), Point(dx, dy, 0)])
		BasePanel1 = Panel.by_polycurve_thickness(
			PC1, brick_width, 0, "BasePanel1", BaseBrick.colorint)
		BasePanel2 = Panel.by_polycurve_thickness(
			PC2, brick_width, 0, "BasePanel2", BaseBrick.colorint)

		self.basepanels.append(BasePanel1)
		self.basepanels.append(BasePanel2)
		return self

	def tile_bond_with_joint(self, name: str, tile_width: float, tile_height: float, tile_thickness: float, joint_width: float, joint_height: float):
		"""Configures a tile bond pattern with specified dimensions and joint sizes for the pattern_system.
		Defines a simple tiling pattern where tiles are laid out in rows and columns, separated by specified joint widths and heights. This method sets up base panels to represent individual tiles and their arrangement vectors.

		#### Parameters:
		- `name` (str): The name of the tile bond pattern configuration.
		- `tile_width` (float): The width of a single tile.
		- `tile_height` (float): The height of a single tile.
		- `tile_thickness` (float): The thickness of the tile.
		- `joint_width` (float): The width of the joint between adjacent tiles.
		- `joint_height` (float): The height of the joint between tile rows.

		#### Returns:
		The instance itself, updated with the tile bond pattern configuration.

		#### Example Usage:
		```python
		pattern_system = pattern_system()
		pattern_system.tile_bond_with_joint('TilePattern', 200, 300, 10, 5, 5)
		```
		This configures the `pattern_system` with a tile bond pattern named 'TilePattern', where each tile measures 200x300x10 units, with 5 units of spacing between tiles.
		"""
		self.name = name
		# Vectors of panel 1
		V1 = Vector(0, (tile_height + joint_height), 0)  # dy
		V2 = Vector(tile_width+joint_width, 0, 0)  # dx
		self.vectors.append([V1, V2])

		PC1 = PolyCurve().by_points([Point(0, 0, 0), Point(0, tile_height, 0), Point(
			tile_width, tile_height, 0), Point(tile_width, 0, 0)])
		BasePanel1 = Panel.by_polycurve_thickness(
			PC1, tile_thickness, 0, "BasePanel1", BaseBrick.colorint)

		self.basepanels.append(BasePanel1)
		return self

	def cross_bond_with_joint(self, name: str, brick_width: float, brick_length: float, brick_height: float, joint_width: float, joint_height: float):
		"""Configures a cross bond pattern with joints for the pattern_system.
		Sets up a complex brick laying pattern combining stretcher (lengthwise) and header (widthwise) bricks in alternating rows, creating a cross bond appearance. This method defines the base panels and their positioning vectors to achieve the cross bond pattern.

		#### Parameters:
		- `name` (str): The name of the cross bond pattern configuration.
		- `brick_width` (float): The width of a single brick.
		- `brick_length` (float): The length of the brick.
		- `brick_height` (float): The height of the brick layer.
		- `joint_width` (float): The width of the joint between bricks.
		- `joint_height` (float): The height of the joint between brick layers.

		#### Returns:
		The instance itself, updated with the cross bond pattern configuration.

		#### Example Usage:
		```python
		pattern_system = pattern_system()
		pattern_system.cross_bond_with_joint('CrossBondPattern', 90, 190, 80, 10, 10)
		```
		In this configuration, `pattern_system` is set to a cross bond pattern named 'CrossBondPattern', with bricks measuring 90x190x80 units and 10 units of joint spacing in both directions.
		"""
		self.name = name
		lagenmaat = brick_height + joint_height
		# Vectors of panel 1 (strek)
		V1 = Vector(0, (brick_height + joint_height) * 4, 0)  # dy spacing
		V2 = Vector(brick_length + joint_width, 0, 0)  # dx spacing
		self.vectors.append([V1, V2])

		# Vectors of panel 2 (koppen 1)
		V3 = Vector(0, (brick_height + joint_height) * 2, 0)  # dy spacing
		V4 = Vector(brick_length + joint_width, 0, 0)  # dx spacing
		self.vectors.append([V3, V4])

		dx2 = (brick_width + joint_width)/2  # start x offset
		dy2 = lagenmaat  # start y offset

		# Vectors of panel 3 (strekken)
		V5 = Vector(0, (brick_height + joint_height) * 4, 0)  # dy spacing
		V6 = Vector(brick_length + joint_width, 0, 0)  # dx spacing
		self.vectors.append([V5, V6])

		dx3 = (brick_length + joint_width)/2  # start x offset
		dy3 = lagenmaat * 2  # start y offset

		# Vectors of panel 4 (koppen 2)
		V7 = Vector(0, (brick_height + joint_height) * 2, 0)  # dy spacing
		V8 = Vector(brick_length + joint_width, 0, 0)  # dx spacing
		self.vectors.append([V7, V8])

		dx4 = (brick_width + joint_width)/2 + \
			(brick_width + joint_width)  # start x offset
		dy4 = lagenmaat  # start y offset

		PC1 = PolyCurve().by_points([Point(0, 0, 0), Point(0, brick_height, 0), Point(
			brick_length, brick_height, 0), Point(brick_length, 0, 0), Point(0, 0, 0)])
		PC2 = PolyCurve().by_points([Point(dx2, dy2, 0), Point(dx2, brick_height+dy2, 0), Point(
			brick_width+dx2, brick_height+dy2, 0), Point(brick_width+dx2, dy2, 0), Point(dx2, dy2, 0)])
		PC3 = PolyCurve().by_points([Point(dx3, dy3, 0), Point(dx3, brick_height+dy3, 0), Point(
			brick_length+dx3, brick_height+dy3, 0), Point(brick_length+dx3, dy3, 0), Point(dx3, dy3, 0)])
		PC4 = PolyCurve().by_points([Point(dx4, dy4, 0), Point(dx4, brick_height+dy4, 0), Point(
			brick_width+dx4, brick_height+dy4, 0), Point(brick_width+dx4, dy4, 0), Point(dx4, dy4, 0)])

		BasePanel1 = Panel.by_polycurve_thickness(
			PC1, brick_width, 0, "BasePanel1", BaseBrick.colorint)
		BasePanel2 = Panel.by_polycurve_thickness(
			PC2, brick_width, 0, "BasePanel2", BaseBrick.colorint)
		BasePanel3 = Panel.by_polycurve_thickness(
			PC3, brick_width, 0, "BasePanel3", BaseBrick.colorint)
		BasePanel4 = Panel.by_polycurve_thickness(
			PC4, brick_width, 0, "BasePanel4", BaseBrickYellow.colorint)

		self.basepanels.append(BasePanel1)
		self.basepanels.append(BasePanel2)
		self.basepanels.append(BasePanel3)
		self.basepanels.append(BasePanel4)

		return self


def pattern_geom(pattern_system, width: float, height: float, start_point: Point = None) -> list[Panel]:
	"""Generates a geometric pattern based on a pattern_system within a specified area.
	Takes a pattern_system and fills a defined width and height area starting from an optional start point with the pattern described by the system.

	#### Parameters:
	- `pattern_system`: The pattern_system instance defining the pattern.
	- `width` (float): Width of the area to fill with the pattern.
	- `height` (float): Height of the area to fill with the pattern.
	- `start_point` (Point, optional): Starting point for the pattern generation.

	#### Returns:
	`list[Panel]`: A list of Panel instances constituting the generated pattern.
	
	#### Example usage:
	```python

	```
	"""
	start_point = start_point or Point(0, 0, 0)
	test = pattern_system
	panels = []

	for i, j in zip(test.basepanels, test.vectors):
		ny = int(height / (j[0].y))  # number of panels in y-direction
		nx = int(width / (j[1].x))  # number of panels in x-direction
		PC = i.origincurve
		thickness = i.thickness
		color = i.colorint

		# YX ARRAY
		yvectdisplacement = j[0]
		yvector = Point.to_vector(start_point)
		xvectdisplacement = j[1]
		xvector = Vector(0, 0, 0)

		ylst = []
		for k in range(ny):
			yvector = yvectdisplacement + yvector
			for l in range(nx):
				# Copy in x-direction
				xvector = xvectdisplacement + xvector
				xyvector = yvector + xvector
				# translate curve in x and y-direction
				PCNew = PolyCurve.copy_translate(PC, xyvector)
				pan = Panel.by_polycurve_thickness(
					PCNew, thickness, 0, "name", color)
				panels.append(pan)
			xvector = Vector.sum(
				xvectdisplacement, Vector(-test.basepanels[0].origincurve.curves[1].length, 0, 0))
	return panels