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
Vector3(0, 100, 0) #returns 3d-vector
```
<br>

#### Boundingbox:  
> _`Input: POINTS=list[Points]`_
<br>

``` python
BoundingBox2d(points=[POINTS]).perimeter() #returns 2d-perimeter
BoundingBox3d(points=[POINTS]).perimeter() #returns 3d-perimeter
```