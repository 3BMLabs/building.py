from packages.helper import generateID
from abstract.serializable import Serializable

# [!not included in BP singlefile - end]

class Coords(Serializable):
    """a shared base class for point and vector. contains the x, y and z coordinates"""
    def __init__(self, x: float, y: float, z: float) -> 'Coords':
        self.x : float = float(x)
        self.y : float = float(y)
        self.z : float = float(z)
        self.id = generateID()