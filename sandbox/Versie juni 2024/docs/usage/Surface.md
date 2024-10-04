# Class `Surface`
Represents a surface object created from PolyCurves.

## Constructor

### `__init__(self, PolyCurves: geometry.curve.PolyCurve, color=None) -> None`
This class is designed to manage and manipulate surfaces derived from PolyCurve objects. It supports the generation of mesh representations, serialization/deserialization, and operations like filling and voiding based on PolyCurve inputs.
       
        - `type` (str): The class name, "Surface".
        - `mesh` (list): A list of meshes that represent the surface.
        - `length` (float): The total length of the PolyCurves defining the surface.
        - `area` (float): The area of the surface, excluding any inner PolyCurves.
        - `offset` (float): An offset value for the surface.
        - `name` (str): The name of the surface.
        - `id` (str): A unique identifier for the surface.
        - `PolyCurveList` (list): A list of PolyCurve objects that define the surface.
        - `origincurve` (PolyCurve): The original PolyCurve from which the surface was created.
        - `color` (int): The color of the surface, represented as an integer.
        - `colorlst` (list): A list of color values associated with the surface.
        

---


## Methods

- `__id__(self)`: Returns the unique identifier of the Surface.
        This method provides a way to retrieve the unique ID of the Surface, which can be useful for tracking or identifying surfaces within a larger system.

        

- `__str__(self) -> str`: Generates a string representation of the Surface object.
        This method returns a string that includes the class name and optionally additional details about the Surface object, making it easier to identify and distinguish the surface when printed or logged.

        

- `deserialize(data: dict) -> Surface`: Creates a Surface object from a serialized data dictionary.
        This static method reconstructs a Surface object from a dictionary containing serialized surface data. It is particularly useful for loading surfaces from storage or reconstructing them from data received over a network.

        

- `fill(self, PolyCurveList: list)`: Fills the Surface with the specified PolyCurves.
        This method applies PolyCurves to the Surface, creating an extrusion for each PolyCurve and adding it to the surface's mesh. It also assigns the specified color to each extrusion.

        

- `serialize(self) -> dict`: Serializes the Surface object into a dictionary for storage or transfer.
        This method converts the Surface object's properties into a dictionary format, making it suitable for serialization processes like saving to a file or sending over a network.

        

- `void(self, polyCurve: geometry.curve.PolyCurve)`: Creates a void in the Surface based on the specified PolyCurve.
        This method identifies and removes a part of the Surface that intersects with the given PolyCurve, effectively creating a void in the Surface. It then updates the surface's mesh and color list to reflect this change.

        


## Documentation

#### `__id__(self)`

Returns the unique identifier of the Surface.
This method provides a way to retrieve the unique ID of the Surface, which can be useful for tracking or identifying surfaces within a larger system.

#### Returns:
`str`: The unique identifier of the Surface.

#### Example usage:
```python
id_str = surface.__id__()
print(id_str)
# Outputs the ID of the surface.
```


---

#### `__str__(self) -> str`

Generates a string representation of the Surface object.
This method returns a string that includes the class name and optionally additional details about the Surface object, making it easier to identify and distinguish the surface when printed or logged.

#### Returns:
`str`: A string representation of the Surface object, typically including its class name and potentially other identifying information.

#### Example usage:
```python
surface = Surface(polyCurves, color)
print(surface)
# Output: Surface({...})
```


---

#### `deserialize(data: dict) -> Surface`

Creates a Surface object from a serialized data dictionary.
This static method reconstructs a Surface object from a dictionary containing serialized surface data. It is particularly useful for loading surfaces from storage or reconstructing them from data received over a network.

#### Parameters:
- `data` (`dict`): The dictionary containing the serialized data of a Surface object.

#### Returns:
`Surface`: A new Surface object initialized with the data from the dictionary.

#### Example usage:
```python
data = { ... }  # Serialized Surface data
surface = Surface.deserialize(data)
# surface is now a fully reconstructed Surface object
```


---

#### `fill(self, PolyCurveList: list)`

Fills the Surface with the specified PolyCurves.
This method applies PolyCurves to the Surface, creating an extrusion for each PolyCurve and adding it to the surface's mesh. It also assigns the specified color to each extrusion.

#### Parameters:
- `PolyCurveList` (`list` or `PolyCurve`): A list of PolyCurve objects or a single PolyCurve object to be applied to the Surface.

#### Example usage:
```python
polyCurveList = [polyCurve1, polyCurve2]
surface.fill(polyCurveList)
# The surface is now filled with the specified PolyCurves.
```


---

#### `serialize(self) -> dict`

Serializes the Surface object into a dictionary for storage or transfer.
This method converts the Surface object's properties into a dictionary format, making it suitable for serialization processes like saving to a file or sending over a network.

#### Returns:
`dict`: A dictionary representation of the Surface object, containing all relevant data such as type, mesh, dimensions, name, ID, PolyCurve list, origin curve, color, and color list.

#### Example usage:
```python
surface = Surface(polyCurves, color)
serialized_surface = surface.serialize()
# serialized_surface is now a dictionary representation of the surface object
```


---

#### `void(self, polyCurve: geometry.curve.PolyCurve)`

Creates a void in the Surface based on the specified PolyCurve.
This method identifies and removes a part of the Surface that intersects with the given PolyCurve, effectively creating a void in the Surface. It then updates the surface's mesh and color list to reflect this change.

#### Parameters:
- `polyCurve` (`PolyCurve`): The PolyCurve object that defines the area of the Surface to be voided.

#### Example usage:
```python
surface.void(polyCurve)
# A void is now created in the surface based on the specified PolyCurve.
```


---

