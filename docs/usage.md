# BUILDING.PY EXAMPLES
### TODO:
- Add base of classes.
- Text1 = Text(text="Hello world!", font_family="arial", bounding_box=False, xyz=Point(20,10,20), rotation=0)
- Build scale abstract class

<br><br>

#### Vector2:  
> _`Input: XY=(number/float)`_
<br>

``` python
vctr2 = Vector2(0, 100) # returns 2d-vector
```
<br>

#### Point:
##### link_point
> _`Input: XYZ=(number/float)`_
<br>

``` python
Point(0, 100, 20) # returns Point

Point1 = Point(0, 0, 0)
Point2 = Point(0, 1000, 0)
Point3 = Point(1000, 1000, 0)
Point4 = Point(1000, 0, 0)
```
<br>

#### Point.difference:
> _`Input: Point, Point`_
<br>

``` python
Point.difference(Point1, Point2) # calculate the difference between two 3D points and return a Vector
```
<br>

#### Vector.sum:  
> _`Input: Vector, Vector`_
<br>

#### Point.translate:
> _`Input: Point, Vector`_
<br>

``` python
Point.translate(Point1, v1) # translates a 3D point by a given Vector and returns a new Point
```
<br>

#### Point.point_2D_to_3D:
> _`Input: Point2D`_
<br>

``` python
Point.point_2D_to_3D(p2d) # Transforms a 2D point into a 3D point
```
<br>

#### Point.rotate_XY:
> _`Input: Point, Degrees, Number of steps`_
<br>

``` python
Point.rotate_XY(p1, 30, 5) # rotate (30 degrees) and translate (5 steps) a 3D point around the Z axis
```
<br>

#### transform_point:
> _`Input: Point, Coordinate system, Point, Vector`_
<br>

``` python
transformed_point = transform_point(p1, CSGlobal, p2, v1)
```
<br>

#### Vector.sum:  
> _`Input: Vector, Vector`_
<br>

``` python
Vector(0, 1, 0) # returns 3d-vector
v1 = Vector(0, 1, 0) # example vector1
v2 = Vector(1, 0, 0) # example vector2
v10 = Vector(0, 1000, 0) # example vector10
v20 = Vector(1000, 0, 0) # example vector20

Vector.sum(v1, v2) # returns sum of 2 vectors
```
<br>

#### Vector.cross_product:  
> _`Input: Vector, Vector`_
<br>

``` python
Vector.cross_product(v1, v2) # returns vector perpendicular on the two vectors
```
<br>

#### Vector.dot_product:  
> _`Input: Vector, Vector`_
<br>

``` python
Vector.dot_product(v1, v2) # inner product, if zero, then vectors are 
```
<br>

#### Vector.product:  
> _`Input: (number/float), Vector`_
<br>

``` python
Vector.product(5, v1) # Same as scale
```
<br>

#### Vector.length:  
> _`Input: Vector`_
<br>

``` python
Vector.length(v1) # returns the length of a vector
```
<br>

#### Vector.pitch:  
> _`Input: Vector, Degrees (1 to 360)`_
<br>

``` python
Vector.pitch(v1, 45) # ??
```
<br>

#### Vector.angle_between:  
> _`Input: Vector, Vector`_
<br>

``` python
Vector.angle_between(v1, v2) # returns the angle between two vectors
```
<br>

#### Vector.reverse:  
> _`Input: Vector`_
<br>

``` python
Vector.reverse(v1) # returns vector in the opposite direction
```
<br>

#### Vector.perpendicular:  
> _`Input: Vector`_
<br>

``` python
Vector.perpendicular(v1) # Vector local X and local Y perpendicular to given vector and in global Z-direction
```
<br>

#### Vector.normalize:  
> _`Input: Vector`_
<br>

``` python
Vector.normalize(v1) # ??
```
<br>

#### Vector.by_two_points:  
> _`Input: Point, Point`_
<br>

``` python
Vector.by_two_points(Point1, Point2) # Subtracts Point1 x,y and z from Point2 x,y and z
```
<br>

#### Vector.to_point:  
> _`Input: Vector`_
<br>

``` python
Vector.to_point(v1) # Translates a Vector to a Point
```
<br>

#### Vector.to_line:  
> _`Input: Vector, Vector`_
<br>

``` python
Vector.to_line(v10, v20) # Returns a Line from point v10, and Point v20
```
<br>

#### Point2D:
> _`Input: XY=(number/float)`_
<br>

``` python
p2d = Point2D(0, 100) # returns Point2D
p2d2 = Point2D(0, 100) # returns Point2D
p2d3 = Point2D(0, 100) # returns Point2D
```
<br>

#### Point2D.translate:
> _`Input: Point2d, Vector`_
<br>

``` python
Point2D.translate(p2d, v1) # A new point is created by translating a Point2D by a Vector
```
<br>

#### Point2D.rotate:
> _`Input: Point2d, Degrees`_
<br>

``` python
Point2D.rotate(p2d, 90) # A new point is created by rotating a Point2D a certain amount of degrees
```
<br>

#### Plane.by_two_vectors_origin:  
> _`Input: v1, v2, Point`_
<br>

``` python
origin = Point(0, 0, 0)

plane_ex = Plane.by_two_vectors_origin(v1, v2, origin)
# returns Plane
```
<br>

#### Line:
>_<code>Input usage: Line(start=<a href="#link_point">Point</a>, end=<a href="#link_point">Point</a>)</code>_
<br>
``` python
Line1 = Line(start=Point(0, 0, 0), end=Point(0, 500, 0))
Line2 = Line(start=Point(0, 500, 0), end=Point(-200, 500, 0))
Line3 = Line(start=Point(-200, 500, 0), end=Point(100, 1000, 0))
Line4 = Line(start=Point(100, 1000, 0), end=Point(400, 500, 0))
Line5 = Line(start=Point(400, 500, 0), end=Point(200, 500, 0))
Line6 = Line(start=Point(200, 500, 0), end=Point(200, 0, 0))
Line7 = Line(start=Point(200, 0, 0), end=Point(0, 0, 0))
```
<br>

#### Line.length:  
> _`Input: Line`_
<br>

``` python
Line.length(Line1) # Calculate the length of a line
```
<br>

#### Line2D:  
> _`Input: XY=(number/float)`_
<br>

``` python
l2d = Line2D(0, 100)
```
<br>

#### Line2D.length:  
> _`Input: Line2D`_
<br>

``` python
Line2D.length(l2d) # Calculate the length of a 2D Line
```
<br>

#### PolyCurve2D.by_joined_curves:  
> _`Input: Line2D`_
<br>

``` python
ply2D = PolyCurve2D.by_joined_curves([
    Line2D(
        Point2D(0,0),
        Point2D(100,0)),
    Line2D(
        Point2D(100, 0),
        Point2D(100, 100)),
    Line2D(
        Point2D(100,100),
        Point2D(0,0))]
    )
```
<br>

#### PolyCurve2D.points:  
> _`Input: polyCurve2D`_
<br>

``` python
PolyCurve2D.points(ply2D) # return all the points within the PolyCurve2D
```
<br>

#### PolyCurve2D.translate:  
> _`Input: polyCurve2D, Vector2`_
<br>

``` python
PolyCurve2D.translate(ply2D, vctr2) # translates each curve within the PolyCurve2D by a Vector2D and returns a new PolyCurve2D
```
<br>

#### PolyCurve2D.rotate:  
> _`Input: polyCurve2D, Degrees`_
<br>

``` python
PolyCurve2D.rotate(ply2D, 90) # rotates each curve within the PolyCurve2D by a given rotation angle and returns a new PolyCurve2D
```
<br>

#### PolyCurve2D.polygon:  
> _`Input: polyCurve2D`_
<br>

``` python
PolyCurve2D.polygon(ply2D) # returns a polygon by collecting start points of curves within the PolyCurve2D
```
<br>

#### PolyCurve.by_joined_curves:  
> _`Input: Line`_
<br>

``` python
PC1 = PolyCurve.by_joined_curves([Line1, Line2, Line3]) # Create a PolyCurve object by joining a list of curves and collecting their starting points
```
<br>

#### PolyCurve.by_points:  

>_<code>Input usage: Polycurve.by_points(list[<a href="#link_point">Point</a>])</code>_


``` python
PolyCurve.by_points([Point1, Point2, Point3, Point4, Point1]) # Creating a PolyCurve object from a list of Points
```
<br>

#### PolyCurve.by_polycurve_2D:  
> _`Input: PolyCurve2D`_
<br>

``` python
PolyCurve.by_polycurve_2D(ply2D) # Creating a PolyCurve object from a 2D polygon curve defined by four points
```
<br>

#### PolyCurve.translate:  
> _`Input: Vector`_
<br>

``` python
PolyCurve.translate(v1) # Poly-curve translate moves the curve by v1 vector
```
<br>

#### PolyCurve.rotate:  
> _`Input: Polycurve, Angle in degrees, Displacement in z-direction`_
<br>

``` python
PolyCurve.rotate(PC1, 90, 10) # Poly-curve translate moves the curve by v1 vector
```
<br>

#### Polygon:  
> _`Input: list[Line]`_
<br>

``` python
# moet nog naar worden gekeken

flat_curves = [Line(Point(0, 0, 0), Point(0, 100, 0)), Line(Point(0, 100, 0), Point(100, 100, 0))] # Create a List of lines
plygn1 = Polygon(flat_curves) # Create a Polygon using a list of Lines
```
<br>

#### Arc2D:  
> _`Input: Point2D`_
<br>

``` python
testarc = Arc2D(p2d, p2d2, p2d3) # Creates a 2d Arc
```
<br>

#### Arc2D.points:  
> _`Input: Point2D`_
<br>

``` python
Arc2D.points(testarc) # returns point on the curve
```
<br>

#### Arc:  
> _`Input: Point`_
<br>

``` python
arc1 = Arc(Point1, Point2, Point3) # Create a new Arc
```
<br>

#### Arc.distance:  
> _`Input: Arc, Point, Point`_
<br>

``` python
Arc.distance(arc1, Point1, Point2) # Calculates the distance between two points
```
<br>

#### Arc.radius:  
> _`Input: Arc`_
<br>

``` python
Arc.radius(arc1) # Calculating radius of arc using the distance function
```
<br>

#### Arc.length:  
> _`Input: Arc`_
<br>

``` python
Arc.length(arc1) # Calculate length of Arc
```
<br>

#### Arc.ByThreePoints:  
> _`Input: Arc`_
<br>

``` python
Arc.ByThreePoints(Point1, Point2, Point3) # Creates an Arc from 3 points, with optional plane and properties
```
<br>

#### Circle:  
> _`Input: radius, plane, length`_
<br>

``` python
radius = 5
length = 2 * radius * math.pi

Circle(radius, plane_ex, length) # Create a circle
```
<br>

#### Ellipse:  
> _`Input: radius, radius, plane`_
<br>

``` python
Ellipse(3, 5, plane_ex) # Create an ellipse
```
<br>

#### CoordinateSystem:  
> _`Input: Point, X_axis, Y_Axis, Z_Axis`_
<br>

``` python
X_axis = Vector(1, 0, 0)
Y_Axis = Vector(0, 1, 0)
Z_Axis = Vector(0, 0, 0)

CoordinateSystem(Point(0, 0, 0), X_axis, Y_Axis, Z_Axis) # returns CoordinateSystem
```
<br>

#### Boundingbox:  
> _`Input: POINTS=list[Points]`_
<br>

``` python
BoundingBox2d(points=[POINTS]).perimeter() # returns 2d-perimeter
BoundingBox3d(points=[POINTS]).perimeter() # returns 3d-perimeter
```

#### Extrusion.by_polycurve_height_vector:  
> _`Input: PolyCurve, Height, Coördinate system, Point, Vector`_
<br>

``` python
Extrusion.by_polycurve_height_vector(PC1, 20, 30, p1, v1) # Extrude a 2D profile to a 3D mesh
```

#### Extrusion.by_polycurve_height:  
> _`Input: PolyCurve, Height, Dzloc`_
<br>

``` python
Extrusion.by_polycurve_height(PC1, 20, 40) # Extrude a 2D profile to a 3D mesh
```

#### Grid.by_startpoint_endpoint:  
> _`Input: Line, Name`_
<br>

``` python
GridA = Grid.by_startpoint_endpoint(Line(start=Point(-1000, 0, 0), end=Point(10000, 0, 0)), "A") # Create panel by polycurve
```

#### get_grid_distances:  
> _`Input: Grid`_
<br>

``` python
get_grid_distances(GridA) # ??
```

#### GridSystem:  
> _`Input: spacingX, labelsX, spacingY, labelsY, gridExtension`_
<br>

``` python
spacingX = "4x5400 4000 4000"
labelsX = "A B C D"
spacingY = "4x4000 5400"
labelsY = "1 2 3"
gridExtension = 1000

grdsystem = GridSystem(spacingX, labelsX, spacingY, labelsY, gridExtension)
```

#### Frame.by_startpoint_endpoint_profile:  
> _`Input: start: Point, end: Point, profile_name: str, name: str, material`_
<br>

``` python
Frame.by_startpoint_endpoint_profile(Point(0, 0, 0), Point(0, 1000, 0), "HE100A", "test", "steel")
```

#### Frame.by_startpoint_endpoint_profile_shapevector:  
> _`Input: start: Point, end: Point, profile_name: str, name: str, Vector2, rotation: float, material`_
<br>

``` python
Frame.by_startpoint_endpoint_profile_shapevector(p1, p2, "HE100A", "Frame 4", vctr2, 20, "steel")
```

#### Frame.by_startpoint_endpoint_profile_shapevector:  
> _`Input: start: Point, end: Point, profile_name: str, name: str, XJustifiction: str, YJustifiction: str, rotation: float, material`_
<br>

``` python
Frame.by_startpoint_endpoint_profile_justifiction(p1, p2, "HE100A", "Test", 5, 4, 90, "steel")
```

#### Frame.by_startpoint_endpoint:  
> _`Input: start: Point, end: Point, polycurve: PolyCurve2D, name: str, rotation: float, material`_
<br>

``` python
Frame.by_startpoint_endpoint(p1, p2, PC1, "test", 90, "Steel")
```

#### Panel.by_polycurve_thickness:  
> _`Input: PolyCurve, thickness: float, offset: float, name: str, colorrgbint`_
<br>

``` python
Panel.by_polycurve_thickness(PC4, 100, 0, "test1", rgb_to_int([192, 192, 192]))
```

#### Panel.by_baseline_height:  
> _`Input: baseline: Line, height: float, thickness: float, name: str, colorrgbint`_
<br>

``` python
Panel.by_baseline_height(Line(start=Point(0, -1000, 0),
                            end=Point(3000, -1000, 0)), 2500, 150, "wand", rgb_to_int([192, 192, 192]))
```

#### Text:  
> _`Input: text: str, font_family: str, bounding_box: bool, xyz: Tuple[float, float, float], rotation: float`_
<br>

``` python
Text(text="PyBuildingSystem1", font_family="arial", bounding_box=False, xyz=[0, 0, 0], rotation=90) # all parms (with optional)

Text(text="PyBuildingSystem2", font_family="arial") # without optional parms
```

#### BoundingBox2d:  
> _`Input: points=list[Point]`_
<br>

``` python
BoundingBox2d(points=[Point1, Point2, Point3 ,Point4]).perimeter() # Boundingbox
```

#### BoundingBox3d:  
> _`Input: points=list[Point]`_
<br>

``` python
BoundingBox3d(points=[Point1, Point2, Point3 ,Point4]).perimeter() # Boundingbox
```

#### Intersect.getIntersect:  
> _`Input: line1:Line, line2:Line`_
<br>

``` python
Intersect.getIntersect(Line(start=Point(0, -1000, 0),
                            end=Point(3000, -1000, 0)),
                        Line(start=Point(0, -1000, 0),
                            end=Point(3000, -1000, 0))) # Finds the intersection point between two given lines?
```

#### Intersect.onSegment:  
> _`Input: ?, ?, ?`_
<br>

``` python
Intersect.onSegment("?, ?, ?") # ?
```

#### Intersect.orientation:  
> _`Input: ?, ?, ?`_
<br>

``` python
Intersect.orientation("?, ?, ?") # Checks the orientation of three 2D points?
```