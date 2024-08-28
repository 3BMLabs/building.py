# Class `Line`
No documentation available.

## Constructor

### `__init__(self, start: Point, end: Point) -> Line`
Initializes a Line object with the specified start and end points.

        - `start` (Point): The starting point of the line segment.
        - `end` (Point): The ending point of the line segment.
        

---


## Methods

- `__str__(self) -> str`: Returns a string representation of the Line object.

        

- `by_startpoint_direction_length(start: Point, direction: Vector, length: float) -> Line`: Creates a line segment starting from a given point in the direction of a given vector with a specified length.

        

- `deserialize(data: dict)`: Deserializes the data dictionary into a Line object.

        

- `length(self) -> float`: Computes the length of the Line object.

        

- `mid_point(self) -> Point`: Computes the midpoint of the Line object.

        

- `offset(line: Line, vector: Vector) -> Line`: Offsets the Line object by a given vector.

        

- `point_at_parameter(self, interval: float = None) -> Point`: Computes the point on the Line object at a specified parameter value.

        

- `serialize(self) -> dict`: Serializes the Line object into a dictionary.

        

- `split(self, points: Union[Point, list[Point]]) -> list[Line]`: Splits the Line object at the specified point(s).

        

- `transform(line: Line, cs_new: CoordinateSystem) -> Line`: Transforms the Line object to a new coordinate system.

        

- `translate(self, direction: Vector) -> Line`: Translates the Line object by a given direction vector.

        

- `translate_2(line: Line, direction: Vector) -> Line`: Translates the specified Line object by a given direction vector.

        


## Documentation

#### `__str__(self) -> str`

Returns a string representation of the Line object.

#### Returns:
`str`: A string representation of the Line object.

#### Example usage:
```python

```          


---

#### `by_startpoint_direction_length(start: Point, direction: Vector, length: float) -> Line`

Creates a line segment starting from a given point in the direction of a given vector with a specified length.

#### Parameters:
- `start` (Point): The starting point of the line segment.
- `direction` (Vector): The direction vector of the line segment.
- `length` (float): The length of the line segment.

#### Returns:
`Line`: A new Line object representing the line segment.

#### Example usage:
```python

```          


---

#### `deserialize(data: dict)`

Deserializes the data dictionary into a Line object.

#### Parameters:
- `data` (dict): The dictionary containing the serialized data of the Line object.

#### Returns:
`Line`: A Line object reconstructed from the serialized data.

#### Example usage:
```python

```          


---

#### `length(self) -> float`

Computes the length of the Line object.

#### Returns:
`float`: The length of the Line object.

#### Example usage:
```python

```          


---

#### `mid_point(self) -> Point`

Computes the midpoint of the Line object.

#### Returns:
`Point`: The midpoint of the Line object.

#### Example usage:
```python

```          


---

#### `offset(line: Line, vector: Vector) -> Line`

Offsets the Line object by a given vector.

#### Parameters:
- `line` (Line): The Line object to be offset.
- `vector` (Vector): The vector by which the Line object will be offset.

#### Returns:
`Line`: The offset Line object.

#### Example usage:
```python

```          


---

#### `point_at_parameter(self, interval: float = None) -> Point`

Computes the point on the Line object at a specified parameter value.

#### Parameters:
- `interval` (float): The parameter value determining the point on the line. Default is None, which corresponds to the midpoint.

#### Returns:
`Point`: The point on the Line object corresponding to the specified parameter value.

#### Example usage:
```python

```          


---

#### `serialize(self) -> dict`

Serializes the Line object into a dictionary.

#### Returns:
`dict`: A dictionary containing the serialized data of the Line object.

#### Example usage:
```python

```         


---

#### `split(self, points: Union[Point, list[Point]]) -> list[Line]`

Splits the Line object at the specified point(s).

#### Parameters:
- `points` (Point or List[Point]): The point(s) at which the Line object will be split.

#### Returns:
`List[Line]`: A list of Line objects resulting from the split operation.

#### Example usage:
```python

```          


---

#### `transform(line: Line, cs_new: CoordinateSystem) -> Line`

Transforms the Line object to a new coordinate system.

#### Parameters:
- `line` (Line): The Line object to be transformed.
- `cs_new` (CoordinateSystem): The new coordinate system to which the Line object will be transformed.

#### Returns:
`Line`: The transformed Line object.

#### Example usage:
```python

```          


---

#### `translate(self, direction: Vector) -> Line`

Translates the Line object by a given direction vector.

#### Parameters:
- `direction` (Vector): The direction vector by which the line segment will be translated.

#### Returns:
`Line`: The translated Line object.

#### Example usage:
```python

```          


---

#### `translate_2(line: Line, direction: Vector) -> Line`

Translates the specified Line object by a given direction vector.

#### Parameters:
- `line` (Line): The Line object to be translated.
- `direction` (Vector): The direction vector by which the line segment will be translated.

#### Returns:
`Line`: The translated Line object.

#### Example usage:
```python

```          


---

