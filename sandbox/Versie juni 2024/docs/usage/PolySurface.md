# Class `PolySurface`
Represents a compound surface consisting of multiple connected surfaces.

## Constructor

### `__init__(self) -> None`
PolySurface is a geometric entity that represents a complex surface made up of several simpler surfaces. These simpler surfaces are typically connected along their edges. Attributes include an ID and type, with functionalities to manipulate and query the composite surface structure.
        
        - `id` (str): A unique identifier for the PolySurface.
        - `type` (str): Class name, "PolySurface".
        

---


## Methods

- `__id__(self) -> str`: Returns the unique identifier of the PolySurface object.
        Similar to the NurbsSurface, this method provides the unique ID of the PolySurface, facilitating its identification and tracking across various operations or within data structures that involve multiple surfaces.

        

- `__str__(self) -> str`: Generates a string representation of the PolySurface object.
        Provides a simple string that identifies the PolySurface, mainly through its class name. This is helpful for debugging, logging, or any scenario where a quick textual representation of the object is beneficial.

        


## Documentation

#### `__id__(self) -> str`

Returns the unique identifier of the PolySurface object.
Similar to the NurbsSurface, this method provides the unique ID of the PolySurface, facilitating its identification and tracking across various operations or within data structures that involve multiple surfaces.

#### Returns:
`str`: The unique identifier of the PolySurface, prefixed with "id:".

#### Example usage:
```python
poly_surface = PolySurface()
print(poly_surface.__id__())
# Output format: "id:{unique_id}"
```


---

#### `__str__(self) -> str`

Generates a string representation of the PolySurface object.
Provides a simple string that identifies the PolySurface, mainly through its class name. This is helpful for debugging, logging, or any scenario where a quick textual representation of the object is beneficial.

#### Returns:
`str`: A string representation of the PolySurface object.

#### Example usage:
```python
poly_surface = PolySurface()
print(poly_surface)
# Output: "PolySurface({self})"
```


---

