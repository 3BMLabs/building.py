import sys
from pathlib import Path


sys.path.append(str(Path(__file__).resolve().parents[1]))

from BuildingPy import Vector, BuildingPy
v = Vector(x=20,y=10,z=20)
print(v)