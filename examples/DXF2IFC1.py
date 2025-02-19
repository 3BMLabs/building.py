import sys
import os
from ezdxf import readfile, DXFStructureError, DXFValueError


from project.fileformat import *
from geometry.curve import *
from abstract.vector import Point
from geometry.surface import *
from exchange.DXF import *
from exchange.IFC import *
from abstract.coordinatesystem import *


def process_entities(dxf_path, index, name):
    dxf_reader = ReadDXF(dxf_path).polylines
    only_polycurves = []
    for polycurve, layer in dxf_reader:
        if polycurve is not None:
            translated_polycurve = Polygon.translate(polycurve, Vector(0, index*1000, 0))
            only_polycurves.append(translated_polycurve)
            project.objects.append(translated_polycurve)
            print(f"{index}: Translated object on layer {layer}: {translated_polycurve}")
    srf = Surface.by_patch_inner_and_outer(only_polycurves)
    srf.name = name
    print(name)
    project.objects.append(srf)


def process_directory(dxf_directory):
    if os.path.isdir(dxf_directory):
        for index, filename in enumerate(os.listdir(dxf_directory)):
            if filename.lower().endswith('.dxf'):
                filepath = os.path.join(dxf_directory, filename)
                process_entities(filepath, index, filepath.split("\\")[-1].replace(".dxf", ""))
    elif os.path.isfile(dxf_directory) and dxf_directory.lower().endswith('.dxf'):
        process_entities(dxf_directory, 0, dxf_directory.split("\\")[-1].replace(".dxf", ""))
    else:
        print("Invalid directory or file path")

# dxf_input_path = 'Z:\\50_projecten\\6_3BM_LABS\\50_projecten\\001_Project Conda\\Aluminium kozijnen\\SL 38 Classic buitenopengaand\\'
dxf_input_path = 'library\\object_database\\DXF\\'

process_directory(dxf_input_path)
project.to_speckle("29a6c39880")

ifc_project = CreateIFC()

ifc_project.add_project("My Project")
ifc_project.add_site("My Site")
ifc_project.add_building("Building A")
ifc_project.add_storey("Ground Floor")
ifc_project.add_storey("G2Floor")


translateObjectsToIFC(project.objects, ifc_project)
ifc_project.export("BILT_Dictionary.ifc")