# Class `MeshPB`
Represents a mesh object with vertices, faces, and other attributes.

## Constructor

### `__init__(self)`
The MeshPB class is designed to construct mesh objects from vertices and faces. It supports creating meshes from a variety of inputs including vertex-face lists, polycurves, and coordinate lists with support for nested structures.
        
        - `verts` (list): A list of vertices that make up the mesh.
        - `faces` (list): A list defining the faces of the mesh. Each face is represented by indices into the `verts` list.
        - `numberFaces` (int): The number of faces in the mesh.
        - `name` (str): The name of the mesh.
        - `material` (Material): The material assigned to the mesh.
        - `colorlst` (list): A list of colors for the mesh, derived from the material.
        

---


## Methods

- `by_coords(self, lsts: list, name: str, material, doublenest: bool) -> MeshPB`: Creates a mesh from a list of coordinates.

        

- `by_polycurve(self, PC, name: str, material) -> MeshPB`: Creates a mesh from a polycurve object.

        

- `by_verts_faces(self, verts: list, faces: list) -> MeshPB`: Initializes the mesh with vertices and faces.

        


## Documentation

#### `by_coords(self, lsts: list, name: str, material, doublenest: bool) -> MeshPB`

Creates a mesh from a list of coordinates.

#### Parameters:
- `lsts` (list): A nested list of coordinates defining the vertices of the mesh.
- `name` (str): The name of the mesh.
- `material` (Material): The material to apply to the mesh.
- `doublenest` (bool): A flag indicating if the list of coordinates is double-nested.

This method allows for flexible mesh creation from complex nested list structures of coordinates.

#### Example usage:
```python

```


---

#### `by_polycurve(self, PC, name: str, material) -> MeshPB`

Creates a mesh from a polycurve object.

#### Parameters:
- `PC` (Polycurve): A polycurve object from which to generate the mesh.
- `name` (str): The name of the mesh.
- `material` (Material): The material to apply to the mesh.

This method constructs the mesh such that it represents the shape defined by the polycurve.

#### Example usage:
```python

```


---

#### `by_verts_faces(self, verts: list, faces: list) -> MeshPB`

Initializes the mesh with vertices and faces.

#### Parameters:
- `verts` (list): A list of vertices.
- `faces` (list): A list of faces. Each face is a list of indices into the `verts` list.

This method directly sets the vertices and faces of the mesh based on the input lists.

#### Example usage:
```python

```


---

