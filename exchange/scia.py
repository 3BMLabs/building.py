# -*- coding: utf8 -*-
# ***************************************************************************
# *   Copyright (c) 2023 Maarten Vroegindeweij & Jonathan van der Gouwe      *
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
__author__ = "Maarten & Jonathan"
__url__ = "./exchange/scia.py"


import sys
from pathlib import Path
import math
import xml.etree.ElementTree as ET

sys.path.append(str(Path(__file__).resolve().parents[2]))

from exchange.speckle import TransportToSpeckle, translateObjectsToSpeckleObjects
from geometry.point import Point
from geometry.curve import *
from abstract.vector import Vector3
from abstract.intersect2d import *
from abstract.plane import Plane
from abstract.text import Text
from abstract.intersect2d import Intersect2d
from objects.datum import *
from geometry.solid import Extrusion
from objects.panel import Panel
from abstract.color import Color
from geometry.surface import Surface
from packages.helper import *
from objects.frame import *
from objects.analytical import *
from project.fileformat import BuildingPy


class LoadXML:
    def __init__(self, filename=str, project=BuildingPy):
        self.filename = filename
        self.project = project
        self.unrecognizedElements = []
        
        self.root = self.load()
        if self.root != None:
            self.getStaaf()
            if len(self.unrecognizedElements) != 0:
                print(f"Unrecognized objects: {self.unrecognizedElements}")


    def load(self):
        try:
            tree = ET.parse(self.filename)
            root = tree.getroot()
            return root
        except Exception as e:
            print(e)
            return None


    def getAllKnoop(self):
        tableName = "EP_DSG_Elements.EP_StructNode.1"
        for container in self.root:
            for table in container:
                if table.attrib["t"] == tableName:
                    for obj in table:
                        if obj.tag == "{http://www.scia.cz}h":
                            for header in obj:
                                # print(header.attrib["t"])
                                pass
                        else:
                            pass
                            # print(obj.attrib["nm"])


    def findKnoop(self, name):
        tableName = "EP_DSG_Elements.EP_StructNode.1"
        for container in self.root:
            for table in container:
                if table.attrib["t"] == tableName:
                    for obj in table.iter("{http://www.scia.cz}obj"):
                        if obj.attrib["nm"] == name:
                            x, y, z = float(obj[1].attrib["v"])*self.project.scale, float(obj[2].attrib["v"])*self.project.scale, float(obj[3].attrib["v"])*self.project.scale
                            return Point(x,y,z)

    def convertJustification(self, justification):
        justification = justification.lower()
        if justification == "left":
            return "center", "left"
        elif justification == "right":
            return "center", "right"
        elif justification == "top":
            return "top", "center"
        elif justification == "bottom":
            return "bottom", "center"
        elif justification == "top left":
            return "top", "left"
        elif justification == "top right":
            return "top", "right"
        elif justification == "bottom left":
            return "bottom", "left"
        elif justification == "bottom right":
            return "bottom", "right"
        elif justification == "center" or justification == "midden" or justification == "centre":
            return "center", "center"
        else:
            print(f"Justification: [{justification}] not recognized")
            return "center", "center"

    def getStaaf(self):
        tableName = "EP_DSG_Elements.EP_Beam.1"
        h0 = "Naam"
        h1 = "Laag"
        h2 = "Loodrecht uitlijning"
        h3 = "LCS-rotatie"
        h3Index = None

        h4 = "Beginknoop"
        h4Index = None

        h5 = "Eindknoop"
        h5Index = None

        h6 = "Doorsnede"
        h6Index = None

        h7 = "EEM-type"

        h8 = "Staafsysteemlijn op"
        h8Index = None

        h9 = "ey"
        h9Index = None

        h10= "ez"
        h10Index = None

        h11 = "Tabel van geometrie"

        removeLayers = ["dummy"]

        for container in self.root:
            for table in container:
                if table.attrib["t"] == tableName:
                    for obj in table:
                        if obj.tag == "{http://www.scia.cz}h":
                            for index, header in enumerate(obj):
                                if header.attrib["t"] == h3:
                                    h3Index = index
                                if header.attrib["t"] == h4:
                                    h4Index = index
                                elif header.attrib["t"] == h5:
                                    h5Index = index
                                elif header.attrib["t"] == h6:
                                    h6Index = index
                                elif header.attrib["t"] == h8:
                                    h8Index = index
                                elif header.attrib["t"] == h9:
                                    h9Index = index
                                elif header.attrib["t"] == h10:
                                    h10Index = index
                        else:
                            rotationRAD = obj[h3Index].attrib["v"]
                            rotationDEG = (float(rotationRAD)*float(180) / math.pi)
                            # print(rotationDEG)
                            Yjustification, Xjustification = self.convertJustification(obj[h8Index].attrib["t"])
                            p1 = self.findKnoop(obj[h4Index].attrib["n"])
                            p2 = self.findKnoop(obj[h5Index].attrib["n"])

                            ey = float(obj[h9Index].attrib["v"]) * -1
                            ez = float(obj[h10Index].attrib["v"])

                            print(ey, ez)
                            
                            lineSeg = Line(start=p1, end=p2)
                            
                            elementType = (obj[h6Index].attrib["n"])
                            for removeLayer in removeLayers:
                                if removeLayer.lower() in elementType.lower():
                                    # print(f"[removeLayers]: {elementType}")
                                    pass
                                else:
                                    elementType = elementType.split("-")[1].strip()
                                    self.project.objects.append(lineSeg)
                                    # self.project.objects.append(Frame.byStartpointEndpointProfileName(p1, p2, elementType, elementType, BaseSteel))

                                    try:
                                        self.project.objects.append(Frame.byStartpointEndpointProfileNameJustifiction(p1, p2, elementType, elementType, Xjustification, Yjustification, rotationDEG, BaseSteel, ey, ez))                                        
                                    except Exception as e:
                                        if elementType not in self.unrecognizedElements:
                                            self.unrecognizedElements.append(elementType)
                                        print(e, elementType)