# Class `Point`
Represents a point in 3D space with x, y, and z coordinates.

## Constructor

### `__init__(self, x, y, z)`
Initializes a new Point instance with the given x, y, and z coordinates.

        - `x` (float): X-coordinate of the point.
        - `y` (float): Y-coordinate of the point.
        - `z` (float): Z-coordinate of the point.
        

---


## Methods

- `__str__(self) -> str`: Converts the point to its string representation.

- `deserialize(data)`: Deserializes the point object from the provided data.

- `diff(point_1: Point, point_2: Point) -> Point`: Computes the difference between two points.

- `difference(point_1: Point, point_2: Point)`: Computes the difference between two points as a Vector3 object.

- `distance(point_1: Point, point_2: Point) -> float`: Computes the Euclidean distance between two 3D points.

        

- `distance_list(points: list[Point]) -> float`: Calculates distances between points in a list.

- `from_matrix(list: list) -> Point`: Converts a list to a Point object.

- `intersect(point_1: Point, point_2: Point) -> Point`: Checks if two points intersect.

- `origin(point_1: Point, point_2: Point) -> Point`: Computes the midpoint between two points.

- `point_2D_to_3D(point_2D) -> Point`: Converts a 2D point to a 3D point with zero z-coordinate.

- `product(number: float, point: Point) -> Point`: Scales the point by a given factor.

- `rotate_XY(point: Point, beta: float, dz: float) -> Point`: Rotates the point about the Z-axis by a given angle.

- `serialize(self)`: Serializes the point object.

- `sum(point_1: Point, point_2: Point) -> Point`: Computes the sum of two points.

- `to_matrix(point: Point) -> Point`: Converts the point to a list.

- `to_vector(point: Point)`: Converts the point to a Vector3 object.

- `translate(point: Point, vector) -> Point`: Translates the point by a given vector.


## Documentation

#### `__str__(self) -> str`

Converts the point to its string representation.

---

#### `deserialize(data)`

Deserializes the point object from the provided data.

---

#### `diff(point_1: 'Point', point_2: 'Point') -> 'Point'`

Computes the difference between two points.

---

#### `difference(point_1: 'Point', point_2: 'Point')`

Computes the difference between two points as a Vector3 object.

---

#### `distance(point_1: 'Point', point_2: 'Point') -> float`

Computes the Euclidean distance between two 3D points.

#### Parameters:
- `point_1` (Point): The first point.
- `point_2` (Point): The second point.

#### Returns:
`float`: The Euclidean distance between `point_1` and `point_2`.

#### Example usage:
```python
point_1 = Point(100.23, 182, 19)
point_2 = Point(81, 0.1, -901)
output = Point.distance(point_1, point_2) 
# 938.0071443757771
```

---

#### `distance_list(points: list['Point']) -> float`

Calculates distances between points in a list.

---

#### `from_matrix(list: list) -> 'Point'`

Converts a list to a Point object.

---

#### `intersect(point_1: 'Point', point_2: 'Point') -> 'Point'`

Checks if two points intersect.

---

#### `origin(point_1: 'Point', point_2: 'Point') -> 'Point'`

Computes the midpoint between two points.

---

#### `point_2D_to_3D(point_2D) -> 'Point'`

Converts a 2D point to a 3D point with zero z-coordinate.

---

#### `product(number: float, point: 'Point') -> 'Point'`

Scales the point by a given factor.

---

#### `rotate_XY(point: 'Point', beta: float, dz: float) -> 'Point'`

Rotates the point about the Z-axis by a given angle.

---

#### `serialize(self)`

Serializes the point object.

---

#### `sum(point_1: 'Point', point_2: 'Point') -> 'Point'`

Computes the sum of two points.

---

#### `to_matrix(point: 'Point') -> 'Point'`

Converts the point to a list.

---

#### `to_vector(point: 'Point')`

Converts the point to a Vector3 object.

---

#### `translate(point: 'Point', vector) -> 'Point'`

Translates the point by a given vector.

---

