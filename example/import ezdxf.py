import sys
from ezdxf import readfile, DXFStructureError, DXFValueError
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from project.fileformat import *
from geometry.curve import *
from geometry.point import Point
from geometry.geometry2d import Point2D, Line2D, Arc2D, PolyCurve2D
from geometry.surface import *
from exchange.DXF import *
from exchange.IFC import *
from abstract.coordinatesystem import *

def fetch_polycurves(dxf_filepath):
    doc = ezdxf.readfile(dxf_filepath)
    msp = doc.modelspace()

    polycurves = []

    polycurve_types = {'LWPOLYLINE', 'POLYLINE'}
    line_types = {'LINE'}

    for entity in msp:
        if entity.dxftype() in polycurve_types:
            try:
                points = [Point2D(x, y) for x, y in entity.vertices()]
                polygon = Polygon.by_points(points)
                polycurves.append((polygon, entity.dxf.layer))
            except DXFValueError as dxf_error:
                print(f"Failed to process {entity.dxftype()} on layer {entity.dxf.layer} due to a DXF error: {str(dxf_error)}")
            except ValueError as val_error:
                print(f"Data format error with {entity.dxftype()} on layer {entity.dxf.layer}: {str(val_error)}")
            except Exception as e:
                print(f"An unexpected error occurred while processing an entity: {str(e)}")

        elif entity.dxftype() in line_types:
            start_point = Point2D(entity.dxf.start.x, entity.dxf.start.y)
            end_point = Point2D(entity.dxf.end.x, entity.dxf.end.y)
            line = Line2D(start_point, end_point)
            polycurves.append((line, entity.dxf.layer))
    return polycurves


dxf_file_path = 'C:\\Users\\Jonathan\\Documents\\GitHub\\building.py\\library\\object_database\\DXF\\VBI Isolatieplaatvloer KVU320 Randoplegging I.dxf'
polycurves = fetch_polycurves(dxf_file_path)
plcrvs = []
for polycurve, layer in polycurves:
    print(f"Object on layer {layer}: {polycurve}")
    if polycurve != None:
        project.objects.append(polycurve)
        plcrvs.append(polycurve)


obj = Surface.by_patch_inner_and_outer(plcrvs)


original_cs = CoordinateSystem(Point(0,0,0),Vector3(1,0,0),Vector3(0,1,0),Vector3(0,0,1))

#create dict, (multi arrray).

print(original_cs)
# project.objects.append(obj)

# project.toSpeckle("7603a8603c")


# ifc_project = CreateIFC()

# ifc_project.add_project("My Project")
# ifc_project.add_site("My Site")
# ifc_project.add_building("Building A")
# ifc_project.add_storey("Ground Floor")
# ifc_project.add_storey("G2Floor")

# translateObjectsToIFC(project.objects, ifc_project)
# ifc_project.export("my_model.ifc")