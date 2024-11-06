import math
from geometry.curve import Curve
from geometry.matrix import Matrix
from geometry.sphere import Sphere
from geometry.vector import Vector
from geometry.coords import x_axis
from geometry.point import Point

class Arc(Curve):
	def __init__(self, matrix:Matrix, angle:float) -> None:
		self.matrix, self.angle = matrix, angle
 
	@staticmethod
	def by_start_mid_end(start: Point, end: Point, mid: Point) -> 'Arc':
		#construct a matrix from a plane
		#x = (start - origin).normalized
		#y
  
		start_to_end = end - start
		half_start_end = start_to_end * 0.5
		b = half_start_end.magnitude
		radius = Sphere.radius_by_3_points(start, mid, end)
		x = math.sqrt(radius * radius - b * b)
		#mid point as if this was a straight line
		straight_line_mid = start + half_start_end
		#substract the curved mid point from the straight line mid point
		to_center = straight_line_mid - mid
		#change length to x
		to_center.magnitude = x
		origin = mid + to_center

		x_axis = start - mid
		normalized_x_axis = x_axis.normalized
		normalized_end_direction = (end - mid).normalized
		#TODO: z axis is pointing the other way when the angle is more than PI
		#dot_product = Vector.dot_product(normalized_x_axis, normalized_end_direction)
		#if dot_product > 
		normalized_z_axis = Vector.cross_product(normalized_x_axis, normalized_end_direction).normalized
		normalized_y_axis = Vector.cross_product(normalized_z_axis, normalized_x_axis)
		return Arc(Matrix.by_origin_and_axes(origin, [x_axis, normalized_y_axis * radius, normalized_z_axis]))
 
	@property
	def start(self) -> Point:
		"""

		Returns:
			Point: the starting point of this arc
		"""
		return self.matrix * x_axis

	@property
	def radius(self) -> float:
		"""

		Returns:
			Point: the radius of the circle this arc is a part of
		"""
		return self.matrix.multiply_without_translation(x_axis).magnitude

	@property
	def origin(self) -> Point:
		"""

		Returns:
			Point: the center of the circle this arc is a part of
		"""
		return self.matrix.translation


	@property
	def length(self) -> float:
		"""

		Returns:
			Point: the length of this arc
		"""
		return self.angle * self.radius

	def point_at_fraction(self, fraction: float):
		"""
  
        #### Example usage:
        ```python
        #counter-clockwise arc with center 0,0
        arc = Arc.by_start_mid_end(Point(-1,0), Point(0,1), Point(1, 0))
        #the point at fraction 0.5 is (0,1)
        
        #clockwise arc with center 0,0
        arc = Arc.by_start_mid_end(Point(-1,0), Point(0, -1), Point(1, 0))
        #the point at fraction 0.5 is (0,-1)
        ```

		Args:
			fraction (float): a value from 0 (start) to (end)

		Returns:
			Point: a point on the arc at a certain fraction
		"""
		return self.matrix * Vector.by_angle(self.angle * fraction)

	@property
	def centroid(self) -> 'Point':
		"""

		Returns:
			Point: the center of mass of this arc object
		"""
		origin = self.origin
		radius = self.radius
		angle = self.angle
		#the distance of the centroid of the arc to its origin
		centroid_distance = (2 / 3) * ((radius * (math.sin(angle) ** 3)) / (angle - math.sin(angle) * math.cos(angle)))
		return origin + centroid_distance * ((self.mid - origin) / radius)

	def __str__(self) -> 'str':
		"""Generates a string representation of the Arc object.

		#### Returns:
		`str`: A string that represents the Arc object.
		"""
		return f"{__class__.__name__}.by_start_mid_end(start={self.start}, mid={self.mid}, end={self.end})"