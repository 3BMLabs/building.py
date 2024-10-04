# Class `NurbsSurface`
Represents a NURBS (Non-Uniform Rational B-Spline) surface.

## Constructor

### `__init__(self) -> NurbsSurface`
NurbsSurface is a mathematical model representing a 3D surface in terms of NURBS, a flexible method to represent curves and surfaces. It encompasses properties such as ID and type but is primarily defined by its control points, weights, and degree in the U and V directions.

        - `id` (str): A unique identifier for the NurbsSurface.
        - `type` (str): Class name, "NurbsSurface".
        

---


## Methods

- `__id__(self) -> str`: Returns the unique identifier of the NurbsSurface object.
        This method provides a standardized way to access the unique ID of the NurbsSurface, useful for identification and tracking purposes within a system that handles multiple surfaces.

        

- `__str__(self) -> str`: Generates a string representation of the NurbsSurface object.
        This method creates a string that summarizes the NurbsSurface, typically including its class name and potentially its unique ID, providing a concise overview of the object when printed or logged.

        


## Documentation

#### `__id__(self) -> str`

Returns the unique identifier of the NurbsSurface object.
This method provides a standardized way to access the unique ID of the NurbsSurface, useful for identification and tracking purposes within a system that handles multiple surfaces.

#### Returns:
`str`: The unique identifier of the NurbsSurface, prefixed with "id:".

#### Example usage:
```python
nurbs_surface = NurbsSurface()
print(nurbs_surface.__id__())
# Output format: "id:{unique_id}"
```


---

#### `__str__(self) -> str`

Generates a string representation of the NurbsSurface object.
This method creates a string that summarizes the NurbsSurface, typically including its class name and potentially its unique ID, providing a concise overview of the object when printed or logged.

#### Returns:
`str`: A string representation of the NurbsSurface object.

#### Example usage:
```python
nurbs_surface = NurbsSurface()
print(nurbs_surface)
# Output: "NurbsSurface({self})"
```


---

