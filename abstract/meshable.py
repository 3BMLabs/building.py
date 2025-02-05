from abc import abstractmethod

class Meshable:
	"""A Meshable is a class convertable to mesh.
	"""
	@abstractmethod
	def to_mesh():
		pass