# -*- coding: utf8 -*-
# ***************************************************************************
# *   Copyright (c) 2024 Maarten Vroegindeweij & Jonathan van der Gouwe      *
# *   maarten@3bm.co.nl & jonathan@3bm.co.nl                                *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with this program; if not, write to the Free Software   *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************


"""This module provides tools for exporting geometry to Speckle
"""

__title__ = "revit"
__author__ = "Maarten"
__url__ = "./exchange/freecad.py"

import Part
import FreeCAD
from geometry.geometry2d import *
from geometry.curve import *


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
        ArchSiteObject = FreeCAD.ActiveDocument.Objects[lstObjects.index(
            SiteName)]
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
            curve = Part.Arc(Vector(i.start.x, i.start.y, 0), Vector(
                i.mid.x, i.mid.y, 0), Vector(i.end.x, i.end.y, 0))
            PartCurves.append(curve.toShape())
        elif i.__class__.__name__ == "Line2D":
            PartCurves.append(Part.makeLine(
                Vector(i.start.x, i.start.y, 0), Vector(i.end.x, i.end.y, 0)))
    aWire = Part.Wire(PartCurves)
    return aWire


def polycurve3d_to_part_wire(poly_curve_3d: PolyCurve):
    PartCurves = []
    for i in poly_curve_3d.curves:
        if i.__class__.__name__ == "Arc":
            curve = Part.Arc(Vector(i.start.x, i.start.y, i.start.z), Vector(
                i.mid.x, i.mid.y, i.mid.z), Vector(i.end.x, i.end.y, i.end.z))
            PartCurves.append(curve.toShape())
        elif i.__class__.__name__ == "Line":
            PartCurves.append(Part.makeLine(
                Vector(i.start.x, i.start.y, i.start.z), Vector(i.end.x, i.end.y, i.end.z)))
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
            test = "test"

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
