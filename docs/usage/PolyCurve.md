# Class `PolyCurve`
No documentation available.

## Constructor

### `__init__(self)`
Initializes a PolyCurve object.
        
        - `id` (int): The unique identifier of the arc.
        - `type` (str): The type of the arc.
        - `start` (Point): The start point of the arc.
        - `mid` (Point): The mid point of the arc.
        - `end` (Point): The end point of the arc.
        - `origin` (Point): The origin point of the arc.
        - `plane` (Plane): The plane containing the arc.
        - `radius` (float): The radius of the arc.
        - `startAngle` (float): The start angle of the arc in radians.
        - `endAngle` (float): The end angle of the arc in radians.
        - `angle_radian` (float): The total angle of the arc in radians.
        - `area` (float): The area of the arc.
        - `length` (float): The length of the arc.
        - `units` (str): The units used for measurement.
        - `coordinatesystem` (CoordinateSystem): The coordinate system of the arc.

        

---


## Methods

- `__str__(self) -> str`: Returns a string representation of the PolyCurve.

        

- `area(self) -> float`: Calculates the area enclosed by the PolyCurve using the shoelace formula.

        

- `by_polycurve_2D(PolyCurve2D) -> PolyCurve`: Creates a 3D PolyCurve from a 2D PolyCurve.

        

- `centroid(self) -> Point`: Calculates the centroid of the PolyCurve.

        

- `close(self) -> bool`: Closes the PolyCurve by connecting the last point to the first point.

        

- `copy_translate(pc: PolyCurve, vector_3d: Vector3) -> PolyCurve`: Creates a copy of a PolyCurve and translates it by a 3D vector.

        

- `deserialize(data)`: Deserializes the PolyCurve object.

        

- `get_width(self) -> float`: Calculates the width of the PolyCurve.

        

- `length(self) -> float`: Calculates the total length of the PolyCurve.

        

- `multi_split(self, lines: Line) -> list[PolyCurve]`: Splits the PolyCurve by multiple lines.
        This method splits the PolyCurve by multiple lines and adds the resulting PolyCurves to the project.

        

- `rotate(self, angle: float, dz: float) -> PolyCurve`: Rotates the PolyCurve by a given angle around the Z-axis and displaces it in the Z-direction.

        

- `scale(self, scale_factor: float) -> PolyCurve`: Scales the PolyCurve object by the given factor.

        

- `segment(self, count: int) -> PolyCurve`: Segments the PolyCurve into straight lines.

        

- `serialize(self) -> dict`: Serializes the PolyCurve object.

        

- `split(self, line: Line, returnlines=None) -> list[PolyCurve]`: Splits the PolyCurve by a line and returns the split parts.

        

- `to_polycurve_2D(self)`: Converts the PolyCurve to a PolyCurve2D.

        

- `transform_from_origin(polycurve: PolyCurve, startpoint: Point, directionvector: Vector3) -> PolyCurve`: Transforms a PolyCurve from a given origin point and direction vector.

        

- `translate(self, vector_3d: Vector3) -> PolyCurve`: Translates the PolyCurve by a 3D vector.

        


## Documentation

#### `__str__(self) -> str`

Returns a string representation of the PolyCurve.

#### Returns:
`str`: The string representation of the PolyCurve.

#### Example usage:
```python

```        


---

#### `area(self) -> float`

Calculates the area enclosed by the PolyCurve using the shoelace formula.

#### Returns:
`float`: The area enclosed by the PolyCurve.

#### Example usage:
```python

```        


---

#### `by_polycurve_2D(PolyCurve2D) -> PolyCurve`

Creates a 3D PolyCurve from a 2D PolyCurve.

#### Parameters:
- `PolyCurve2D`: The 2D PolyCurve object.

#### Returns:
`PolyCurve`: The created 3D PolyCurve object.

#### Example usage:
```python

```        


---

#### `centroid(self) -> Point`

Calculates the centroid of the PolyCurve.

#### Returns:
`Point`: The centroid point of the PolyCurve.

#### Example usage:
```python

```        


---

#### `close(self) -> bool`

Closes the PolyCurve by connecting the last point to the first point.

#### Returns:
`bool`: True if the PolyCurve is successfully closed, False otherwise.

#### Example usage:
```python

```        


---

#### `copy_translate(pc: PolyCurve, vector_3d: Vector3) -> PolyCurve`

Creates a copy of a PolyCurve and translates it by a 3D vector.

#### Parameters:
- `pc` (PolyCurve): The PolyCurve to copy and translate.
- `vector_3d` (Vector3): The 3D vector by which to translate the PolyCurve.

#### Returns:
`PolyCurve`: The translated copy of the PolyCurve.

#### Example usage:
```python

```        


---

#### `deserialize(data)`

Deserializes the PolyCurve object.

#### Parameters:
- `data` (dict): Serialized data of the PolyCurve object.

#### Returns:
`PolyCurve`: Deserialized PolyCurve object.

#### Example usage:
```python

```        


---

#### `get_width(self) -> float`

Calculates the width of the PolyCurve.

#### Returns:
`float`: The width of the PolyCurve.

#### Example usage:
```python

```        


---

#### `length(self) -> float`

Calculates the total length of the PolyCurve.

#### Returns:
`float`: The total length of the PolyCurve.

#### Example usage:
```python

```        


---

#### `multi_split(self, lines: Line) -> list[PolyCurve]`

Splits the PolyCurve by multiple lines.
This method splits the PolyCurve by multiple lines and adds the resulting PolyCurves to the project.

#### Parameters:
- `lines` (List[Line]): The list of lines to split the PolyCurve.

#### Returns:
`List[PolyCurve]`: The list of split PolyCurves.

#### Example usage:
```python

```        


---

#### `rotate(self, angle: float, dz: float) -> PolyCurve`

Rotates the PolyCurve by a given angle around the Z-axis and displaces it in the Z-direction.

#### Parameters:
- `angle` (float): The angle of rotation in degrees.
- `dz` (float): The displacement in the Z-direction.

#### Returns:
`PolyCurve`: The rotated and displaced PolyCurve.

#### Example usage:
```python

```        


---

#### `scale(self, scale_factor: float) -> PolyCurve`

Scales the PolyCurve object by the given factor.

#### Parameters:
- `scale_factor`: The scaling factor.

#### Returns:
`PolyCurve`: Scaled PolyCurve object.

#### Example usage:
```python

```        


---

#### `segment(self, count: int) -> PolyCurve`

Segments the PolyCurve into straight lines.

#### Parameters:
- `count` (int): The number of segments.

#### Returns:
`PolyCurve`: The segmented PolyCurve object.

#### Example usage:
```python

```        


---

#### `serialize(self) -> dict`

Serializes the PolyCurve object.

#### Returns:
`dict`: Serialized data of the PolyCurve object.

#### Example usage:
```python

```        


---

#### `split(self, line: Line, returnlines=None) -> list[PolyCurve]`

Splits the PolyCurve by a line and returns the split parts.

#### Parameters:
- `line` (Line): The line to split the PolyCurve.
- `returnlines` (bool, optional): Whether to return the split PolyCurves as objects or add them to the project. Defaults to None.

#### Returns:
`list[PolyCurve]`: If `returnlines` is True, returns a list of split PolyCurves. Otherwise, None.

#### Example usage:
```python

```        


---

#### `to_polycurve_2D(self)`

Converts the PolyCurve to a PolyCurve2D.

#### Returns:
`PolyCurve2D`: The converted PolyCurve2D.

#### Example usage:
```python

```        


---

#### `transform_from_origin(polycurve: PolyCurve, startpoint: Point, directionvector: Vector3) -> PolyCurve`

Transforms a PolyCurve from a given origin point and direction vector.

#### Parameters:
- `polycurve` (PolyCurve): The PolyCurve to transform.
- `startpoint` (Point): The origin point for the transformation.
- `directionvector` (Vector3): The direction vector for the transformation.

#### Returns:
`PolyCurve`: The transformed PolyCurve.

#### Example usage:
```python

```        


---

#### `translate(self, vector_3d: Vector3) -> PolyCurve`

Translates the PolyCurve by a 3D vector.

#### Parameters:
- `vector_3d` (Vector3): The 3D vector by which to translate the PolyCurve.

#### Returns:
`PolyCurve`: The translated PolyCurve.

#### Example usage:
```python

```        


---

