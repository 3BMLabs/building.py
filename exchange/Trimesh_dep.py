#install dep: pip install "pyglet<2

import sys
from pathlib import Path
import trimesh
import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[1]))

from project.fileformat import *

class Trimesh:
    def __init__(self, name, mesh) -> None:
        self.type = __class__.__name__
        self.name = name or ""
        self.vertices = np.array([coord for vertex in mesh.vertices for coord in vertex], dtype=float).tolist()
        self.faces = np.array([index for face in mesh.faces for index in face], dtype=int).tolist()


length = 1
width = 1
height = 0.4

box_mesh = trimesh.creation.box(extents=(length, width, height))

torus_major_radius = 0.3
torus_minor_radius = 0.1

torus_mesh = trimesh.creation.torus(torus_major_radius, torus_minor_radius)

torus_position = np.array([(length - torus_major_radius * 2) / 2, (width - torus_major_radius * 2) / 2, 0])
torus_mesh.apply_translation(torus_position)

box_with_hole_mesh = box_mesh.difference(torus_mesh)


t_mesh = Trimesh("trimesh_object", box_with_hole_mesh)

box_with_hole_mesh.export('box_with_hole_mesh.obj')
box_with_hole_mesh.show()
