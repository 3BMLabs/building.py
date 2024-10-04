# Class `Ellipse`
Represents an ellipse defined by its two radii and the plane it lies in.

## Constructor

### `__init__(self, firstRadius: float, secondRadius: float, plane: Plane) -> Ellipse`
The Ellipse class describes an ellipse through its major and minor radii and the plane it occupies.
            
        - `firstRadius` (float): The first (major) radius of the ellipse.
        - `secondRadius` (float): The second (minor) radius of the ellipse.
        - `plane` (Plane): The plane in which the ellipse lies.
        

---


## Methods

- `__id__(self)`: Returns the ID of the Ellipse.

        

- `__str__(self) -> str`: Generates a string representation of the Ellipse object.

        


## Documentation

#### `__id__(self)`

Returns the ID of the Ellipse.

#### Returns:
`str`: The ID of the Ellipse in the format "id:{self.id}".


---

#### `__str__(self) -> str`

Generates a string representation of the Ellipse object.

#### Returns:
`str`: A string that represents the Ellipse object.

#### Example usage:
```python
ellipse = Ellipse(firstRadius, secondRadius, plane)
print(ellipse)
# Output: Ellipse(...)
```


---

