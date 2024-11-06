import math
from abstract.matrix import Matrix
from abstract.vector import Vector
from geometry.coords import x_axis, y_axis
from geometry.point import Point

class Curve:
	@property
	def start(self) -> Point:
		return self.point_at_fraction(0)
	@property
	def mid(self) -> Point:
		return self.point_at_fraction(0.5)
	@property
	def end(self) -> Point:
		return self.point_at_fraction(1)

class Arc(Curve):
	def __init__(self, matrix:Matrix, angle:float) -> None:
		self.matrix, self.angle = matrix, angle
	
	@staticmethod
	def radius_by_3_points(start:float, mid: float, end: float) -> float:
		a = Point.distance(start, mid)
		b = Point.distance(mid, end)
		c = Point.distance(end, start)
		s = (a + b + c) / 2
		A = math.sqrt(max(s * (s - a) * (s - b) * (s - c), 0))
				
		if abs(A) < 1e-6:
			return float('inf')
		else:
			R = (a * b * c) / (4 * A)
			return R
 
	@staticmethod
	def by_start_mid_end(self, start: Point, end: Point, mid: Point) -> 'Arc':
		#construct a matrix from a plane
		#x = (start - origin).normalized
		#y
  
		start_to_end = end - start
		half_start_end = start_to_end * 0.5
		b = half_start_end.magnitude
		radius = Arc.radius_by_3_points(start, mid, end)
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
		normalized_z_axis = Vector.cross_product(normalized_x_axis, normalized_end_direction).normalized
		normalized_y_axis = Vector.cross_product(normalized_z_axis, normalized_x_axis)
		return Arc(Matrix.by_origin_and_axes(origin, [x_axis, normalized_y_axis * radius, normalized_z_axis]))
 
	@property
	def start(self) -> Point:
		return self.matrix * x_axis
	def point_at_fraction(self, fraction: float):
		return self.matrix * Vector.by_angle(self.angle * fraction)
	def radius(self):
		return self.matrix.multiply_without_translation(x_axis).magnitude
	def origin(self):
		return self.matrix.translation