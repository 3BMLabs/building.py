# BUILDING.PY EXAMPLES

#### Vector2:  
> _`Input: XY=(number/float)`_
<br>

``` python
Vector2(0, 100) #returns 2d-vector
```
<br>

#### Vector3:  
> _`Input: XYZ=(number/float)`_
<br>

``` python
v1 = Vector3(0, 1, 0)
v2 = Vector3(1, 0, 0)

Vector3(0, 1, 0) #returns 3d-vector
Vector3.sum(v1, v2) #returns sum of 2 vectors
```
<br>

#### Point2D:  
> _`Input: XY=(number/float)`_
<br>

``` python
Point2D(0, 100) #returns Point2D
```
<br>

#### Point:
> _`Input: XYZ=(number/float)`_
<br>

``` python
Point(0, 100, 20) #returns Point
```
<br>

#### CoordinateSystem:  
> _`Input: Point, XAxis, YAxis, ZAxis`_
<br>

``` python
XAxis = Vector3(1, 0, 0)
YAxis = Vector3(0, 1, 0)
ZAxis = Vector3(0, 0, 0)

CoordinateSystem(Point(0, 0, 0), XAxis, YAxis, ZAxis) #returns CoordinateSystem
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
#returns Plane
```
<br>

#### Boundingbox:  
> _`Input: POINTS=list[Points]`_
<br>

``` python
BoundingBox2d(points=[POINTS]).perimeter() #returns 2d-perimeter
BoundingBox3d(points=[POINTS]).perimeter() #returns 3d-perimeter
```