import sys, os, math
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from construction.panel import *
from construction.frame import *
from construction.profile import *
from exchange.speckle import *
from library.profile import data as jsondata
from library.material import *
from library.profile import nameToProfile
from geometry.surface import Surface
from construction.annotation import *
from abstract.intersect2d import *
from geometry.systemsimple import *



project = BuildingPy("Polygon, to Surface and DXF to Ifc","0")


class Serializable:
    # Placeholder for the Serializable base class
    pass

class Shape(Serializable):
    def __init__(self, ID, name: str, description: str):
        super().__init__()  # Ensure the Serializable base class is initialized
        self.ID = ID
        self.name = name
        self.description = description
        self.curve = []

class RectangularShape(Shape):
    def __init__(self, width: float, height: float, **kwargs):
        super().__init__(**kwargs)
        self.width = width
        self.height = height

class SteelShape(Shape):
    def __init__(self, IFC_profile_def: str, **kwargs):
        super().__init__(**kwargs)
        self.IFC_profile_def = IFC_profile_def

class SteelRectangularShape(SteelShape, RectangularShape):
    def __init__(self, ID, name: str, description: str, IFC_profile_def: str, width: float, height: float):
        # Initialize Shape through the correct order
        #Shape.__init__(self, ID, name, description)
        #super().__init__(IFC_profile_def, width, height)
        #RectangularShape.__init__(self, ID= ID, name, description, width, height)
        #SteelShape.__init__(self, ID, name, description, IFC_profile_def)
        super().__init__(ID=ID, name=name,description=description, IFC_profile_def=IFC_profile_def, width=width,height=height)

# Example of how to create a SteelRectangularShape object
steel_rectangular_shape = SteelRectangularShape("HEA", "Steel Beam", "A steel beam", "IFC_HEA", 200, 100)
print(vars(steel_rectangular_shape))

r = RectangularSteelShape("test", "name", "desc", "def", 3, 4)

p1 = Point(0,0, 0)
p2 = Point(0,3000, 0)
#p3 = Point(2000,6500, 0)
p4 = Point(4000,3000, 0)
#p5 = Point(4000,0, 0)
PG1 = Polygon.by_points([p1,p2,p4,])

#ip1_1 = Point(1000, 1000, 500)
#ip1_2 = Point(1000, 2000, 500)
#ip1_3 = Point(2000, 2000, 1000)
#ip1_4 = Point(2000, 1000, 500)
#innerPolygon1 = Polygon.by_points([ip1_1, ip1_2, ip1_3, ip1_4])#

#ip2_1 = Point(2500, 1000, 10)
#ip2_2 = Point(2500, 2000, 20)
#ip2_3 = Point(3500, 2000, 30)
#ip2_4 = Point(3500, 1000, 40)
#innerPolygon2 = Polygon.by_points([ip2_1, ip2_2, ip2_3, ip2_4])

lst = [PG1]#, innerPolygon1, innerPolygon2]

p = Point(2,3,4)

obj = Surface.by_patch_inner_and_outer(lst)
print(obj)

curve = PolyCurve.by_points([p1, p2, p4])

obj2 = Extrusion.by_polycurve_height(polycurve=curve,height= 2000.0,dz_loc= 0)


#project.objects.append(obj)
project.objects.append(obj2)
# project.objects.append(SF1)
#project.objects.append(PG1)
#project.objects.append(innerPolygon1)
#project.objects.append(innerPolygon2)
#project.save()
#project.open()
project.save()
project.to_speckle("29a6c39880")