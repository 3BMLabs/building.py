# Class `Extrusion`
The Extrusion class represents the process of extruding a 2D profile into a 3D mesh or solid form. It is designed to handle geometric transformations and properties related to the extrusion process.

## Constructor

### `__init__(self)`
The Extrusion class represents the process of extruding a 2D profile into a 3D mesh or solid form. It is designed to handle geometric transformations and properties related to the extrusion process.
        
        - `id` (str): A unique identifier for the extrusion instance.
        - `type` (str): Class name, indicating the object type as "Extrusion".
        - `parameters` (list): A list of parameters associated with the extrusion.
        - `verts` (list): A list of vertices that define the shape of the extruded mesh.
        - `faces` (list): A list of faces, each defined by indices into the `verts` list.
        - `numberFaces` (int): The total number of faces in the extrusion.
        - `countVertsFaces` (int): The total number of vertices per face, distinct from the total vertex count.
        - `name` (str): The name assigned to the extrusion instance.
        - `color` (tuple): The color of the extrusion, defined as an RGB tuple.
        - `colorlst` (list): A list of colors applied to the extrusion, potentially varying per face or vertex.
        - `topface` (PolyCurve): The top face of the extrusion, returned as a polycurve converted to a surface.
        - `bottomface` (PolyCurve): The bottom face of the extrusion, similar to `topface`.
        - `polycurve_3d_translated` (PolyCurve): A polycurve representing the translated 3D profile of the extrusion.
        - `bottomshape` (list): A list representing the shape of the bottom face of the extrusion.
        

---


## Methods

- `by_polycurve_height(cls, polycurve: geometry.curve.PolyCurve, height: float, dz_loc: float) -> Extrusion`: Creates an extrusion from a PolyCurve with a specified height and base elevation.
        This method generates a vertical extrusion of a given PolyCurve. The PolyCurve is first translated vertically by `dz_loc`, then extruded to the specified `height`, creating a solid form.

        

- `by_polycurve_height_vector(cls, polycurve_2d: geometry.geometry2d.PolyCurve2D, height: float, cs_old: geometry.point.CoordinateSystem, start_point: geometry.point.Point, direction_vector: abstract.vector.Vector) -> Extrusion`: Creates an extrusion from a 2D polycurve profile along a specified vector.
        This method extrudes a 2D polycurve profile into a 3D form by translating it to a specified start point and direction. The extrusion is created perpendicular to the polycurve's plane, extending it to the specified height.

        

- `deserialize(data: dict) -> Extrusion`: Reconstructs an Extrusion object from a dictionary.
        This static method allows for the creation of an Extrusion instance from serialized data, enabling the loading of extrusion objects from file storage or network data.

        

- `merge(cls, extrusions: list, name: str = None) -> Extrusion`: Merges multiple Extrusion instances into a single one.
        This class method combines several extrusions into a single Extrusion object, potentially useful for operations requiring unified geometric manipulation.

        

- `serialize(self) -> dict`: Serializes the extrusion object into a dictionary.
        This method facilitates the conversion of the Extrusion instance into a dictionary format, suitable for serialization to JSON or other data formats for storage or network transmission.

        

- `set_parameter(self, data: list) -> Extrusion`: Sets parameters for the extrusion.
        This method allows for the modification of the Extrusion's parameters, which can influence the extrusion process or define additional properties.

        


## Documentation

#### `by_polycurve_height(cls, polycurve: geometry.curve.PolyCurve, height: float, dz_loc: float) -> Extrusion`

Creates an extrusion from a PolyCurve with a specified height and base elevation.
This method generates a vertical extrusion of a given PolyCurve. The PolyCurve is first translated vertically by `dz_loc`, then extruded to the specified `height`, creating a solid form.

#### Parameters:
- `polycurve` (PolyCurve): The PolyCurve to be extruded.
- `height` (float): The height of the extrusion.
- `dz_loc` (float): The base elevation offset from the original plane of the PolyCurve.

#### Returns:
`Extrusion`: An Extrusion object that represents the 3D extruded form of the input PolyCurve.

#### Example usage:
```python
extrusion = Extrusion.by_polycurve_height(polycurve, 5, 0)
```


---

#### `by_polycurve_height_vector(cls, polycurve_2d: geometry.geometry2d.PolyCurve2D, height: float, cs_old: geometry.point.CoordinateSystem, start_point: geometry.point.Point, direction_vector: abstract.vector.Vector) -> Extrusion`

Creates an extrusion from a 2D polycurve profile along a specified vector.
This method extrudes a 2D polycurve profile into a 3D form by translating it to a specified start point and direction. The extrusion is created perpendicular to the polycurve's plane, extending it to the specified height.

#### Parameters:
- `polycurve_2d` (PolyCurve2D): The 2D polycurve to be extruded.
- `height` (float): The height of the extrusion.
- `cs_old` (CoordinateSystem): The original coordinate system of the polycurve.
- `start_point` (Point): The start point for the extrusion in the new coordinate system.
- `direction_vector` (Vector): The direction vector along which the polycurve is extruded.

#### Returns:
`Extrusion`: An Extrusion object representing the 3D form of the extruded polycurve.

#### Example usage:
```python
extrusion = Extrusion.by_polycurve_height_vector(polycurve_2d, 10, oldCS, startPoint, directionVec)
```


---

#### `deserialize(data: dict) -> Extrusion`

Reconstructs an Extrusion object from a dictionary.
This static method allows for the creation of an Extrusion instance from serialized data, enabling the loading of extrusion objects from file storage or network data.

#### Parameters:
- `data` (dict): A dictionary containing serialized Extrusion data.

#### Returns:
`Extrusion`: A newly constructed Extrusion instance based on the provided data.

#### Example usage:
```python

```


---

#### `merge(cls, extrusions: list, name: str = None) -> Extrusion`

Merges multiple Extrusion instances into a single one.
This class method combines several extrusions into a single Extrusion object, potentially useful for operations requiring unified geometric manipulation.

#### Parameters:
- `extrusions` (list): A list of Extrusion instances to be merged.
- `name` (str, optional): The name for the merged extrusion.

#### Returns:
`Extrusion`: A new Extrusion instance resulting from the merger of the provided extrusions.

#### Example usage:
```python

```


---

#### `serialize(self) -> dict`

Serializes the extrusion object into a dictionary.
This method facilitates the conversion of the Extrusion instance into a dictionary format, suitable for serialization to JSON or other data formats for storage or network transmission.

#### Returns:
`dict`: A dictionary representation of the Extrusion instance, including all relevant geometric and property data.

#### Example usage:
```python

```


---

#### `set_parameter(self, data: list) -> Extrusion`

Sets parameters for the extrusion.
This method allows for the modification of the Extrusion's parameters, which can influence the extrusion process or define additional properties.

#### Parameters:
- `data` (list): A list of parameters to be applied to the extrusion.

#### Returns:
`Extrusion`: The Extrusion instance with updated parameters.

#### Example usage:
```python

```


---

