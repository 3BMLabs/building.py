# Class `Vector`
Represents a 3D vector with x, y, and z coordinates.

## Constructor

### `__init__(self, x: float, y: float, z: float) -> Vector`
Initializes a new Vector instance with the given x, y, and z coordinates.

        - `x` (float): X-coordinate of the vector.
        - `y` (float): Y-coordinate of the vector.
        - `z` (float): Z-coordinate of the vector.
        

---


## Methods

- `__str__(self)`: Returns a string representation of the vector.

        

- `angle_between(vector_1: Vector, vector_2: Vector) -> float`: Computes the angle in degrees between two vectors.
        The angle between two vectors is the angle required to rotate one vector onto the other, measured in degrees.

        

- `angle_between_XY(vector_1: Vector, vector_2: Vector) -> float`: Computes the angle in degrees between two vectors projected onto the XY plane (Z-axis rotation).

        

- `angle_between_XZ(vector_1: Vector, vector_2: Vector) -> float`: Computes the angle in degrees between two vectors projected onto the XZ plane (Y-axis rotation).

        

- `angle_between_YZ(vector_1: Vector, vector_2: Vector) -> float`: Computes the angle in degrees between two vectors projected onto the YZ plane (X-axis rotation).

        

- `angle_radian_between(vector_1: Vector, vector_2: Vector) -> float`: Computes the angle in radians between two vectors.
        The angle between two vectors is the angle required to rotate one vector onto the other, measured in radians.

        

- `by_line(line_1) -> Vector`: Computes a vector representing the direction of a given line.
        This method takes a Line object and returns a Vector representing the direction of the line.

        

- `by_two_points(point_1: Point, point_2: Point) -> Vector`: Computes the vector between two points.

        

- `cross_product(vector_1: Vector, vector_2: Vector) -> Vector`: Computes the cross product of two vectors.
        The cross product of two vectors in three-dimensional space is a vector that is perpendicular to both original vectors. It is used to find a vector that is normal to a plane defined by the input vectors.

        

- `deserialize(data)`: Converts a dictionary representation of a vector into a Vector object.
        This method takes a dictionary containing 'x', 'y', and 'z' keys with numeric values and creates a new Vector instance representing the vector described by these values. It's particularly useful for converting serialized vector data back into Vector objects, for instance, when loading vectors from a file or a database.

        

- `diff(vector_1: Vector, vector_2: Vector) -> Vector`: Calculates the difference between two Vector objects.
        This method returns a new Vector object that is the result of subtracting the components of `vector_2` from `vector_1`.

        

- `divide(vector_1: Vector, vector_2: Vector) -> Vector`: Divides the components of the first vector by the corresponding components of the second vector.
        This method performs component-wise division. If any component of `vector_2` is 0, the result for that component will be undefined.

        

- `dot_product(vector_1: Vector, vector_2: Vector) -> Vector`: Computes the dot product of two vectors.
        The dot product of two vectors is a scalar quantity equal to the sum of the products of their corresponding components. It gives insight into the angle between the vectors.

        

- `from_matrix(vector_list: list) -> Vector`: Creates a Vector object from a list representation.

        

- `length(vector_1: Vector) -> float`: Computes the length (magnitude) of a vector.
        The length of a vector is the Euclidean norm or magnitude of the vector, which is calculated as the square root of the sum of the squares of its components.

        

- `new_length(vector_1: Vector, newlength: float) -> Vector`: Rescales the vector to have the specified length.

        

- `normalize(vector_1: Vector) -> Vector`: Returns the normalized form of the input vector.
        The normalized form of a vector is a vector with the same direction but with a length (magnitude) of 1.

        

- `perpendicular(vector_1: Vector) -> tuple`: Computes two vectors perpendicular to the input vector.

        

- `pitch(vector_1: Vector, angle: float) -> Vector`: Rotates a vector around the X-axis (pitch).
        This method rotates the vector around the X-axis (pitch) by the specified angle.

        

- `product(number: float, vector_1: Vector) -> Vector`: Scales a vector by a scalar value.
        This method multiplies each component of the vector by the given scalar value.

        

- `reverse(vector_1: Vector) -> Vector`: Returns the reverse (negation) of the vector.

        

- `rotate_XY(vector: Vector, Beta: float) -> Vector`: Rotates the vector in the XY plane by the specified angle.

        

- `scale(vector: Vector, scalefactor: float) -> Vector`: Scales the vector by the specified scale factor.

        

- `serialize(self) -> dict`: Serializes the Vector object into a dictionary.

        

- `square(vector_1: Vector) -> Vector`: 
        Computes the square of each component of the input vector.

        

- `subtract(vector_1: Vector, vector_2: Vector) -> Vector`: Subtracts the components of the second vector from the first.
        This method is synonymous with `diff` and serves the same purpose, providing an alternative naming convention.

        

- `sum(vector_1: Vector, vector_2: Vector) -> Vector`: Adds two vectors element-wise.        
        
        

- `sum3(vector_1: Vector, vector_2: Vector, vector_3: Vector) -> Vector`: Calculates the sum of three Vector objects.
        This method returns a new Vector object whose components are the sum of the corresponding components of the three input vectors.

        

- `to_line(vector_1: Vector, vector_2: Vector) -> Vector`: Creates a Line object from two vectors.

        

- `to_matrix(vector: Vector) -> list`: Converts the vector to a list representation.

        

- `to_point(vector_1: Vector) -> Vector`: Converts the vector to a Point object.

        

- `value(vector_1: Vector) -> tuple`: Returns the rounded values of the vector's components.

        


## Documentation

#### `__str__(self)`

Returns a string representation of the vector.

#### Returns:
`str`: A string representation of the vector.

#### Example usage:
```python
vector = Vector(1.234, 2.345, 3.456)
print(vector)
# Vector(X = 1.234, Y = 2.345, Z = 3.456)
```


---

#### `angle_between(vector_1: Vector, vector_2: Vector) -> float`

Computes the angle in degrees between two vectors.
The angle between two vectors is the angle required to rotate one vector onto the other, measured in degrees.

#### Parameters:
- `vector_1` (`Vector`): The first vector.
- `vector_2` (`Vector`): The second vector.

#### Returns:
`float`: The angle in degrees between the input vectors.

#### Example usage:
```python
vector1 = Vector(1, 0, 0)
vector2 = Vector(0, 1, 0)
angle = Vector.angle_between(vector1, vector2)
# 90
```


---

#### `angle_between_XY(vector_1: Vector, vector_2: Vector) -> float`

Computes the angle in degrees between two vectors projected onto the XY plane (Z-axis rotation).

#### Parameters:
- `vector_1` (`Vector`): The first vector.
- `vector_2` (`Vector`): The second vector.

#### Returns:
`float`: The angle in degrees between the input vectors projected onto the XY plane (Z-axis rotation).

#### Example usage:
```python
vector1 = Vector(1, 0, 1)
vector2 = Vector(0, 1, 1)
angle = Vector.angle_between_XY(vector1, vector2)
# 45
```


---

#### `angle_between_XZ(vector_1: Vector, vector_2: Vector) -> float`

Computes the angle in degrees between two vectors projected onto the XZ plane (Y-axis rotation).

#### Parameters:
- `vector_1` (`Vector`): The first vector.
- `vector_2` (`Vector`): The second vector.

#### Returns:
`float`: The angle in degrees between the input vectors projected onto the XZ plane (Y-axis rotation).

#### Example usage:
```python
vector1 = Vector(1, 0, 1)
vector2 = Vector(0, 1, 1)
angle = Vector.angle_between_XZ(vector1, vector2)
# 90
```


---

#### `angle_between_YZ(vector_1: Vector, vector_2: Vector) -> float`

Computes the angle in degrees between two vectors projected onto the YZ plane (X-axis rotation).

#### Parameters:
- `vector_1` (`Vector`): The first vector.
- `vector_2` (`Vector`): The second vector.

#### Returns:
`float`: The angle in degrees between the input vectors projected onto the YZ plane (X-axis rotation).

#### Example usage:
```python
vector1 = Vector(1, 1, 0)
vector2 = Vector(1, 0, 1)
angle = Vector.angle_between_YZ(vector1, vector2)
# 90
```


---

#### `angle_radian_between(vector_1: Vector, vector_2: Vector) -> float`

Computes the angle in radians between two vectors.
The angle between two vectors is the angle required to rotate one vector onto the other, measured in radians.

#### Parameters:
- `vector_1` (`Vector`): The first vector.
- `vector_2` (`Vector`): The second vector.

#### Returns:
`float`: The angle in radians between the input vectors.

#### Example usage:
```python
vector1 = Vector(1, 0, 0)
vector2 = Vector(0, 1, 0)
angle = Vector.angle_radian_between(vector1, vector2)
# 1.5707963267948966
```


---

#### `by_line(line_1) -> Vector`

Computes a vector representing the direction of a given line.
This method takes a Line object and returns a Vector representing the direction of the line.

#### Parameters:
- `line_1` (`Line`): The Line object from which to extract the direction.

#### Returns:
`Vector`: A Vector representing the direction of the line.

#### Example usage:
```python
line = Line(start=Point(0, 0, 0), end=Point(1, 1, 1))
direction_vector = Vector.by_line(line)
# Vector(X = 1, Y = 1, Z = 1)
```


---

#### `by_two_points(point_1: Point, point_2: Point) -> Vector`

Computes the vector between two points.

#### Parameters:
- `point_1` (`Point`): The starting point.
- `point_2` (`Point`): The ending point.

#### Returns:
`Vector`: A new Vector object representing the vector between the two points.

#### Example usage:
```python
point1 = Point(1, 2, 3)
point2 = Point(4, 6, 8)
vector = Vector.by_two_points(point1, point2)
# Vector(X = 3, Y = 4, Z = 5)
```


---

#### `cross_product(vector_1: Vector, vector_2: Vector) -> Vector`

Computes the cross product of two vectors.
The cross product of two vectors in three-dimensional space is a vector that is perpendicular to both original vectors. It is used to find a vector that is normal to a plane defined by the input vectors.

#### Parameters:
- `vector_1` (`Vector`): The first vector.
- `vector_2` (`Vector`): The second vector.

#### Returns:
`Vector`: A new Vector object representing the cross product of the input vectors.

#### Example usage:
```python
vector1 = Vector(1, 2, 3)
vector2 = Vector(4, 5, 6)
cross_product = Vector.cross_product(vector1, vector2)
# Vector(X = -3, Y = 6, Z = -3)
```


---

#### `deserialize(data)`

Converts a dictionary representation of a vector into a Vector object.
This method takes a dictionary containing 'x', 'y', and 'z' keys with numeric values and creates a new Vector instance representing the vector described by these values. It's particularly useful for converting serialized vector data back into Vector objects, for instance, when loading vectors from a file or a database.

#### Parameters:
- `data` (dict): A dictionary with keys 'x', 'y', and 'z', corresponding to the components of the vector. Each key's value should be a number (int or float).

#### Returns:
Vector: A new Vector object initialized with the x, y, and z values from the input dictionary.

#### Example usage:
```python
data = {'x': 1.0, 'y': 2.0, 'z': 3.0}
vector = Vector.deserialize(data)
# Vector object with x=1.0, y=2.0, z=3.0
```


---

#### `diff(vector_1: Vector, vector_2: Vector) -> Vector`

Calculates the difference between two Vector objects.
This method returns a new Vector object that is the result of subtracting the components of `vector_2` from `vector_1`.

#### Parameters:
- `vector_1` (`Vector`): The minuend vector.
- `vector_2` (`Vector`): The subtrahend vector.

#### Returns:
`Vector`: A new Vector object resulting from the component-wise subtraction of `vector_2` from `vector_1`.

#### Example usage:
```python
vector1 = Vector(5, 7, 9)
vector2 = Vector(1, 2, 3)
result = Vector.diff(vector1, vector2)
# Vector(X = 4.000, Y = 5.000, Z = 6.000)
```


---

#### `divide(vector_1: Vector, vector_2: Vector) -> Vector`

Divides the components of the first vector by the corresponding components of the second vector.
This method performs component-wise division. If any component of `vector_2` is 0, the result for that component will be undefined.

#### Parameters:
- `vector_1` (`Vector`): The numerator vector.
- `vector_2` (`Vector`): The denominator vector.

#### Returns:
`Vector`: A new Vector object resulting from the component-wise division.

#### Example usage:
```python
vector1 = Vector(10, 20, 30)
vector2 = Vector(2, 4, 5)
result = Vector.divide(vector1, vector2)
# Vector(X = 5.000, Y = 5.000, Z = 6.000)
```


---

#### `dot_product(vector_1: Vector, vector_2: Vector) -> Vector`

Computes the dot product of two vectors.
The dot product of two vectors is a scalar quantity equal to the sum of the products of their corresponding components. It gives insight into the angle between the vectors.

#### Parameters:
- `vector_1` (`Vector`): The first vector.
- `vector_2` (`Vector`): The second vector.

#### Returns:
`float`: The dot product of the input vectors.

#### Example usage:
```python
vector1 = Vector(1, 2, 3)
vector2 = Vector(4, 5, 6)
dot_product = Vector.dot_product(vector1, vector2)
# 32
```


---

#### `from_matrix(vector_list: list) -> Vector`

Creates a Vector object from a list representation.

#### Parameters:
- `vector_list` (list): The list representing the vector.

#### Returns:
`Vector`: A Vector object created from the list representation.

#### Example usage:
```python
vector_list = [1, 2, 3]
vector = Vector.from_matrix(vector_list)
# Vector(X = 1, Y = 2, Z = 3)
```


---

#### `length(vector_1: Vector) -> float`

Computes the length (magnitude) of a vector.
The length of a vector is the Euclidean norm or magnitude of the vector, which is calculated as the square root of the sum of the squares of its components.

#### Parameters:
- `vector_1` (`Vector`): The vector whose length is to be computed.

#### Returns:
`float`: The length of the input vector.

#### Example usage:
```python
vector1 = Vector(1, 2, 3)
length = Vector.length(vector1)
# 3.7416573867739413
```


---

#### `new_length(vector_1: Vector, newlength: float) -> Vector`

Rescales the vector to have the specified length.

#### Parameters:
- `vector_1` (`Vector`): The vector to be rescaled.
- `newlength` (float): The desired length of the vector.

#### Returns:
`Vector`: A new Vector object representing the rescaled vector.

#### Example usage:
```python
vector = Vector(3, 4, 0)
new_vector = Vector.new_length(vector, 5)
# Vector(X = 3.000, Y = 4.000, Z = 0.000)
```


---

#### `normalize(vector_1: Vector) -> Vector`

Returns the normalized form of the input vector.
The normalized form of a vector is a vector with the same direction but with a length (magnitude) of 1.

#### Parameters:
- `vector_1` (`Vector`): The vector to be normalized.

#### Returns:
`Vector`: A new Vector object representing the normalized form of the input vector.

#### Example usage:
```python
vector1 = Vector(3, 0, 4)
normalized_vector = Vector.normalize(vector1)
# Vector(X = 0.600, Y = 0.000, Z = 0.800)
```


---

#### `perpendicular(vector_1: Vector) -> tuple`

Computes two vectors perpendicular to the input vector.

#### Parameters:
- `vector_1` (`Vector`): The input vector.

#### Returns:
`tuple`: A tuple containing two vectors perpendicular to the input vector.

#### Example usage:
```python
vector1 = Vector(1, 2, 3)
perpendicular_vectors = Vector.perpendicular(vector1)
# (Vector(X = 2, Y = -1, Z = 0), Vector(X = -3, Y = 0, Z = 1))
```


---

#### `pitch(vector_1: Vector, angle: float) -> Vector`

Rotates a vector around the X-axis (pitch).
This method rotates the vector around the X-axis (pitch) by the specified angle.

#### Parameters:
- `vector_1` (`Vector`): The vector to be rotated.
- `angle` (float): The angle of rotation in radians.

#### Returns:
`Vector`: A new Vector object representing the rotated vector.

#### Example usage:
```python
vector1 = Vector(1, 2, 3)
rotated_vector = Vector.pitch(vector1, math.pi/2)
# Vector(X = 1.000, Y = -3.000, Z = 2.000)
```


---

#### `product(number: float, vector_1: Vector) -> Vector`

Scales a vector by a scalar value.
This method multiplies each component of the vector by the given scalar value.

#### Parameters:
- `number` (float): The scalar value to scale the vector by.
- `vector_1` (`Vector`): The vector to be scaled.

#### Returns:
`Vector`: A new Vector object representing the scaled vector.

#### Example usage:
```python
vector1 = Vector(1, 2, 3)
scaled_vector = Vector.product(2, vector1)
# Vector(X = 2, Y = 4, Z = 6)
```


---

#### `reverse(vector_1: Vector) -> Vector`

Returns the reverse (negation) of the vector.

#### Parameters:
- `vector_1` (`Vector`): The vector.

#### Returns:
`Vector`: The reverse (negation) of the input vector.

#### Example usage:
```python
vector1 = Vector(1, 2, 3)
reversed_vector = Vector.reverse(vector1)
# Vector(X = -1, Y = -2, Z = -3)
```


---

#### `rotate_XY(vector: Vector, Beta: float) -> Vector`

Rotates the vector in the XY plane by the specified angle.

#### Parameters:
- `vector` (`Vector`): The vector to be rotated.
- `Beta` (float): The angle of rotation in radians.

#### Returns:
`Vector`: A new Vector object representing the rotated vector.

#### Example usage:
```python
vector = Vector(1, 0, 0)
rotated_vector = Vector.rotate_XY(vector, math.pi/2)
# Vector(X = 0, Y = 1, Z = 0)
```


---

#### `scale(vector: Vector, scalefactor: float) -> Vector`

Scales the vector by the specified scale factor.

#### Parameters:
- `vector` (`Vector`): The vector to be scaled.
- `scalefactor` (float): The scale factor.

#### Returns:
`Vector`: A new Vector object representing the scaled vector.

#### Example usage:
```python
vector = Vector(1, 2, 3)
scaled_vector = Vector.scale(vector, 2)
# Vector(X = 2, Y = 4, Z = 6)
```


---

#### `serialize(self) -> dict`

Serializes the Vector object into a dictionary.

#### Returns:
`dict`: A dictionary containing the serialized data of the Vector object.

#### Example usage:
```python
vector = Vector(1, 2, 3)
serialized_data = vector.serialize()
# {'id': None, 'type': None, 'x': 1, 'y': 2, 'z': 3}
```


---

#### `square(vector_1: Vector) -> Vector`


Computes the square of each component of the input vector.

#### Parameters:
- `vector_1` (`Vector`): The input vector.

#### Returns:
`Vector`: A new Vector object representing the square of each component of the input vector.

#### Example usage:
```python
vector = Vector(2, 3, 4)
squared_vector = Vector.square(vector)
# Vector(X = 4, Y = 9, Z = 16)
```


---

#### `subtract(vector_1: Vector, vector_2: Vector) -> Vector`

Subtracts the components of the second vector from the first.
This method is synonymous with `diff` and serves the same purpose, providing an alternative naming convention.

#### Parameters:
- `vector_1` (`Vector`): The vector from which to subtract.
- `vector_2` (`Vector`): The vector to be subtracted.

#### Returns:
`Vector`: The result of the component-wise subtraction.

#### Example usage:
```python
vector1 = Vector(10, 20, 30)
vector2 = Vector(1, 2, 3)
result = Vector.subtract(vector1, vector2)
# Vector(X = 9.000, Y = 18.000, Z = 27.000)
```


---

#### `sum(vector_1: Vector, vector_2: Vector) -> Vector`

Adds two vectors element-wise.        

#### Parameters:
- `vector_1` (Vector): First vector.
- `vector_2` (Vector): Second vector.

Returns:
`Vector`: Sum of the two input vectors.

#### Example usage:

```python
vector_1 = Vector(19, 18, 17)
vector_2 = Vector(8, 17, 1)
output = Vector.sum(vector_1, vector_2)
# Vector(X = 27.000, Y = 35.000, Z = 18.000)
```


---

#### `sum3(vector_1: Vector, vector_2: Vector, vector_3: Vector) -> Vector`

Calculates the sum of three Vector objects.
This method returns a new Vector object whose components are the sum of the corresponding components of the three input vectors.

#### Parameters:
- `vector_1`, `vector_2`, `vector_3` (`Vector`): The vectors to be summed.

#### Returns:
`Vector`: A new Vector object resulting from the component-wise sum of the input vectors.

#### Example usage:
```python
vector1 = Vector(1, 2, 3)
vector2 = Vector(4, 5, 6)
Vector = Vector(-1, -2, -3)
result = Vector.sum3(vector1, vector2, Vector)
# Vector(X = 4.000, Y = 5.000, Z = 6.000)
```


---

#### `to_line(vector_1: Vector, vector_2: Vector) -> Vector`

Creates a Line object from two vectors.

#### Parameters:
- `vector_1` (`Vector`): The start vector of the line.
- `vector_2` (`Vector`): The end vector of the line.

#### Returns:
`Line`: A Line object connecting the two vectors.

#### Example usage:
```python
vector1 = Vector(10, 20, 30)
vector2 = Vector(2, 4, 5)
line = Vector.to_line(vector1, vector2)
# Line(start=Point(X = 10.000, Y = 20.000, Z = 30.000), end=Point(X = 2.000, Y = 4.000, Z = 5.000))
```


---

#### `to_matrix(vector: Vector) -> list`

Converts the vector to a list representation.

#### Parameters:
- `vector` (`Vector`): The vector to be converted.

#### Returns:
`list`: A list representation of the vector.

#### Example usage:
```python
vector = Vector(1, 2, 3)
vector_list = Vector.to_matrix(vector)
# [1, 2, 3]
```


---

#### `to_point(vector_1: Vector) -> Vector`

Converts the vector to a Point object.

#### Parameters:
- `vector_1` (`Vector`): The vector to be converted to a Point object.

#### Returns:
`Point`: A Point object with coordinates same as the vector.

#### Example usage:
```python
vector1 = Vector(10, 20, 30)
point = Vector.to_point(vector1)
# Point(X = 10.000, Y = 20.000, Z = 30.000)
```


---

#### `value(vector_1: Vector) -> tuple`

Returns the rounded values of the vector's components.

#### Parameters:
- `vector_1` (`Vector`): The vector.

#### Returns:
`tuple`: A tuple containing the rounded values of the vector's components.

#### Example usage:
```python
vector1 = Vector(1.123456, 2.345678, 3.987654)
rounded_values = Vector.value(vector1)
# (1.1235, 2.3457, 3.9877)
```


---

