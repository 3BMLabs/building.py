# [included in BP singlefile]
# [!not included in BP singlefile - start]
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

sys.path.append(str(Path(__file__).resolve().parents[2]))

from abstract.node import *
from objects.shape3d import *
from objects.frame import *
from objects.analytical import *
from project.fileformat import BuildingPy

# [!not included in BP singlefile - end]
class Scia_Params:
    def __init__(self, id=str, name=str, layer=str, perpendicular_alignment=str, lcs_rotation=str, start_node=str, end_node=str, cross_section=str, eem_type=str, bar_system_line_on=str, ey=str, ez=str, geometry_table=str):
        self.id = id
        self.name = name
        self.layer = layer
        self.perpendicular_alignment = perpendicular_alignment
        self.lcs_rotation = lcs_rotation
        self.start_node = start_node
        self.end_node = end_node
        self.cross_section = cross_section
        self.eem_type = eem_type
        self.bar_system_line_on = bar_system_line_on
        self.ey = ey
        self.ez = ez
        self.geometry_table = geometry_table


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
                            pt = Point(x,y,z)
                            return pt

    def findKnoopNumber(self, name):
        tableName = "EP_DSG_Elements.EP_StructNode.1"
        for container in self.root:
            for table in container:
                if table.attrib["t"] == tableName:
                    for obj in table.iter("{http://www.scia.cz}obj"):
                        if obj.attrib["nm"] == name:
                            return obj.attrib["nm"]
                        

    def convertJustification(self, justification):
        justification = justification.lower()
        if justification == "left" or justification == "links":
            return "center", "right"
        elif justification == "right" or justification == "rechts":
            return "center", "left"
        elif justification == "top" or justification == "boven":
            return "top", "center"
        elif justification == "bottom" or justification == "onder":
            return "bottom", "center"
        elif justification == "top left" or justification == "linksboven":
            return "top", "right"
        elif justification == "top right" or justification == "rechtsboven":
            return "top", "left"
        elif justification == "bottom left" or justification == "linksonder":
            return "bottom", "right"
        elif justification == "bottom right" or justification == "rechtsonder":
            return "bottom", "left"
        elif justification == "center" or justification == "midden" or justification == "centre":
            return "center", "center"
        else:
            print(f"Justification: [{justification}] not recognized")
            return "center", "center"

    def structuralElementRecognision(self, tag):
        columnstrings = ["kolom", "column"]
        for columnstring in columnstrings:
            if columnstring.lower() in tag.lower():
                return "Column"
        return "Beam"


    def getStaaf(self):
        tableName = "EP_DSG_Elements.EP_Beam.1"

        h0 = "Naam"
        h0Index = None

        h1 = "Laag"
        h1Index = None

        h2 = "Loodrecht uitlijning"
        h2Index = None

        h3 = "LCS-rotatie"
        h3Index = None

        h4 = "Beginknoop"
        h4Index = None

        h5 = "Eindknoop"
        h5Index = None

        h6 = "Doorsnede"
        h6Index = None

        h7 = "EEM-type"
        h7Index = None

        h8 = "Staafsysteemlijn op"
        h8Index = None

        h9 = "ey"
        h9Index = None

        h10= "ez"
        h10Index = None

        h11 = "Tabel van geometrie"
        h11Index = None

        removeLayers = ["dummy"]

        for container in self.root:
            for table in container:
                if table.attrib["t"] == tableName:
                    for obj in table:
                        if obj.tag == "{http://www.scia.cz}h":
                            for index, header in enumerate(obj):
                                if header.attrib["t"] == h0:
                                    h0Index = index
                                if header.attrib["t"] == h1:
                                    h1Index = index
                                if header.attrib["t"] == h2:
                                    h2Index = index
                                if header.attrib["t"] == h3:
                                    h3Index = index
                                if header.attrib["t"] == h4:
                                    h4Index = index
                                if header.attrib["t"] == h5:
                                    h5Index = index
                                if header.attrib["t"] == h6:
                                    h6Index = index
                                if header.attrib["t"] == h7:
                                    h7Index = index
                                if header.attrib["t"] == h8:
                                    h8Index = index
                                if header.attrib["t"] == h9:
                                    h9Index = index
                                if header.attrib["t"] == h10:
                                    h10Index = index
                                if header.attrib["t"] == h11:
                                    h11Index = index
                            if h1Index == None:
                                print("Incorrect Scia XML Export Template")
                                sys.exit()
                        else:
                            #define here
                            comments = Scia_Params()
                            comments.id = str(obj.attrib["id"])
                            comments.name = str(obj[h0Index].attrib["v"])
                            comments.layer = str(obj[h1Index].attrib["n"])
                            comments.perpendicular_alignment = str(obj[h2Index].attrib["t"])
                            comments.lcs_rotation = str(obj[h3Index].attrib["v"])
                            comments.start_node = str(obj[h4Index].attrib["n"])
                            comments.end_node = str(obj[h5Index].attrib["n"])
                            comments.cross_section = str(obj[h6Index].attrib["n"])
                            comments.eem_type = str(obj[h7Index].attrib["t"])
                            comments.bar_system_line_on = str(obj[h8Index].attrib["t"])
                            comments.ey = str(obj[h9Index].attrib["v"])
                            comments.ez = str(obj[h10Index].attrib["v"])
                            comments.geometry_table = str(obj[h11Index].attrib["t"])

                            rotationRAD = obj[h3Index].attrib["v"]
                            rotationDEG = (float(rotationRAD)*float(180) / math.pi) * -1
                            # print(rotationDEG)
                            Yjustification, Xjustification = self.convertJustification(obj[h8Index].attrib["t"])
                            p1 = self.findKnoop(obj[h4Index].attrib["n"])
                            p1Number = self.findKnoopNumber(obj[h4Index].attrib["n"])
                            p2 = self.findKnoop(obj[h5Index].attrib["n"])
                            p2Number = self.findKnoopNumber(obj[h5Index].attrib["n"])
                            #TEMP
                            p1 = Point(p1.x-0.00000000001, p1.y, p1.z)

                            node1 = Node()
                            node1.number = p1Number
                            node1.point = p1
                            self.project.objects.append(node1)
                            # print(node1)

                            node2 = Node()
                            node2.point = p2
                            node2.number = p2Number
                            self.project.objects.append(node2)

                            ey = float(obj[h9Index].attrib["v"]) * -project.scale
                            ez = float(obj[h10Index].attrib["v"]) * project.scale
                            
                            lineSeg = Line(start=p1, end=p2)
                            
                            layerType = self.structuralElementRecognision(obj[h1Index].attrib["n"])

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
                                        if node1.x == node2.x:
                                            node2 = Node(node2.x,node2.y+0.000001,node2.z)
                                        self.project.objects.append(Frame.byStartpointEndpointProfileNameJustifiction(node1, node2, elementType, elementType, Xjustification, Yjustification, rotationDEG, BaseSteel, ey, ez, layerType, comments))                                        
                                    except Exception as e:
                                        if elementType not in self.unrecognizedElements:
                                            self.unrecognizedElements.append(elementType)
                                        print(e, elementType)