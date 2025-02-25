from abc import abstractmethod
import math

from geometry.mesh import Mesh

class SegmentationSettings:
	def __init__(self, max_angle: float =  math.pi / 4):
		self.max_angle = max_angle
		"""the maximum angle to keep a straight line"""

class TesselationSettings(SegmentationSettings):
	def __init__(self, max_angle = math.pi / 4, fallback_color = 0xffffffff):
		super().__init__(max_angle)
		self.fallback_color = fallback_color

class Meshable:
	"""A Meshable is a class convertable to mesh.
	"""
	@abstractmethod
	def to_mesh(self, settings: TesselationSettings) -> Mesh:
		pass