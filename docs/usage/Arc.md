# Class `Arc`
No documentation available.

## Constructor

### `__init__(self, startPoint: Point, midPoint: Point, endPoint: Point) -> Arc`
Initializes an Arc object with start, mid, and end points.
        This constructor calculates and assigns the arc's origin, plane, radius, start angle, end angle, angle in radians, area, length, units, and coordinate system based on the input points.

        - `startPoint` (Point): The starting point of the arc.
        - `midPoint` (Point): The mid point of the arc which defines its curvature.
        - `endPoint` (Point): The ending point of the arc.
        

---


## Methods

- `__str__(self) -> str`: Generates a string representation of the Arc object.

        

- `angle_radian(self) -> float`: Calculates and returns the total angle of the arc in radians.
        The angle is determined based on the vectors defined by the start, mid, and end points with respect to the arc's origin.

        

- `coordinatesystem_arc(self) -> CoordinateSystem`: Calculates and returns the coordinate system of the arc.
        The coordinate system is defined by the origin of the arc and the normalized vectors along the local X, Y, and Z axes.

        

- `distance(self, point_1: Point, point_2: Point) -> float`: Calculates the Euclidean distance between two points in 3D space.

        

- `length(self) -> float`: Calculates and returns the length of the arc.
        The length is calculated using the geometric properties of the arc defined by its start, mid, and end points.

        

- `origin_arc(self) -> Point`: Calculates and returns the origin of the arc.
        The origin is calculated based on the geometric properties of the arc defined by its start, mid, and end points.

        

- `points_at_parameter(arc: Arc, count: int) -> list`: Generates a list of points along the arc at specified intervals.
        This method divides the arc into segments based on the `count` parameter and calculates points at these intervals along the arc.

        

- `radius_arc(self) -> float`: Calculates and returns the radius of the arc.
        The radius is computed based on the distances between the start, mid, and end points of the arc.

        

- `segmented_arc(arc: Arc, count: int) -> list`: Divides the arc into segments and returns a list of line segments.
        This method uses the `points_at_parameter` method to generate points along the arc at specified intervals and then creates line segments between these consecutive points.

        


## Documentation

#### `__str__(self) -> str`

Generates a string representation of the Arc object.

#### Returns:
`str`: A string that represents the Arc object.

#### Example usage:
```python
arc = Arc(startPoint, midPoint, endPoint)
print(arc)
# Output: Arc()
```


---

#### `angle_radian(self) -> float`

Calculates and returns the total angle of the arc in radians.
The angle is determined based on the vectors defined by the start, mid, and end points with respect to the arc's origin.

#### Returns:
`float`: The total angle of the arc in radians.

#### Example usage:
```python
angle = arc.angle_radian()
# angle will be the total angle of the arc in radians
```


---

#### `coordinatesystem_arc(self) -> CoordinateSystem`

Calculates and returns the coordinate system of the arc.
The coordinate system is defined by the origin of the arc and the normalized vectors along the local X, Y, and Z axes.

#### Returns:
`CoordinateSystem`: The coordinate system of the arc.

#### Example usage:
```python
coordinatesystem = arc.coordinatesystem_arc()
# coordinatesystem will be an instance of CoordinateSystem representing the arc's local coordinate system
```


---

#### `distance(self, point_1: Point, point_2: Point) -> float`

Calculates the Euclidean distance between two points in 3D space.

#### Parameters:
- `point_1` (Point): The first point.
- `point_2` (Point): The second point.

#### Returns:
`float`: The Euclidean distance between `point_1` and `point_2`.

#### Example usage:
```python
point1 = Point(1, 2, 3)
point2 = Point(4, 5, 6)
distance = arc.distance(point1, point2)
# distance will be the Euclidean distance between point1 and point2
```


---

#### `length(self) -> float`

Calculates and returns the length of the arc.
The length is calculated using the geometric properties of the arc defined by its start, mid, and end points.

#### Returns:
`float`: The length of the arc.

#### Example usage:
```python
length = arc.length()
# length will be the calculated length of the arc
```


---

#### `origin_arc(self) -> Point`

Calculates and returns the origin of the arc.
The origin is calculated based on the geometric properties of the arc defined by its start, mid, and end points.

#### Returns:
`Point`: The calculated origin point of the arc.

#### Example usage:
```python
origin = arc.origin_arc()
# origin will be the calculated origin point of the arc
```


---

#### `points_at_parameter(arc: Arc, count: int) -> list`

Generates a list of points along the arc at specified intervals.
This method divides the arc into segments based on the `count` parameter and calculates points at these intervals along the arc.

#### Parameters:
- `arc` (Arc): The arc object.
- `count` (int): The number of points to generate along the arc.

#### Returns:
`list`: A list of points (`Point` objects) along the arc.

#### Example usage:
```python
arc = Arc(startPoint, midPoint, endPoint)
points = Arc.points_at_parameter(arc, 5)
# points will be a list of 5 points along the arc
```


---

#### `radius_arc(self) -> float`

Calculates and returns the radius of the arc.
The radius is computed based on the distances between the start, mid, and end points of the arc.

#### Returns:
`float`: The radius of the arc.

#### Example usage:
```python
radius = arc.radius_arc()
# radius will be the calculated radius of the arc
```


---

#### `segmented_arc(arc: Arc, count: int) -> list`

Divides the arc into segments and returns a list of line segments.
This method uses the `points_at_parameter` method to generate points along the arc at specified intervals and then creates line segments between these consecutive points.

#### Parameters:
- `arc` (Arc): The arc object.
- `count` (int): The number of segments (and thus the number of points - 1) to create.

#### Returns:
`list`: A list of line segments (`Line` objects) representing the divided arc.

#### Example usage:
```python
arc = Arc(startPoint, midPoint, endPoint)
segments = Arc.segmented_arc(arc, 3)
# segments will be a list of 2 lines dividing the arc into 3 segments
```


---

