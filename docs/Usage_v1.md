# Building.py Class Documentation

## `Vector3` class

Represents a 3D vector with x, y, and z coordinates.

### Constructor

#### `__init__(self, x, y, z)`

Initializes a new Vector3 instance with the given x, y, and z coordinates.

- `x` (float): X-coordinate of the vector.
- `y` (float): Y-coordinate of the vector.
- `z` (float): Z-coordinate of the vector.

---

## Methods

- `sum(vector_1: Vector3, vector_2: Vector3) -> Vector3`: Adds two vectors element-wise.
- `diff(vector_1: Vector3, vector_2: Vector3) -> Vector3`: Subtracts two vectors element-wise.
- `scale(vector: Vector3, scalefactor: float) -> Vector3`: Scales a vector by a given factor.
- `dot_product(vector_1: Vector3, vector_2: Vector3) -> float`: Computes the dot product of two vectors.
- `cross_product(vector_1: Vector3, vector_2: Vector3) -> Vector3`: Computes the cross product of two vectors.
- `normalize(vector: Vector3) -> Vector3`: Normalizes a vector (converts it to a unit vector).
- `angle_between(vector_1: Vector3, vector_2: Vector3) -> float`: Computes the angle between two vectors in degrees.
- `__str__(self) -> str`: Converts the vector to its string representation.

### Documentation

#### `sum(vector_1: Vector3, vector_2: Vector3) -> Vector3`

Adds two vectors element-wise.

#### Parameters:
- `vector_1` (Vector3): First vector.
- `vector_2` (Vector3): Second vector.

Returns:
(Vector3): Sum of the two input vectors.

#### Example usage:

```python

```

---

#### `diff(vector_1: Vector3, vector_2: Vector3) -> Vector3`

Subtracts two vectors element-wise.

#### Parameters:
- `vector_1` (Vector3): First vector.
- `vector_2` (Vector3): Second vector.

Returns:
(Vector3): Difference of the two input vectors.

---

#### `scale(vector: Vector3, scalefactor: float) -> Vector3`

Scales a vector by a given factor.

#### Parameters:
- `vector` (Vector3): The vector to be scaled.
- `scalefactor` (float): The factor by which to scale the vector.

Returns:
(Vector3): Scaled vector.

#### Example usage:

```python

```

---

#### `dot_product(vector_1: Vector3, vector_2: Vector3) -> float`

Computes the dot product of two vectors.

#### Parameters:
- `vector_1` (Vector3): First vector.
- `vector_2` (Vector3): Second vector.

Returns:
(float): Dot product of the two input vectors.

---

#### `cross_product(vector_1: Vector3, vector_2: Vector3) -> Vector3`

Computes the cross product of two vectors.

#### Parameters:
- `vector_1` (Vector3): First vector.
- `vector_2` (Vector3): Second vector.

Returns:
(Vector3): Cross product of the two input vectors.

#### Example usage:

```python

```

---

#### `normalize(vector: Vector3) -> Vector3`

Normalizes a vector (converts it to a unit vector).

#### Parameters:
- `vector` (Vector3): The vector to be normalized.

Returns:
(Vector3): Normalized vector.

#### Example usage:

```python

```

---

#### `angle_between(vector_1: Vector3, vector_2: Vector3) -> float`

Computes the angle between two vectors in degrees.

#### Parameters:
- `vector_1` (Vector3): First vector.
- `vector_2` (Vector3): Second vector.

Returns:
(float): Angle between the two input vectors in degrees.

#### Example usage:

```python

```

---

#### `__str__(self) -> str`

Converts the vector to its string representation.

Returns:
(str): String representation of the vector.

#### Example usage:

```python

```

---

## `Point` class

Represents a point in 3D space with x, y, and z coordinates.

### Constructor

#### `__init__(self, x, y, z)`

Initializes a new Point instance with the given x, y, and z coordinates.

- `x` (float): X-coordinate of the point.
- `y` (float): Y-coordinate of the point.
- `z` (float): Z-coordinate of the point.

### Methods

- `__str__(self) -> str`: Converts the point to its string representation.
- `serialize()`: Serializes the point object.
- `deserialize(data)`: Deserializes the point object from the provided data.
- `distance(point_1, point_2) -> float`: Computes the Euclidean distance between two points.
- `distance_list(points: list) -> float`: Calculates distances between points in a list.
- `difference(point_1, point_2) -> Vector3`: Computes the difference between two points as a Vector3 object.
- `translate(point, vector) -> Point`: Translates the point by a given vector.
- `origin(point_1, point_2) -> Point`: Computes the midpoint between two points.
- `point_2D_to_3D(point2D) -> Point`: Converts a 2D point to a 3D point with zero z-coordinate.
- `to_vector(point_1) -> Vector3`: Converts the point to a Vector3 object.
- `sum(point_1, point_2) -> Point`: Computes the sum of two points.
- `diff(point_1, point_2) -> Point`: Computes the difference between two points.
- `rotate_XY(point_1, beta, dz) -> Point`: Rotates the point about the Z-axis by a given angle.
- `product(number, point_1) -> Point`: Scales the point by a given factor.
- `intersect(point_1, point_2) -> int`: Checks if two points intersect.
- `to_matrix(self) -> list`: Converts the point to a list.
- `from_matrix(self) -> Point`: Converts a list to a Point object.

### `__str__(self) -> str`

Converts the point to its string representation.

Returns:
(str): String representation of the point.

---

#### `serialize()`

Serializes the point object.

Returns:
(dict): Serialized representation of the point object.

#### Example usage:

```python

```

---

#### `deserialize(data)`

Deserializes the point object from the provided data.

#### Parameters:
- `data` (dict): Serialized data of the point object.

Returns:
(Point): Deserialized point object.

---

#### `distance(point_1, point_2) -> float`

Computes the Euclidean distance between two points.

#### Parameters:
- `point_1` (Point): First point.
- `point_2` (Point): Second point.

Returns:
(float): Euclidean distance between the two points.

#### Example usage:

```python

```

---

#### `distance_list(points: list) -> float`

Calculates distances between points in a list.

#### Parameters:
- `points` (list): List of points.

Returns:
(float): Total distance calculated between all the points in the list.

#### Example usage:

```python

```

---

#### `difference(point_1, point_2) -> Vector3`

Computes the difference between two points as a Vector3 object.

#### Parameters:
- `point_1` (Point): First point.
- `point_2` (Point): Second point.

Returns:
(Vector3): Difference between the two input points as a Vector3 object.

#### Example usage:

```python

```

---

#### `translate(point, vector) -> Point`

Translates the point by a given vector.

#### Parameters:
- `point` (Point): The point to be translated.
- `vector` (Vector3): The translation vector.

Returns:
(Point): Translated point.

#### Example usage:

```python

```

---

#### `origin(point_1, point_2) -> Point`

Computes the midpoint between two points.

#### Parameters:
- `point_1` (Point): First point.
- `point_2` (Point): Second point.

Returns:
(Point): Midpoint between the two input points.

#### Example usage:

```python

```

---

#### `point_2D_to_3D(point2D) -> Point`

Converts a 2D point to a 3D point with zero z-coordinate.

#### Parameters:
- `point2D` (Point): 2D point to be converted.

Returns:
(Point): 3D point with zero z-coordinate.

#### Example usage:

```python

```

---

#### `to_vector(point_1) -> Vector3`

Converts the point to a Vector3 object.

#### Parameters:
- `point_1` (Point): Point to be converted.

Returns:
(Vector3): Vector representation of the point.

#### Example usage:

```python

```

---

#### `sum(point_1, point_2) -> Point`

Computes the sum of two points.

#### Parameters:
- `point_1` (Point): First point.
- `point_2` (Point): Second point.

Returns:
(Point): Sum of the two input points.

#### Example usage:

```python

```

---

#### `diff(point_1, point_2) -> Point`

Computes the difference between two points.

#### Parameters:
- `point_1` (Point): First point.
- `point_2` (Point): Second point.

Returns:
(Point): Difference between the two input points.

#### Example usage:

```python

```

---

#### `rotate_XY(point_1, beta, dz) -> Point`

Rotates the point about the Z-axis by a given angle.

#### Parameters:
- `point_1` (Point): Point to be rotated.
- `beta` (float): Angle of rotation in degrees.
- `dz` (float): Offset in the z-coordinate.

Returns:
(Point): Rotated point.

#### Example usage:

```python

```

---

#### `product(number, point_1) -> Point`

Scales the point by a given factor.

#### Parameters:
- `number` (float): Scaling factor.
- `point_1` (Point): Point to be scaled.

Returns:
(Point): Scaled point.

#### Example usage:

```python

```

---

#### `intersect(point_1, point_2) -> int`

Checks if two points intersect.

#### Parameters:
- `point_1` (Point): First point.
- `point_2` (Point): Second point.

Returns:
(int): 1 if points intersect, 0 otherwise.

#### Example usage:

```python

```

---

#### `to_matrix(self) -> list`

Converts the point to a list.

Returns:
(list): List representation of the point.

#### Example usage:

```python

```

---

#### `from_matrix(self) -> Point`

Converts a list to a Point object.

Returns:
(Point): Point object created from the list.

#### Example usage:

```python

```
