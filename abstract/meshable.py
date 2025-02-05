from abc import abstractmethod

from geometry.mesh import Mesh

class Meshable:
	"""A Meshable is a class convertable to mesh.
	"""
	@abstractmethod
	def to_mesh() -> Mesh:
		pass