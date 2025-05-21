import sys, os, math
from pathlib import Path
from typing import Any, List


from abstract.color import Color
from abstract.matrix import CoordinateSystem
from abstract.vector import Point, Vector
from construction.annotation import BeamTag, ColumnTag, DT2_5_mm, Dimension
from construction.beam import Beam
from construction.datum import Grid, GridLine, seqChar, seqNumber
from construction.panel import Panel
from construction.profile import RectangleProfile
from geometry.curve import Line
from library.material import BaseSteel, Material
from project import fileformat


from packages.text import Text

project = fileformat.BuildingPy("Aanbouw", "0")


# INPUT
DL = Dimension(Point(0, -1000, 0), Point(5400, -1000, 0), DT2_5_mm)
print(DL.start)
DL.write(project)

# GRIDS
grids = Grid.by_spacing_labels(
    "9x5500", seqChar, "3x5500", seqNumber, 1600
).write(project)
GridLine.by_startpoint_endpoint(
    Line(Point(100, 100, 0), Point(-5000, 10000, 0)), "Q"
).write(project)
BaseConcrete = Material("Concrete", Color.RGB([192, 192, 192]))

# PANEL
project.objects.append(
    Panel.by_baseline_height(
        Line(start=Point(1000, 10800 + 5400, 0), end=Point(5000, 10800 + 5400, 0)),
        2500,
        150,
        "Concrete Wall",
        BaseConcrete,
    )
)


# COLUMNS
# project.objects.append(Frame.by_startpoint_endpoint_profile(Point(1000,1000,0),Point(500,1000,3000),"HEA200","Kolom",BaseSteel))
f1 = Beam(
    Point(10800, 5400, 0),
    Point(10800, 5400, 3000),
    RectangleProfile("A", 400, 400),
    "BK 400x400",
    BaseConcrete,
    0,
).write(project)
f2 = Beam(
    Point(0, 5400, 0),
    3000,
    RectangleProfile("A", 400, 400),
    "BK 400x400",
    BaseConcrete,
    0,
).write(project)
f3 = Beam.by_point_profile_height_rotation(
    Point(5400, 5400, 0), 3000, "HEA200", 0, BaseSteel
).write(project)
ColumnTag.by_beam(f2).write(project)
ColumnTag.by_beam(f1).write(project)
ColumnTag.by_beam(f3).write(project)

f4 = Beam.by_startpoint_endpoint_profile(
    Point(0, 3000, 0), Point(10800, 6000, 0), "IPE400", "IPE400 zeeg 30 mm", BaseSteel
).write(project)
tg = BeamTag.by_frame(f4).write(project)

CS = CoordinateSystem.by_origin(Point(10800, 10800, 0))
t1 = Text(text="Textnote", font_family="calibri", cs=CS, height=200).write()
for x in t1:
    project.objects.append(x)

CS = CoordinateSystem.identity(3)
t2 = Text(text="Textnote", font_family="calibri", cs=CS, height=200).write()
for x in t2:
    project.objects.append(x)

# Columntag1 = Columntag.by_cs_text(CS,"HEA200").write()

project.to_speckle("261190074a")
