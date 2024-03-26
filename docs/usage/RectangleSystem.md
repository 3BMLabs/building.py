# Class `RectangleSystem`
The `RectangleSystem` class is designed to represent and manipulate rectangular systems, focusing on dimensions, frame types, and panel arrangements within a specified coordinate system.

## Constructor

### `__init__(self)`
Initializes a new RectangleSystem instance.
        
        - `type` (str): Class name, indicating the object type as "RectangleSystem".
        - `name` (str, optional): The name of the rectangle system.
        - `id` (str): A unique identifier for the rectangle system instance.
        - `height` (float): The height of the rectangle system.
        - `width` (float): The width of the rectangle system.
        - `bottom_frame_type` (Rectangle): A `Rectangle` instance for the bottom frame type.
        - `top_frame_type` (Rectangle): A `Rectangle` instance for the top frame type.
        - `left_frame_type` (Rectangle): A `Rectangle` instance for the left frame type.
        - `right_frame_type` (Rectangle): A `Rectangle` instance for the right frame type.
        - `inner_frame_type` (Rectangle): A `Rectangle` instance for the inner frame type.
        - `material` (BaseTimber): The material used for the system, pre-defined as `BaseTimber`.
        - `inner_width` (float): The computed inner width of the rectangle system, excluding the width of the left and right frames.
        - `inner_height` (float): The computed inner height of the rectangle system, excluding the height of the top and bottom frames.
        - `coordinatesystem` (CSGlobal): A global coordinate system applied to the rectangle system.
        - `local_coordinate_system` (CSGlobal): A local coordinate system specific to the rectangle system.
        - `division_system` (DivisionSystem, optional): A `DivisionSystem` instance to manage divisions within the rectangle system.
        - `inner_frame_objects` (list): A list of inner frame objects within the rectangle system.
        - `outer_frame_objects` (list): A list of outer frame objects.
        - `panel_objects` (list): A list of panel objects used within the system.
        - `symbolic_inner_mother_surface` (PolyCurve, optional): A symbolic representation of the inner mother surface.
        - `symbolic_inner_panels` (list, optional): Symbolic representations of inner panels.
        - `symbolic_outer_grids` (list): Symbolic representations of outer grids.
        - `symbolic_inner_grids` (list): Symbolic representations of inner grids.
        

---


## Methods

- `_RectangleSystem__inner_frames(self)`: Creates inner frame objects based on division distances within the rectangle system.
        Utilizes the division distances to place vertical frames across the inner width of the rectangle system. These frames are represented both as Frame objects within the system and as symbolic lines for visualization.

        

- `_RectangleSystem__inner_mother_surface(self)`: Determines the inner mother surface dimensions and creates its symbolic representation.
        Calculates the inner width and height by subtracting the frame widths from the total width and height. It then constructs a symbolic PolyCurve representing the mother surface within the rectangle system's frames.

        

- `_RectangleSystem__inner_panels(self)`: Calculates and creates inner panel objects for the RectangleSystem.
        This method iteratively calculates the positions and dimensions of inner panels based on the division system's distances and the inner frame type's width. It populates the `panel_objects` list with created panels.

        

- `_RectangleSystem__outer_frames(self)`: Generates the outer frame objects for the rectangle system.
        Creates Frame objects for the bottom, top, left, and right boundaries of the rectangle system. Each frame is defined by its start and end points, along with its type and material. Symbolic lines representing these frames are also generated for visualization.

        

- `by_width_height_divisionsystem_studtype(self, width: float, height: float, frame_width: float, frame_height: float, division_system: geometry.systemsimple.DivisionSystem, filling: bool) -> RectangleSystem`: Configures the rectangle system with specified dimensions, division system, and frame types.
        This method sets the dimensions of the rectangle system, configures the frame types based on the provided dimensions, and applies a division system to generate inner frames. Optionally, it can also fill the system with panels based on the inner divisions.

        


## Documentation

#### `_RectangleSystem__inner_frames(self)`

Creates inner frame objects based on division distances within the rectangle system.
Utilizes the division distances to place vertical frames across the inner width of the rectangle system. These frames are represented both as Frame objects within the system and as symbolic lines for visualization.

#### Effects:
- Generates Frame objects for each division, placing them vertically within the rectangle system.
- Populates `inner_frame_objects` with these Frame instances.
- Adds symbolic representations of these frames to `symbolic_inner_grids`.


---

#### `_RectangleSystem__inner_mother_surface(self)`

Determines the inner mother surface dimensions and creates its symbolic representation.
Calculates the inner width and height by subtracting the frame widths from the total width and height. It then constructs a symbolic PolyCurve representing the mother surface within the rectangle system's frames.

#### Effects:
- Updates `inner_width` and `inner_height` attributes based on frame dimensions.
- Creates a symbolic PolyCurve `symbolic_inner_mother_surface` representing the inner mother surface.


---

#### `_RectangleSystem__inner_panels(self)`

Calculates and creates inner panel objects for the RectangleSystem.
This method iteratively calculates the positions and dimensions of inner panels based on the division system's distances and the inner frame type's width. It populates the `panel_objects` list with created panels.

#### Effects:
- Populates `panel_objects` with Panel instances representing the inner panels of the rectangle system.


---

#### `_RectangleSystem__outer_frames(self)`

Generates the outer frame objects for the rectangle system.
Creates Frame objects for the bottom, top, left, and right boundaries of the rectangle system. Each frame is defined by its start and end points, along with its type and material. Symbolic lines representing these frames are also generated for visualization.

#### Effects:
- Creates Frame instances for the outer boundaries of the rectangle system and adds them to `outer_frame_objects`.
- Generates symbolic Line instances for each outer frame and adds them to `symbolic_outer_grids`.


---

#### `by_width_height_divisionsystem_studtype(self, width: float, height: float, frame_width: float, frame_height: float, division_system: geometry.systemsimple.DivisionSystem, filling: bool) -> RectangleSystem`

Configures the rectangle system with specified dimensions, division system, and frame types.
This method sets the dimensions of the rectangle system, configures the frame types based on the provided dimensions, and applies a division system to generate inner frames. Optionally, it can also fill the system with panels based on the inner divisions.

#### Parameters:
- `width` (float): The width of the rectangle system.
- `height` (float): The height of the rectangle system.
- `frame_width` (float): The width of the frame elements.
- `frame_height` (float): The height (thickness) of the frame elements.
- `division_system` (DivisionSystem): The division system to apply for inner divisions.
- `filling` (bool): A flag indicating whether to fill the divided areas with panels.

#### Returns:
`RectangleSystem`: The instance itself, updated with the new configuration.

#### Example usage:
```python
rectangle_system = RectangleSystem()
rectangle_system.by_width_height_divisionsystem_studtype(2000, 3000, 38, 184, divisionSystem, True)
```


---

