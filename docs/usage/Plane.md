# Class `Plane`
The `Plane` class represents an infinite plane in 3D space, defined uniquely by an origin point and a normal vector, along with two other vectors lying on the plane, providing a complete basis for defining plane orientation and position.

## Constructor

### `__init__(self)`
"Initializes a new Plane instance.

        - `Origin` (Point): The origin point of the plane, which also lies on the plane.
        - `Normal` (Vector3): A vector perpendicular to the plane, defining its orientation.
        - `v1` (Vector3): A vector lying on the plane, typically representing the "x" direction on the plane.
        - `v2` (Vector3): Another vector on the plane, perpendicular to `v1` and typically representing the "y" direction on the plane.
        

---


## Methods

- `__str__(self) -> str`: Generates a string representation of the Plane.

        

- `deserialize(data: dict) -> Plane`: Creates a Plane object from a serialized data dictionary.
        This method allows for the reconstruction of a Plane instance from data previously serialized into a dictionary format, typically after storage or transmission.

        

- `serialize(self) -> dict`: Serializes the plane's attributes into a dictionary.
        This method facilitates the conversion of the plane's properties into a format that can be easily stored or transmitted.

        


## Documentation

#### `__str__(self) -> str`

Generates a string representation of the Plane.

#### Returns:
str: A string describing the Plane with its origin, normal, and basis vectors.

#### Example usage:
```python

```


---

#### `deserialize(data: dict) -> Plane`

Creates a Plane object from a serialized data dictionary.
This method allows for the reconstruction of a Plane instance from data previously serialized into a dictionary format, typically after storage or transmission.

#### Parameters:
data (dict): The dictionary containing the serialized data of a Plane object.

#### Returns:
Plane: A new Plane object initialized with the data from the dictionary.

#### Example usage:
```python

```


---

#### `serialize(self) -> dict`

Serializes the plane's attributes into a dictionary.
This method facilitates the conversion of the plane's properties into a format that can be easily stored or transmitted.

#### Returns:
dict: A dictionary containing the serialized attributes of the plane.

#### Example usage:
```python

```


---

