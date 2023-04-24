# BUILDING.PY EXAMPLES

#### Vector2:  
> _`Input: XY=(number/float)`_
<br>

``` python
Vector2(0, 100) # returns 2d-vector
```
<br>

#### Point2D:
> _`Input: XY=(number/float)`_
<br>

``` python
Point2D(0, 100) # returns Point2D
```
<br>

#### Point:
##### link_point
> _`Input: XYZ=(number/float)`_
<br>

``` python
Point(0, 100, 20) # returns Point
```
<br>

#### Vector3:  
> _`Input: XYZ=(number/float)`_
<br>

``` python
Vector3(0, 1, 0) # returns 3d-vector

v1 = Vector3(0, 1, 0) # example vector1
v2 = Vector3(1, 0, 0) # example vector2
Vector3.sum(v1, v2) # returns sum of 2 vectors
Vector3.crossProduct(v1, v2) # returns vector perpendicular on the two vectors
Vector3.dotProduct(v1, v2) # inner product, if zero, then vectors are perpendicular
Vector3.product(5, v1) # Same as scale
Vector3.length(v1) # returns the length of a vector
Vector3.pitch(v1, 45) # ??
Vector3.angleBetween(v1, v2) # returns the angle between two vectors
Vector3.reverse(v1) # returns vector in the opposite direction
Vector3.perpendicular(v1) # Vector local X and local Y perpendicular to given vector and in global Z-direction
Vector3.normalise(v1) # ??
Vector3.byTwoPoints(p1, p2) # Subtracts point1 x,y and z from point2 x,y and z
```
<br>

#### Line:
_<code>Input usage: Line(start=<a href="#link_point">Point</a>, end=<a href="#link_point">Point</a>)</code>_
<br>
``` python
Line1 = Line(start=Point(0, 0, 0), end=Point(0, 500, 0))
Line2 = Line(start=Point(0, 500, 0), end=Point(-200, 500, 0))
Line3 = Line(start=Point(-200, 500, 0), end=Point(100, 1000, 0))
Line4 = Line(start=Point(100, 1000, 0), end=Point(400, 500, 0))
Line5 = Line(start=Point(400, 500, 0), end=Point(200, 500, 0))
Line6 = Line(start=Point(200, 500, 0), end=Point(200, 0, 0))
Line7 = Line(start=Point(200, 0, 0), end=Point(0, 0, 0))

Line.length(Line1) # Calculate the length of a line
```
<br>

#### Polycurve.byJoinedCurves:  
> _`Input: Line`_
<br>

``` python
plycurve = PolyCurve()

PolyCurve.byJoinedCurves([Line1, Line2, Line3]) # Create a PolyCurve object by joining a list of curves and collecting their starting points
```
<br>

#### Polycurve.byPoints:  
> _`Input: Point`_
<br>

``` python
PolyCurve.byPoints(
    [Point(0, 0, 0),
     Point(2000, 0, 0),
     Point(0, 1000, 2000),
     Point(0, 0, 0)
     ])
```
<br>

#### Polycurve.byJoinedCurves:  
> _`Input: Point, Line2D`_
<br>

``` python
PolyCurve2D.byJoinedCurves([
    Line2D(
        Point2D(0,0),
        Point2D(100,0)),
    Line2D(
        Point2D(100, 0),
        Point2D(100, 100)),
    Line2D(
        Point2D(100,100),
        Point2D(0,0))]
    ) # Creating a PolyCurve object (PC2) from a list of Points.
    # by points, must be a closed polygon
```
<br>

#### Polycurve.byPolyCurve2D:  
> _`Input: PolyCurve2D`_
<br>

``` python
PolyCurve.byPolyCurve2D(ply2D) # Creating a PolyCurve object from a 3D polygon curve defined by four points
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

#### Plane.byTwoVectorsOrigin:  
> _`Input: v1, v2, Point`_
<br>

``` python
origin = Point(0, 0, 0)
v1 = Vector3(0, 1, 0)
v2 = Vector3(1, 1, 0)

Plane.byTwoVectorsOrigin(v1, v2, origin)
# returns Plane
```
<br>

#### Boundingbox:  
> _`Input: POINTS=list[Points]`_
<br>

``` python
BoundingBox2d(points=[POINTS]).perimeter() # returns 2d-perimeter
BoundingBox3d(points=[POINTS]).perimeter() # returns 3d-perimeter
```