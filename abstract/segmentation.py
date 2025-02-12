from abc import abstractmethod
import math

from geometry.mesh import Mesh

class SegmentationSettings:
	def __init__(self, max_angle: float =  math.pi / 4):
		self.max_angle = max_angle
		"""the maximum angle to keep a straight line"""
 
class Meshable:
	"""A Meshable is a class convertable to mesh.
	"""
	@abstractmethod
	def to_mesh(settings: SegmentationSettings) -> Mesh:
		pass