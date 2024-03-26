# Class `Circle`
Represents a circle with a specific radius, plane, and length.
    

## Constructor

### `__init__(self, radius: float, plane: Plane, length: float) -> Circle`
The Circle class defines a circle by its radius, the plane it lies in, and its calculated length (circumference).

        - `radius` (float): The radius of the circle.
        - `plane` (Plane): The plane in which the circle lies.
        - `length` (float): The length (circumference) of the circle. Automatically calculated during initialization.
        

---


## Methods

- `__id__(self)`: Returns the ID of the Circle.

        

- `__str__(self) -> str`: Generates a string representation of the Circle object.

        


## Documentation

#### `__id__(self)`

Returns the ID of the Circle.

#### Returns:
`str`: The ID of the Circle in the format "id:{self.id}".


---

#### `__str__(self) -> str`

Generates a string representation of the Circle object.

#### Returns:
`str`: A string that represents the Circle object.

#### Example usage:
```python
circle = Circle(radius, plane, length)
print(circle)
# Output: Circle(...)
```


---

