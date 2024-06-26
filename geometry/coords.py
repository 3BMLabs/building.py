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
        
    def serialize(self):
        """Serializes the point object."""
        id_value = str(self.id) if not isinstance(
            self.id, (str, int, float)) else self.id
        return super().serialize() | {
            'id': id_value,
            'x': self.x,
            'y': self.y,
            'z': self.z
        }

    @staticmethod
    def deserialize(data):
        """Deserializes the point object from the provided data."""
        return Point(data['x'], data['y'], data['z'])