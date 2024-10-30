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


"""This module forms the base for points and vectors
"""

__title__ = "coords"
__author__ = "JohnHeikens"
__url__ = "./geometry/coords.py"

import math
from typing import Self
from abstract.serializable import Serializable

import operator

# [!not included in BP singlefile - end]
def to_array(*args) -> list:
    """converts the arguments into an array.

    Returns:
        list: the arguments provided, converted to a list.
    """
    return args[0] if len(args) == 1 and hasattr(args[0], "__getitem__") else list(args)


class Coords(Serializable, list):
    """
    a shared base class for point and vector. contains the x, y and z coordinates.
    operations you do with these coords will apply for the children.
    for example: Vector(2, 4, 6) / 2 = Vector(1, 2, 3)
    or: Vector(2,5) ** 2 = Vector(4, 25)
    Vectors can also be nested.
    """
    def __init__(self, *args, **kwargs) -> 'Coords':
        arrayArgs:list = to_array(*args)

        list.__init__(self, arrayArgs)
        Serializable.__init__(self)

        for kwarg in kwargs.items():
            self.set_axis_by_name(kwarg[0], kwarg[1])            

    def __str__(self):
        return self.__class__.__name__ + '(' + ','.join([f'{axis_name}={((v * 100) // 1 ) / 100 }' for v, axis_name in zip(self, self.axis_names)]) + ')'
    
    axis_names = ['x', 'y', 'z', 'w']
    
    @property
    def x(self): return self[0]
    @x.setter
    def x(self, value): self[0] = value
        
    @property
    def y(self): return self[1]
    @y.setter
    def y(self, value): self[1] = value

    @property
    def z(self): return self[2]
    @z.setter
    def z(self, value): self[2] = value

    @property
    def w(self): return self[3]
    @w.setter
    def w(self, value): self[3] = value
    
    @property
    def squared_magnitude(self):
        result = 0
        for axis_value in self:
            result += axis_value * axis_value
        return result
    squared_length = squared_magnitude
    
    @property
    def magnitude(self): 
        """the 'length' could also mean the axis count. this makes it more clear.
        Returns:
            the length
        """
        return math.sqrt(self.squared_magnitude)
    length = magnitude
    
    @magnitude.setter
    def magnitude(self, value):
        """Rescales the vector to have the specified length.

        #### Parameters:
        - `vector_1` (`Vector`): The vector to be rescaled.
        - `newlength` (float): The desired length of the vector.

        #### Returns:
        `Vector`: A new Vector object representing the rescaled vector.

        #### Example usage:
        ```python
        vector = Vector(3, 4, 0)
        new_vector = Vector.new_length(vector, 5)
        # Vector(X = 3.000, Y = 4.000, Z = 0.000)
        ```
        """
        self *= value / self.magnitude
    
    @property
    def normalized(self):
        """Returns the normalized form of the vector.
        The normalized form of a vector is a vector with the same direction but with a length (magnitude) of 1.

        #### Returns:
        `Vector`: A new Vector object representing the normalized form of the input vector.

        #### Example usage:
        ```python
        vector1 = Vector(3, 0, 4)
        normalized_vector = vector1.normalized
        # Vector(X = 0.600, Y = 0.000, Z = 0.800)
        ```
        """
        sqm = self.squared_magnitude
        
        return self / math.sqrt(sqm) if sqm > 0 else Coords()
    
    @property
    def angle(self) -> float:
        """output range: -PI to PI

        Returns:
            float: the arc tangent of y / x in radians
        """
        #treat this normal vector as a triangle. we know all sides but want to know the angle.
        #tan(deg) = other side / straight side
        #deg = atan(other side / straight side)
        return math.atan2(self.x, self.y)
    
    @staticmethod
    def by_coordinates(x: float, y: float, z:float = None):
        return Coords(x, y, z) if z is not None else Coords(x, y)
    
    @staticmethod
    def by_list(coordinate_list: list):
        return Coords(coordinate_list)
    
    @staticmethod
    def angle_between(vector_1: 'Coords', vector_2: 'Coords') -> float:
        """Computes the angle in degrees between two coords.
        The angle between two coords is the angle required to rotate one vector onto the other, measured in degrees.

        #### Parameters:
        - `vector_1` (`Vector`): The first vector.
        - `vector_2` (`Vector`): The second vector.

        #### Returns:
        `float`: The angle in degrees between the input coords.

        #### Example usage:
        ```python
        vector1 = Vector(1, 0, 0)
        vector2 = Vector(0, 1, 0)
        angle = Vector.angle_between(vector1, vector2)
        # 90
        ```
        """
        dot_product = Coords.dot_product(vector_1, vector_2)
        length_vector_1 = vector_1.magnitude
        length_vector_2 = vector_2.magnitude

        if length_vector_1 == 0 or length_vector_2 == 0:
            return 0

        cos_angle = dot_product / (length_vector_1 * length_vector_2)
        cos_angle = max(-1.0, min(cos_angle, 1.0))
        return math.acos(cos_angle)

    @staticmethod
    def dot_product(vector_1: 'Coords', vector_2: 'Coords') -> 'float':
        """Computes the dot product of two vectors.
        The dot product of two vectors is a scalar quantity equal to the sum of the products of their corresponding components. It gives insight into the angle between the vectors.

        #### Parameters:
        - `vector_1` (`Coords`): The first vector.
        - `vector_2` (`Coords`): The second vector.

        #### Returns:
        `float`: The dot product of the input vectors.

        #### Example usage:
        ```python
        vector1 = Vector(1, 2, 3)
        vector2 = Vector(4, 5, 6)
        dot_product = Vector.dot_product(vector1, vector2)
        # 32
        ```
        """
        total = 0
        for i in range(len(vector_1)):
            total += vector_1[i] * vector_2 [i]
        return total
    
    @staticmethod
    def distance_squared(point_1: 'Coords', point_2: 'Coords') -> float:
        """Computes the Euclidean distance between two 3D points.

        #### Parameters:
        - `point_1` (Coords): The first point.
        - `point_2` (Coords): The second point.

        #### Returns:
        `float`: The Euclidean distance between `point_1` and `point_2`.

        #### Example usage:
    	```python
        point_1 = Coords(0, 0, 400)
        point_2 = Coords(300, 0, 400)
        output = Coords.distance(point_1, point_2) 
        # 90000
        ```
        """
        return (point_2 - point_1).squared_magnitude
    
    @staticmethod
    def distance(point_1: 'Coords', point_2: 'Coords') -> float:
        """Computes the Euclidean distance between two 3D points.

        #### Parameters:
        - `point_1` (Coords): The first point.
        - `point_2` (Coords): The second point.

        #### Returns:
        `float`: The Euclidean distance between `point_1` and `point_2`.

        #### Example usage:
    	```python
        point_1 = Coords(0, 0, 400)
        point_2 = Coords(300, 0, 400)
        output = Coords.distance(point_1, point_2) 
        # 90000
        ```
        """
        return (point_2 - point_1).magnitude
    
    @staticmethod
    def axis_index(axis:str) -> int:
        """returns index of axis name.<br>
        raises a valueError when the name isn't valid.

        Args:
            axis (str): the name of the axis

        Returns:
            int: the index
        """
        return Coords.axis_names.index(axis.lower())

    def change_axis_count(self,axis_count: int):
        """in- or decreases the amount of axes to the preferred axis count.

        Args:
            axis_count (int): the new amount of axes
        """
        if axis_count > len(self):
            diff = axis_count + 1 - len(self)
            self.extend([0] * diff)
        else:
            self = self[:axis_count]
    def set_axis(self, axis_index: int, value) -> int | None:
        """sets an axis with the specified index to the value. will resize when the coords can't contain them.

        Args:
            axis_index (int): the index of the axis, for example 2
            value: the value to set the axis to

        Returns:
            int: the new size when resized, -1 when the axis is invalid, None when the value was just set.
        """

        if axis_index >= len(self):
            self.extend([0] * (axis_index - len(self)))
            self.extend([value])
            return axis_index
        self[axis_index] = value
        return None
        
    def set_axis_by_name(self, axis_name: str, value) -> int | None:
        """sets an axis with the specified name to the value. will resize when the coords can't contain them.

        Args:
            axis_name (str): the name of the axis, for example 'x'
            value: the value to set the axis to

        Returns:
            int: the new size when resized, -1 when the axis is invalid, None when the value was just set.
        """
        return self.set_axis(Coords.axis_index(axis_name), value)
    
    @staticmethod
    def by_two_points(point_1: 'Coords', point_2: 'Coords') -> 'Coords':
        """Computes the vector between two points.

        #### Parameters:
        - `point_1` (`Coords`): The starting point.
        - `point_2` (`Coords`): The ending point.

        #### Returns:
        `Vector`: A new Vector object representing the vector between the two points.

        #### Example usage:
        ```python
        point1 = Point(1, 2, 3)
        point2 = Point(4, 6, 8)
        vector = Vector.by_two_points(point1, point2)
        # Vector(X = 3, Y = 4, Z = 5)
        ```
        """
        return point_2 - point_1
        
    def volume(self):
        result = 1
        for val in self:
            result *= val
        return result
        
    #useful for sorting
    def compare(self, other):
        for axis in range(len(self)):
            if self[axis] != other[axis]:
                return other[axis] - self[axis]
        return 0
    
    def ioperate_2(self, op: operator, other):
        try:
            for index in range(len(self)):
                self[index] = op(self[index], other[index])
        except TypeError:
            #variable doesn't support index
            #https://stackoverflow.com/questions/7604380/check-for-operator
            for index in range(len(self)):
                self[index] = op(self[index], other)
        return self
    
    def operate_2(self, op:operator, other):
        result = Coords([0] * len(self))
        try:
            for index in range(len(self)):
                result[index] = op(self[index], other[index])
        except TypeError:
            #variable doesn't support index
            #https://stackoverflow.com/questions/7604380/check-for-operator
            for index in range(len(self)):
                result[index] = op(self[index], other)
        return result
    def operate_1(self, op:operator):
        result = Coords([0] * len(self))
        for index in range(len(self)):
            result[index] = op(self[index])
        return result
    
    def __add__(self, other):
        """Calculates the sum of two vectors.
        
        equivalent to the + operator.
        
        """
        return self.operate_2(operator.__add__,other)
    
    sum = __add__
    
    def __sub__(self, other):
        """Calculates the difference between two Vector objects.
        This method returns a new Vector object that is the result of subtracting the components of `vector_2` from `vector_1`.

        equivalent to the - operator.

        #### Parameters:
        - `vector_1` (`Vector`): The minuend vector.
        - `vector_2` (`Vector`): The subtrahend vector.

        #### Returns:
        `Vector`: A new Vector object resulting from the component-wise subtraction of `vector_2` from `vector_1`.

        #### Example usage:
        ```python
        vector1 = Vector(5, 7, 9)
        vector2 = Vector(1, 2, 3)
        result = Vector.diff(vector1, vector2)
        # Vector(X = 4.000, Y = 5.000, Z = 6.000)
        ```
        """
        return self.operate_2(operator.__sub__,other)
    

    difference = diff = substract = __sub__
    
    def __truediv__(self, other):
        """Divides the components of the first vector by the corresponding components of the second vector.
        This method performs component-wise division. If any component of `vector_2` is 0, the result for that component will be undefined.

        equivalent to the / operator.

        #### Parameters:
        - `vector_1` (`Vector`): The numerator vector.
        - `vector_2` (`Vector`): The denominator vector.

        #### Returns:
        `Vector`: A new Vector object resulting from the component-wise division.

        #### Example usage:
        ```python
        vector1 = Vector(10, 20, 30)
        vector2 = Vector(2, 4, 5)
        result = Vector.divide(vector1, vector2)
        # Vector(X = 5.000, Y = 5.000, Z = 6.000)
        ```
        """
        return self.operate_2(operator.__truediv__,other)
    
    divide = __truediv__
    
    def __mul__(self, other):
        """Scales the vector by the specified scale factor.

        equivalent to the * operator.

        #### Parameters:
        - `vector` (`Vector`): The vector to be scaled.
        - `scalefactor` (float): The scale factor.

        #### Returns:
        `Vector`: A new Vector object representing the scaled vector.

        #### Example usage:
        ```python
        vector = Vector(1, 2, 3)
        scaled_vector = Vector.scale(vector, 2)
        # Vector(X = 2, Y = 4, Z = 6)
        ```
        """
        return self.operate_2(operator.__mul__,other)
    product = scale = __rmul__ = __mul__
    
    
    
    def __pow__(self, power: float) -> Self:
        """raises the vector to a certain power.
        
        equivalent to the ** operator.

        Returns:
            Self: a vector with all components raised to the specified power
        """
        return self.ioperate_2(operator.__pow__)
    
    def __neg__(self) -> Self:
        """negates this vector.

        equivalent to the - operator.

        Returns:
            Self: a vector with all components negated.
        """
        return self.operate_1(operator.__neg__)
    
    reverse = __neg__
    
    @staticmethod
    def square(self) -> 'Coords':
        """
        Computes the square of each component of the input vector.

        #### Parameters:
        - `vector_1` (`Vector`): The input vector.

        #### Returns:
        `Vector`: A new Vector object representing the square of each component of the input vector.

        #### Example usage:
        ```python
        vector = Vector(2, 3, 4)
        squared_vector = Vector.square(vector)
        # Vector(X = 4, Y = 9, Z = 16)
        ```
        """
        return self ** 2
    
    
    #i operators. these operate on self (+=, *=, etc)
    
    def __iadd__(self, other) -> Self:
        """Translates the point by a given vector.        

        equivalent to the += operator.
        
        #### Parameters:
        - `point` (Point): The point to be translated.
        - `vector` (Vector): The translation vector.

        #### Returns:
        `Point`: Translated point.

        #### Example usage:
    	```python
        point = Point(23, 1, 23)
        vector = Vector(93, 0, -19)
        output = Point.translate(point, vector)
        # Point(X = 116.000, Y = 1.000, Z = 4.000)
        ```
        """
        return self.ioperate_2(operator.__iadd__,other)

    translate = __iadd__
    
    def __isub__(self, other) -> Self:
        return self.ioperate_2(operator.__isub__,other)
    
    def __imul__(self, other) -> Self:
        return self.ioperate_2(operator.__imul__,other)
    
    def __itruediv__(self, other) -> Self:
        return self.ioperate_2(operator.__itruediv__,other)

X_axis = Coords(1, 0, 0)

Y_Axis = Coords(0, 1, 0)

Z_Axis = Coords(0, 0, 1)
Coords.left = Coords(-1, 0, 0)
Coords.right = Coords(1, 0, 0)
Coords.down = Coords(0, -1, 0)
Coords.up = Coords(0, 1, 0)
Coords.backward = Coords(0, 0, -1)
Coords.forward = Coords(0, 0, 1)
