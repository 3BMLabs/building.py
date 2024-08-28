# Class `Point`
Represents a point in 3D space with x, y, and z coordinates.

## Constructor

### `__init__(self, x: float, y: float, z: float) -> Point`
Initializes a new Point instance with the given x, y, and z coordinates.

        - `x` (float): X-coordinate of the point.
        - `y` (float): Y-coordinate of the point.
        - `z` (float): Z-coordinate of the point.
        

---


## Methods

- `__str__(self) -> str`: Converts the point to its string representation.

- `deserialize(data)`: Deserializes the point object from the provided data.

- `diff(point_1: Point, point_2: Point) -> Point`: Computes the difference between two points.        
        
        

- `difference(point_1: Point, point_2: Point)`: Computes the difference between two points as a Vector object.
                
        

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
        
        

- `to_vector(point: Point)`: Converts the point to a Vector object.        
        
        

- `translate(point: Point, vector) -> Point`: Translates the point by a given vector.        
        
        


## Documentation

#### `__str__(self) -> str`

Converts the point to its string representation.

---

#### `deserialize(data)`

Deserializes the point object from the provided data.

---

#### `diff(point_1: Point, point_2: Point) -> Point`

Computes the difference between two points.        

#### Parameters:
- `point_1` (Point): First point.
- `point_2` (Point): Second point.

#### Returns:
`Point`: Difference between the two input points.

#### Example usage:
```python
point_1 = Point(100.23, 182, 19)
point_2 = Point(81, 0.1, -901)
output = Point.diff(point_1, point_2)
# Point(X = 19.230, Y = 181.900, Z = 920.000)
```


---

#### `difference(point_1: Point, point_2: Point)`

Computes the difference between two points as a Vector object.

#### Parameters:
- `point_1` (Point): First point.
- `point_2` (Point): Second point.

#### Returns:
`Vector`: Difference between the two input points as a Vector object.

#### Example usage:
```python
point_1 = Point(23, 1, 23)
point_2 = Point(93, 0, -19)
output = Point.difference(point_1, point_2)
# Vector(X = 70.000, Y = -1.000, Z = -42.000)
```


---

#### `distance(point_1: Point, point_2: Point) -> float`

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

#### `distance_list(points: list[Point]) -> float`

Calculates distances between points in a list.

#### Parameters:
- `points` (list): List of points.

#### Returns:
`float`: Total distance calculated between all the points in the list.

#### Example usage:
```python
point_1 = Point(231, 13, 76)
point_2 = Point(71, 12.3, -232)
point_3 = Point(2, 71, -102)
output = Point.distance_list([point_1, point_2, point_3])
# [(<geometry.point.Point object at 0x00000226BD9CAB90>, <geometry.point.Point object at 0x00000226BA3BCFD0>, 158.45090722365714), (<geometry.point.Point object at 0x00000226BF20F710>, <geometry.point.Point object at 0x00000226BA3BCFD0>, 295.78539517697624), (<geometry.point.Point object at 0x00000226BF20F710>, <geometry.point.Point object at 0x00000226BD9CAB90>, 347.07994756251765)]
```


---

#### `from_matrix(list: list) -> Point`

Converts a list to a Point object.        

#### Parameters:
Converts a list to a Point object.

#### Returns:
`Point`: Point object created from the list.

#### Example usage:
```python
point_1 = [19, 30, 12.3]
output = Point.from_matrix(point_1)
# Point(X = 19.000, Y = 30.000, Z = 12.300)
```


---

#### `intersect(point_1: Point, point_2: Point) -> Point`

Checks if two points intersect.        

#### Parameters:
- `point_1` (Point): First point.
- `point_2` (Point): Second point.

#### Returns:
`boolean`: True if points intersect, False otherwise.

#### Example usage:
```python
point_1 = Point(23, 1, 23)
point_2 = Point(93, 0, -19)
output = Point.intersect(point_1, point_2)
# False
```


---

#### `origin(point_1: Point, point_2: Point) -> Point`

Computes the midpoint between two points.        

#### Parameters:
- `point_1` (Point): First point.
- `point_2` (Point): Second point.

#### Returns:
`Point`: Midpoint between the two input points.

#### Example usage:
```python
point_1 = Point(100.23, 182, 19)
point_2 = Point(81, 0.1, -901)
output = Point.origin(point_1, point_2)
# Point(X = 90.615, Y = 91.050, Z = -441.000)
```


---

#### `point_2D_to_3D(point_2D) -> Point`

Converts a 2D point to a 3D point with zero z-coordinate.        

#### Parameters:
- `point2D` (Point): 2D point to be converted.

#### Returns:
`Point`: 3D point with zero z-coordinate.

#### Example usage:
```python
point_1 = Point2D(19, 30)
output = Point.point_2D_to_3D(point_1)
# Point(X = 19.000, Y = 30.000, Z = 0.000)
```


---

#### `product(number: float, point: Point) -> Point`

Scales the point by a given factor.        

#### Parameters:
- `number` (float): Scaling factor.
- `point` (Point): Point to be scaled.

#### Returns:
`Point`: Scaled point.

#### Example usage:
```python
point_1 = Point(9, 20, 10)
output = Point.product(12, point_1)
# Point(X = 108.000, Y = 240.000, Z = 120.000)
```


---

#### `rotate_XY(point: Point, beta: float, dz: float) -> Point`

Rotates the point about the Z-axis by a given angle.        

#### Parameters:
- `point` (Point): Point to be rotated.
- `beta` (float): Angle of rotation in degrees.
- `dz` (float): Offset in the z-coordinate.

#### Returns:
`Point`: Rotated point.

#### Example usage:
```python
point_1 = Point(19, 30, 12.3)
output = Point.rotate_XY(point_1, 90, 12)
# Point(X = -30.000, Y = 19.000, Z = 24.300)
```


---

#### `serialize(self)`

Serializes the point object.

---

#### `sum(point_1: Point, point_2: Point) -> Point`

Computes the sum of two points.        

#### Parameters:
- `point_1` (Point): First point.
- `point_2` (Point): Second point.

#### Returns:
`Point`: Sum of the two input points.

#### Example usage:
```python
point_1 = Point(23, 1, 23)
point_2 = Point(93, 0, -19)
output = Point.sum(point_1, point_2)
# Point(X = 116.000, Y = 1.000, Z = 4.000)
```


---

#### `to_matrix(point: Point) -> Point`

Converts the point to a list.        

#### Parameters:
Converts the point to a list.

#### Returns:
`list`: List representation of the point.

#### Example usage:
```python
point_1 = Point(23, 1, 23)
output = Point.to_matrix(point_1)
# [23.0, 1.0, 23.0]
```


---

#### `to_vector(point: Point)`

Converts the point to a Vector object.        

#### Parameters:
- `point` (Point): Point to be converted.

#### Returns:
`Vector`: Vector representation of the point.

#### Example usage:
```python
point_1 = Point(9, 20, 10)
output = Point.to_vector(point_1)
# Vector(X = 9.000, Y = 20.000, Z = 10.000)
```


---

#### `translate(point: Point, vector) -> Point`

Translates the point by a given vector.        

#### Parameters:
- `point` (Point): The point to be translated.
- `vector` (Vector): The translation vector.

#### Returns:
`Point`: Translated point.

#### Example usage:
```python
point = Point(23, 1, 23)
vector = Vector(93, 0, -19)
output = Point.translate(point, vector)
# Point(X = 116.000, Y = 1.000, Z = 4.000)
```


---

