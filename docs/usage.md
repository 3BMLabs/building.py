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

#### Vector3.sum:  
> _`Input: Vector3, Vector3`_
<br>

``` python
Vector3(0, 1, 0) # returns 3d-vector
v1 = Vector3(0, 1, 0) # example vector1
v2 = Vector3(1, 0, 0) # example vector2
v10 = Vector3(0, 1000, 0) # example vector10
v20 = Vector3(1000, 0, 0) # example vector20

Vector3.sum(v1, v2) # returns sum of 2 vectors
```
<br>

#### Vector3.crossProduct:  
> _`Input: Vector3, Vector3`_
<br>

``` python
Vector3.crossProduct(v1, v2) # returns vector perpendicular on the two vectors
```
<br>

#### Vector3.dotProduct:  
> _`Input: Vector3, Vector3`_
<br>

``` python
Vector3.dotProduct(v1, v2) # inner product, if zero, then vectors are 
```
<br>

#### Vector3.product:  
> _`Input: (number/float), Vector3`_
<br>

``` python
Vector3.product(5, v1) # Same as scale
```
<br>

#### Vector3.length:  
> _`Input: Vector3`_
<br>

``` python
Vector3.length(v1) # returns the length of a vector
```
<br>

#### Vector3.pitch:  
> _`Input: Vector3, Degrees (1 to 360)`_
<br>

``` python
Vector3.pitch(v1, 45) # ??
```
<br>

#### Vector3.angleBetween:  
> _`Input: Vector3, Vector3`_
<br>

``` python
Vector3.angleBetween(v1, v2) # returns the angle between two vectors
```
<br>

#### Vector3.reverse:  
> _`Input: Vector3`_
<br>

``` python
Vector3.reverse(v1) # returns vector in the opposite direction
```
<br>

#### Vector3.perpendicular:  
> _`Input: Vector3`_
<br>

``` python
Vector3.perpendicular(v1) # Vector local X and local Y perpendicular to given vector and in global Z-direction
```
<br>

#### Vector3.normalise:  
> _`Input: Vector3`_
<br>

``` python
Vector3.normalise(v1) # ??
```
<br>

#### Vector3.byTwoPoints:  
> _`Input: Point, Point`_
<br>

``` python
Vector3.byTwoPoints(Point1, Point2) # Subtracts Point1 x,y and z from Point2 x,y and z
```
<br>

#### Vector3.toPoint:  
> _`Input: Vector3`_
<br>

``` python
Vector3.toPoint(v1) # Translates a Vector to a Point
```
<br>

#### Vector3.toLine:  
> _`Input: Vector3, Vector3`_
<br>

``` python
Vector3.toLine(v10, v20) # Returns a Line from point v10, and Point v20
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
> _`Input: Point2d, Vector3`_
<br>

``` python
Point2D.translate(p2d, v1) # A new point is created by translating a Point2D by a Vector3
```
<br>

#### Point2D.rotate:
> _`Input: Point2d, Degrees`_
<br>

``` python
Point2D.rotate(p2d, 90) # A new point is created by rotating a Point2D a certain amount of degrees
```
<br>

#### Plane.byTwoVectorsOrigin:  
> _`Input: v1, v2, Point`_
<br>

``` python
origin = Point(0, 0, 0)

plane_ex = Plane.byTwoVectorsOrigin(v1, v2, origin)
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
> _`Input: ??`_
<br>

``` python
l2d = # ??
```
<br>

#### Line2D.length:  
> _`Input: Line2D`_
<br>

``` python
Line2D.length(l2d) # Calculate the length of a 2D Line
```
<br>

#### PolyCurve2D.byJoinedCurves:  
> _`Input: Line2D`_
<br>

``` python
ply2D = PolyCurve2D.byJoinedCurves([
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

#### PolyCurve.byJoinedCurves:  
> _`Input: Line`_
<br>

``` python
PC1 = PolyCurve.byJoinedCurves([Line1, Line2, Line3]) # Create a PolyCurve object by joining a list of curves and collecting their starting points
```
<br>

#### PolyCurve.byPoints:  

>_<code>Input usage: Polycurve.byPoints(list[<a href="#link_point">Point</a>])</code>_


``` python
PolyCurve.byPoints([Point1, Point2, Point3, Point4, Point1]) # Creating a PolyCurve object from a list of Points
```
<br>

#### PolyCurve.byPolyCurve2D:  
> _`Input: PolyCurve2D`_
<br>

``` python
PolyCurve.byPolyCurve2D(ply2D) # Creating a PolyCurve object from a 2D polygon curve defined by four points
```
<br>

#### PolyCurve.translate:  
> _`Input: Vector3`_
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
plygn1 = PolyGon(flat_curves) # Create a Polygon using a list of Lines
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
Arc.length(arc1) # Calculate length of Arc using its points
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
> _`Input: Point, XAxis, YAxis, ZAxis`_
<br>

``` python
XAxis = Vector3(1, 0, 0)
YAxis = Vector3(0, 1, 0)
ZAxis = Vector3(0, 0, 0)

CoordinateSystem(Point(0, 0, 0), XAxis, YAxis, ZAxis) # returns CoordinateSystem
```
<br>

#### Boundingbox:  
> _`Input: POINTS=list[Points]`_
<br>

``` python
BoundingBox2d(points=[POINTS]).perimeter() # returns 2d-perimeter
BoundingBox3d(points=[POINTS]).perimeter() # returns 3d-perimeter
```