import sys
import os
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
from objects.frame import *

def process_entities(dxf_path, index):
    dxf_reader = ReadDXF(dxf_path).polylines
    only_polycurves = []
    for polycurve, layer in dxf_reader:
        if polycurve is not None:
            translated_polycurve = Polygon.translate(polycurve, Vector3(0, index*1000, 0))
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

# dxf_input_path = 'Z:\\50_projecten\\6_3BM_LABS\\50_projecten\\001_Project Conda\\Aluminium kozijnen\\SL 38 Classic buitenopengaand\\'
# dxf_input_path = 'C:\\Users\\Jonathan\\Documents\\GitHub\\building.py\\library\\object_database\\DXF\\'

# dxf_input_path = 'C:\\Users\\Jonathan\\Documents\\GitHub\\building.py\\library\\object_database\\DXF\\VBI Isolatieplaatvloer K200 Standaard.dxf'

# process_directory(dxf_input_path)

kozijnstijl = "Z:\\50_projecten\\6_3BM_LABS\\50_projecten\\001_Project Conda\\002 Aluminium kozijnen\\SL 38 Classic binnenopengaand\\Reynaers Aluminium buitenkader SL 38 Classic Bi draai.dxf"
kozijnprofiel = ReadDXF(kozijnstijl).polylines[0][0]
kozijnstijl1 = "Z:\\50_projecten\\6_3BM_LABS\\50_projecten\\001_Project Conda\\002 Aluminium kozijnen\\SL 38 Classic binnenopengaand\\Reynaers Aluminium T-profiel SL 38 Classic Bi vast.dxf"
kozijnprofiel1 = ReadDXF(kozijnstijl1).polylines[0][0]

c_profile = PolyCurve2D.by_points([Point2D(-50,-50), Point2D(-50,50), Point2D(50,50), Point2D(0,-25), Point2D(50,-50)])

# print(j)
# sys.exit()

start_list = [Point(0,0,0),Point(0,0,3000),Point(1500,0,3000),Point(1500,0,0)]
end_list = [Point(0,0,3000),Point(1500,0,3000),Point(1500,0,0),Point(0,0,0)]
profile_name = "HEA100"


# for start, end in zip(start_list, end_list):
#     frame1 = Frame.by_startpoint_endpoint_profile(start, end, kozijnprofiel, "None", BaseSteel)
#     project.objects.append(frame1)

onderdorpel = Line(Point(0,0,0), Point(0,900,0))
onderdorpel_profiel = kozijnprofiel
project.objects.append(Frame.by_startpoint_endpoint_profile(onderdorpel.start, onderdorpel.end, onderdorpel_profiel, "None", BaseSteel))

linkerstijl = Line(Point(0,-99,-99), Point(0,-99,2400))
linkerstijl_profiel = kozijnprofiel
project.objects.append(Frame.by_startpoint_endpoint_profile(linkerstijl.start, linkerstijl.end, linkerstijl_profiel, "None", BaseSteel))

bovendorpel = Line(Point(0,0,2483.1), Point(0,900,2483.1))
bovendorpel_profiel = kozijnprofiel
project.objects.append(Frame.by_startpoint_endpoint_profile(bovendorpel.start, bovendorpel.end, bovendorpel_profiel, "None", BaseSteel))

bovendorpel = Line(Point(0,999,2400), Point(0,999,-99))
bovendorpel_profiel = kozijnprofiel1
project.objects.append(Frame.by_startpoint_endpoint_profile(bovendorpel.start, bovendorpel.end, bovendorpel_profiel, "None", BaseSteel))


project.objects.append(Frame.by_startpoint_endpoint_profile_justifiction(bovendorpel.start, bovendorpel.end, bovendorpel_profiel, "Name", "center", "center", 0, BaseSteel, 0, 0))

project.toSpeckle("7603a8603c")

# ifc_project = CreateIFC()

# ifc_project.add_project("My Project")
# ifc_project.add_site("My Site")
# ifc_project.add_building("Building A")
# ifc_project.add_storey("Ground Floor")
# ifc_project.add_storey("G2Floor")

# translateObjectsToIFC(project.objects, ifc_project)

# ifc_project.export("Single_Obj2.ifc")