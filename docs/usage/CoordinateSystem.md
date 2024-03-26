# Class `CoordinateSystem`

    Represents a coordinate system in 3D space defined by an origin point and normalized x, y, and z axis vectors.
    

## Constructor

### `__init__(self, origin: geometry.point.Point, x_axis, y_axis, z_axis)`

        Initializes a new CoordinateSystem instance with the given origin and axis vectors.
        
        The axis vectors are normalized to ensure they each have a length of 1, providing a standard basis for the coordinate system.

        - `origin` (Point): The origin point of the coordinate system.
        - `x_axis` (Vector3): The initial vector representing the X-axis before normalization.
        - `y_axis` (Vector3): The initial vector representing the Y-axis before normalization.
        - `z_axis` (Vector3): The initial vector representing the Z-axis before normalization.
        

---


## Methods

- `__str__(self)`: No documentation available.

- `by_point_main_vector(self, new_origin_coordinatesystem: geometry.point.Point, DirectionVectorZ)`: 
        Creates a new CoordinateSystem at a given point, oriented along a specified direction vector.

        This method establishes a new coordinate system by defining its origin and its Z-axis direction. The X and Y axes are determined based on the given Z-axis to form a right-handed coordinate system. If the calculated X or Y axis has a zero length (in cases of alignment with the global Z-axis), default axes are used.

        

- `calculate_rotation_matrix(xaxis_1, yaxis_1, zaxis_1, xaxis_2, yaxis_2, zaxis_2)`: 
        Calculates the rotation matrix needed to align one coordinate system with another.

        

- `move_local(cs_old, x: float, y: float, z: float)`: 
        Moves a CoordinateSystem in its local coordinate space by specified displacements.

        

- `normalize(point: geometry.point.Point) -> list`: 
        Normalizes a vector to have a length of 1.

        This method calculates the normalized (unit) version of a given vector, making its length equal to 1 while preserving its direction. If the input vector has a length of 0 (i.e., it is a zero vector), the method returns the original vector.

        

- `translate(cs_old, direction)`: 
        Translates a CoordinateSystem by a given direction vector.

        

- `translate_origin(origin1, origin2)`: 
        Calculates the translation needed to move from one origin to another.

        


## Documentation

#### `__str__(self)`

No documentation available.

---

#### `by_point_main_vector(self, new_origin_coordinatesystem: geometry.point.Point, DirectionVectorZ)`


Creates a new CoordinateSystem at a given point, oriented along a specified direction vector.

This method establishes a new coordinate system by defining its origin and its Z-axis direction. The X and Y axes are determined based on the given Z-axis to form a right-handed coordinate system. If the calculated X or Y axis has a zero length (in cases of alignment with the global Z-axis), default axes are used.

#### Parameters:
- `new_origin_coordinatesystem` (`Point`): The origin point of the new coordinate system.
- `DirectionVectorZ` (Vector3): The direction vector that defines the Z-axis of the new coordinate system.

#### Returns:
`CoordinateSystem`: A new CoordinateSystem object oriented along the specified direction vector with its origin at the given point.

#### Example usage:
```python

```


---

#### `calculate_rotation_matrix(xaxis_1, yaxis_1, zaxis_1, xaxis_2, yaxis_2, zaxis_2)`


Calculates the rotation matrix needed to align one coordinate system with another.

#### Parameters:
- `xaxis_1`, `yaxis_1`, `zaxis_1` (Vector3): The axes of the initial coordinate system.
- `xaxis_2`, `yaxis_2`, `zaxis_2` (Vector3): The axes of the target coordinate system.

#### Returns:
Rotation Matrix (list of lists): A matrix representing the rotation needed to align the first coordinate system with the second.

#### Example usage:
```python

```


---

#### `move_local(cs_old, x: float, y: float, z: float)`


Moves a CoordinateSystem in its local coordinate space by specified displacements.

#### Parameters:
- `cs_old` (CoordinateSystem): The original coordinate system to be moved.
- `x` (float): The displacement along the local X-axis.
- `y` (float): The displacement along the local Y-axis.
- `z` (float): The displacement along the local Z-axis.

#### Returns:
`CoordinateSystem`: A new CoordinateSystem object moved in its local coordinate space.

#### Example usage:
```python

```


---

#### `normalize(point: geometry.point.Point) -> list`


Normalizes a vector to have a length of 1.

This method calculates the normalized (unit) version of a given vector, making its length equal to 1 while preserving its direction. If the input vector has a length of 0 (i.e., it is a zero vector), the method returns the original vector.

#### Parameters:
- `point` (list of float): A vector represented as a list of three floats, corresponding to its x, y, and z components, respectively.

#### Returns:
list of float: The normalized vector as a list of three floats. If the original vector is a zero vector, returns the original vector.

#### Example usage:
```python

```


---

#### `translate(cs_old, direction)`


Translates a CoordinateSystem by a given direction vector.

#### Parameters:
- `cs_old` (CoordinateSystem): The original coordinate system to be translated.
- `direction` (Vector3): The direction vector along which the coordinate system is to be translated.

#### Returns:
`CoordinateSystem`: A new CoordinateSystem object translated from the original one.

#### Example usage:
```python

```


---

#### `translate_origin(origin1, origin2)`


Calculates the translation needed to move from one origin to another.

#### Parameters:
- `origin1` (Point): The starting origin point.
- `origin2` (Point): The ending origin point.

#### Returns:
`Point`: A new Point object representing the translated origin.

#### Example usage:
```python

```


---

