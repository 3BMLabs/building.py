import sys
import os
from ezdxf import readfile, DXFStructureError, DXFValueError


from project.fileformat import *
from geometry.curve import *
from geometry.point import Point

from geometry.surface import *
from exchange.DXF import *
from exchange.IFC import *
from abstract.coordinatesystem import *
from construction.beam import *

def process_entities(dxf_path, index):
    dxf_reader = ReadDXF(dxf_path).polylines
    only_polycurves = []
    for polycurve, layer in dxf_reader:
        if polycurve is not None:
            translated_polycurve = Polygon.translate(polycurve, Vector(0, index*1000, 0))
            only_polycurves.append(translated_polycurve)
            project.objects.append(translated_polycurve)
            print(f"{index}: Translated object on layer {layer}: {translated_polycurve}")
    project.objects.append(Surface.by_patch_inner_and_outer(only_polycurves))


def process_directory(dxf_directory):
    if os.path.isdir(dxf_directory):
        for index, filename in enumerate(os.listdir(dxf_directory)):
            if filename.lower().endswith('.dxf'):
                filepath = os.path.join(dxf_directory, filename)
                process_entities(filepath, index)
    elif os.path.isfile(dxf_directory) and dxf_directory.lower().endswith('.dxf'):
        process_entities(dxf_directory, 0)
    else:
        print("Invalid directory or file path")

# kozijnstijl = "Z:\\50_projecten\\6_3BM_LABS\\50_projecten\\001_Project Conda\\002 Aluminium kozijnen\\SL 38 Classic binnenopengaand\\Reynaers Aluminium buitenkader SL 38 Classic Bi draai.dxf"
# kozijnprofiel = ReadDXF(kozijnstijl).polylines[0][0]
# kozijnstijl1 = "Z:\\50_projecten\\6_3BM_LABS\\50_projecten\\001_Project Conda\\002 Aluminium kozijnen\\SL 38 Classic binnenopengaand\\Reynaers Aluminium T-profiel SL 38 Classic Bi vast.dxf"
# kozijnprofiel1 = ReadDXF(kozijnstijl1).polylines[0][0]

c_profile = PolyCurve.by_points([Point(-50,-50), Point(-50,50), Point(50,50), Point(0,-25), Point(50,-50)])

start_list = [Point(0,0,0),Point(0,0,3000),Point(1500,0,3000),Point(1500,0,0)]
end_list = [Point(0,0,3000),Point(1500,0,3000),Point(1500,0,0),Point(0,0,0)]
profile_name = "HEA100"

project.objects.append(Beam.by_startpoint_endpoint_profile_justifiction(Point(0,0,0), Point(2000,0,0), c_profile, "Name", "center", "center", 0, BaseSteel, 0, 0))
project.objects.append(Beam.by_startpoint_endpoint_profile_justifiction(Point(0,0,0), Point(2000,0,0), c_profile, "Name", "left", "top", 0, BaseSteel, 0, 0))

project.to_speckle("7603a8603c")

project.to_IFC("BILT")