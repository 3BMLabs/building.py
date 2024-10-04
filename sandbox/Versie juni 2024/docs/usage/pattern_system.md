# Class `pattern_system`
The `pattern_system` class is designed to define and manipulate patterns for architectural or design applications. It is capable of generating various patterns based on predefined or dynamically generated parameters.

## Constructor

### `__init__(self)`
Initializes a new pattern_system instance.

---


## Methods

- `cross_bond_with_joint(self, name: str, brick_width: float, brick_length: float, brick_height: float, joint_width: float, joint_height: float)`: Configures a cross bond pattern with joints for the pattern_system.
        Sets up a complex brick laying pattern combining stretcher (lengthwise) and header (widthwise) bricks in alternating rows, creating a cross bond appearance. This method defines the base panels and their positioning vectors to achieve the cross bond pattern.

        

- `stretcher_bond_with_joint(self, name: str, brick_width: float, brick_length: float, brick_height: float, joint_width: float, joint_height: float)`: Configures a stretcher bond pattern with joints for the pattern_system.
        Establishes the fundamental vectors and base panels for a stretcher bond, taking into account brick dimensions and joint sizes. This pattern alternates bricks in each row, offsetting them by half a brick length.

        

- `tile_bond_with_joint(self, name: str, tile_width: float, tile_height: float, tile_thickness: float, joint_width: float, joint_height: float)`: Configures a tile bond pattern with specified dimensions and joint sizes for the pattern_system.
        Defines a simple tiling pattern where tiles are laid out in rows and columns, separated by specified joint widths and heights. This method sets up base panels to represent individual tiles and their arrangement vectors.

        


## Documentation

#### `cross_bond_with_joint(self, name: str, brick_width: float, brick_length: float, brick_height: float, joint_width: float, joint_height: float)`

Configures a cross bond pattern with joints for the pattern_system.
Sets up a complex brick laying pattern combining stretcher (lengthwise) and header (widthwise) bricks in alternating rows, creating a cross bond appearance. This method defines the base panels and their positioning vectors to achieve the cross bond pattern.

#### Parameters:
- `name` (str): The name of the cross bond pattern configuration.
- `brick_width` (float): The width of a single brick.
- `brick_length` (float): The length of the brick.
- `brick_height` (float): The height of the brick layer.
- `joint_width` (float): The width of the joint between bricks.
- `joint_height` (float): The height of the joint between brick layers.

#### Returns:
The instance itself, updated with the cross bond pattern configuration.

#### Example Usage:
```python
pattern_system = pattern_system()
pattern_system.cross_bond_with_joint('CrossBondPattern', 90, 190, 80, 10, 10)
```
In this configuration, `pattern_system` is set to a cross bond pattern named 'CrossBondPattern', with bricks measuring 90x190x80 units and 10 units of joint spacing in both directions.


---

#### `stretcher_bond_with_joint(self, name: str, brick_width: float, brick_length: float, brick_height: float, joint_width: float, joint_height: float)`

Configures a stretcher bond pattern with joints for the pattern_system.
Establishes the fundamental vectors and base panels for a stretcher bond, taking into account brick dimensions and joint sizes. This pattern alternates bricks in each row, offsetting them by half a brick length.

#### Parameters:
- `name` (str): Name of the pattern configuration.
- `brick_width` (float): Width of the brick.
- `brick_length` (float): Length of the brick.
- `brick_height` (float): Height of the brick.
- `joint_width` (float): Width of the joint between bricks.
- `joint_height` (float): Height of the joint between brick layers.

#### Returns:
The instance itself, updated with the stretcher bond pattern configuration.

#### Example usage:
```python

```


---

#### `tile_bond_with_joint(self, name: str, tile_width: float, tile_height: float, tile_thickness: float, joint_width: float, joint_height: float)`

Configures a tile bond pattern with specified dimensions and joint sizes for the pattern_system.
Defines a simple tiling pattern where tiles are laid out in rows and columns, separated by specified joint widths and heights. This method sets up base panels to represent individual tiles and their arrangement vectors.

#### Parameters:
- `name` (str): The name of the tile bond pattern configuration.
- `tile_width` (float): The width of a single tile.
- `tile_height` (float): The height of a single tile.
- `tile_thickness` (float): The thickness of the tile.
- `joint_width` (float): The width of the joint between adjacent tiles.
- `joint_height` (float): The height of the joint between tile rows.

#### Returns:
The instance itself, updated with the tile bond pattern configuration.

#### Example Usage:
```python
pattern_system = pattern_system()
pattern_system.tile_bond_with_joint('TilePattern', 200, 300, 10, 5, 5)
```
This configures the `pattern_system` with a tile bond pattern named 'TilePattern', where each tile measures 200x300x10 units, with 5 units of spacing between tiles.


---

