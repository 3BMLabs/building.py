# FreeCAD imports
import Draft
import Part
import Arch
import FreeCAD
from FreeCAD import Vector

# General imports
import sys, os, math
from pathlib import Path
import json
import urllib.request
import importlib

package_root_directory = "C:/Users/mikev/Documents/GitHub/building.py/"
sys.path.append(str(package_root_directory))

# Building Py Imports
from objects.frame import *
from objects.steelshape import *
from project.fileformat import *
from objects.datum import *
# from exchange.Freecad_Bupy import *
# importlib.reload(GIS2BIM_GUI)
# importlib.reload(GIS2BIM_FreeCAD)


project2 = BuildingPy("FreeCAD test", "0")
project2.round = False


def CreateLayer(layerName):
    layerName = layerName.replace(" ", "_")
    lstObjects = []
    for obj in FreeCAD.ActiveDocument.Objects:  # Check is layername already exists
        lstObjects.append(obj.Label)
    if not layerName in lstObjects:
        FreeCAD.activeDocument().addObject("App::DocumentObjectGroupPython", layerName)
    obj2 = FreeCAD.activeDocument().getObject(layerName)
    return obj2


def ArchSiteCreateCheck(SiteName):
    # Create an ArchSiteobject which is used to store data nessecary for GIS2BIM.
    lstObjects = []
    for obj in FreeCAD.ActiveDocument.Objects:  # Check is SiteObject already exists and fill parameters
        lstObjects.append(obj.Label)
    if SiteName in lstObjects:
        ArchSiteObject = FreeCAD.ActiveDocument.Objects[lstObjects.index(SiteName)]
    else:  # Create Siteobject and add parameters
        ArchSiteObject = Arch.makeSite([], [], SiteName)
        ArchSiteAddparameters(ArchSiteObject)

    return ArchSiteObject


def PlaceText(textData, fontSize, upper):
    Texts = []
    for i, j, k in zip(textData[0], textData[1], textData[2]):
        Z_Axis = FreeCAD.Vector(0, 0, 1)
        p1 = FreeCAD.Vector(i[0][0], i[0][1], 0)
        Place1 = FreeCAD.Placement(p1, FreeCAD.Rotation(Z_Axis, -float(j)))
        if upper:
            k = k.upper()
        else:
            k
        Text1 = Draft.makeText(k, point=p1)
        Text1.ViewObject.FontSize = fontSize
        Text1.Placement = Place1
        Texts.append(Text1)
    return Texts


def polycurve2d_to_part_wire(poly_curve_2d: PolyCurve2D):
    PartCurves = []
    for i in poly_curve_2d.curves:
        if i.__class__.__name__ == "Arc2D":
            curve = Part.Arc(Vector(i.start.x, i.start.y, 0), Vector(i.mid.x, i.mid.y, 0), Vector(i.end.x, i.end.y, 0))
            PartCurves.append(curve.toShape())
        elif i.__class__.__name__ == "Line2D":
            PartCurves.append(Part.makeLine(Vector(i.start.x, i.start.y, 0), Vector(i.end.x, i.end.y, 0)))
    aWire = Part.Wire(PartCurves)
    return aWire


def polycurve3d_to_part_wire(poly_curve_3d: PolyCurve):
    PartCurves = []
    for i in poly_curve_3d.curves:
        if i.__class__.__name__ == "Arc":
            curve = Part.Arc(Vector(i.start.x, i.start.y, i.start.z), Vector(i.mid.x, i.mid.y, i.mid.z),
                             Vector(i.end.x, i.end.y, i.end.z))
            PartCurves.append(curve.toShape())
        elif i.__class__.__name__ == "Line":
            PartCurves.append(Part.makeLine(Vector(i.start.x, i.start.y, i.start.z), Vector(i.end.x, i.end.y, i.end.z)))
    aWire = Part.Wire(PartCurves)
    return aWire


def wire_to_solid(wire, FCVector):
    p = Part.Face(wire)
    solid = p.extrude(FCVector)
    sld = Part.show(solid)


def Vector3ToFreeCADVector(vector3):
    vect = FreeCAD.Vector(vector3.x, vector3.y, vector3.z)
    return vect


def FrameToFreeCAD(frame):
    test2 = frame.curve3d
    vect = Vector3ToFreeCADVector(frame.directionVector)
    wire_to_solid(polycurve3d_to_part_wire(test2), vect)


def PointToFreeCADVector(Point):
    return FreeCAD.Vector(Point.x, Point.y, Point.z)


def LineToDraftLine(Line):
    p1 = PointToFreeCADVector(Line.start)
    p2 = PointToFreeCADVector(Line.end)
    return Draft.makeWire([p1, p2], False)


def translateObjectsToFreeCAD(Obj):
    FreeCADObj = []
    for i in Obj:
        nm = i.__class__.__name__
        if nm == 'Panel':
            test = "test"

        elif nm == 'Surface' or nm == 'Face':
            test = "test"

        elif nm == 'Frame':
            FreeCADObj.append(FrameToFreeCAD(i))

        elif nm == "Extrusion":
            test = "test"

        elif nm == 'PolyCurve':
            test = "test"

        elif nm == 'BoundingBox2d':
            test = "test"

        elif nm == 'ImagePyB':
            test = "test"

        elif nm == 'Interval':
            test = "test"

        elif nm == 'Line':
            FreeCADObj.append(LineToDraftLine(i))

        elif nm == 'Plane':
            test = "test"

        elif nm == 'Arc':
            test = "test"

        elif nm == 'Line2D':
            test = "test"

        elif nm == 'Point':
            test = "test"

        elif nm == 'Point2D':
            test = "test"

        elif nm == 'Grid':
            test = "test"

        elif nm == 'GridSystem':
            test = "test"

        else:
            print(f"{nm} Object not yet added to translateFreeCADObj")

    return FreeCADObj


names = [
    "HEA200",
    "HEB200",
    "HEM200",
    "IPE200",
    "200AA",
    "HD320/300",
    "DIN20",
    "DIE20",
    "DIL20",
    "DIR20",
    "UNP200",
    "Buis219.1/10",
    "INP200",
    "UPE200",
    "L200/200/16",
    "L200/100/10",
    "S100x15",
    "R50",
    "K200/200/10",
    "K200/100/10"
]

height = 2000
x = 0
y = 0
spacing = 2000
row = 5

rownumb = 0
rowcolum = 5
for i in names:
    if rownumb == rowcolum:
        rowcolum = rowcolum + 5
        y = y + spacing
        x = 0
    Mat = BaseSteel
    prof = i[:3]
    print(i)
    # fram = Frame.by_startpoint_endpoint_profile(Point(x, y, 0), Point(x, y+1, height), i, i, Mat).write(project2)
    x = x + spacing
    rownumb = rownumb + 1

fram = Frame.by_startpoint_endpoint_profile(Point(0, -1000, 0), Point(3000, -900, 0), "IPE600", "IPE600", Mat).write(
    project2)

Grid.by_startpoint_endpoint(Line(Point(100, 100, 0), Point(-5000, 10000, 0)), "Q").write(project2)


def toFreeCAD(self):
    translateObjectsToFreeCAD(self.objects)


toFreeCAD(project2)
