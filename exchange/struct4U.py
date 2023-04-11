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


"""This module provides an exchange with XFEM4U
"""

__title__ = "XFEM4U"
__author__ = "Maarten & Jonathan"
__url__ = "./exchange/struct4U.py"

import xml.etree.ElementTree as ET
from geometry.curve import *
from exchange.speckle import *
from objects.panel import *


# TODO Line to Grid Object
# TODO Grid Object with building.py line --> convert to Speckle Line with pattern

def rgb_to_int(rgb):
    r, g, b = [max(0, min(255, c)) for c in rgb]

    return (255 << 24) | (r << 16) | (g << 8) | b


def getXYZ(XMLtree, nodenumber):
    root = XMLtree.getroot()
    # POINTS
    n = root.findall(".//Nodes/Number")
    nodenumbers = []

    for i in n:
        nodenumbers.append(i.text)
    # Search
    rest = nodenumbers.index(nodenumber)
    return (rest)


def XMLImportNodes(XMLtree):
    root = XMLtree.getroot()
    # POINTS
    n = root.findall(".//Nodes/Number")
    nodenumbers = []

    for i in n:
        nodenumbers.append(i.text)
    X = root.findall(".//Nodes/X")
    Y = root.findall(".//Nodes/Y")
    Z = root.findall(".//Nodes/Z")

    XYZ = []
    # Put points in 3D
    for h, i, j, k in zip(n, X, Y, Z):
        Pnt = Point(float(i.text.replace(",", ".")), float(j.text.replace(",", ".")), float(k.text.replace(",", ".")))
        # Pnt.id = int(h.text)
        XYZ.append(Pnt)
    return nodenumbers, XYZ


def XMLImportgetGridDistances(Grids):
    # Function to create grids from the format 0, 4x5400, 4000, 4000 to absolute XYZ-values
    GridsNew = []
    distance = 0.0
    # GridsNew.append(distance)
    for i in Grids:
        # del Grids[0]
        if "x" in i:
            spl = i.split("x")
            count = int(spl[0])
            width = float(spl[1])
            for i in range(count):
                distance = distance + width
                GridsNew.append(distance)
        else:
            distance = distance + float(i)
            GridsNew.append(distance)
    return GridsNew


def XMLImportGrids(XMLtree, gridExtension):
    # create building.py Grids from the grids of XFEM4U
    root = XMLtree.getroot()
    gridlines = []

    # GRIDS
    GridEx = gridExtension

    GridsX = root.findall(".//Grids/X")[0].text.split()
    GridsX = XMLImportgetGridDistances(GridsX)
    Xmax = max(GridsX)
    GridsXLable = root.findall(".//Grids/X_Lable")[0].text.split()
    GridsY = root.findall(".//Grids/Y")[0].text.split()
    GridsY = XMLImportgetGridDistances(GridsY)
    Ymax = max(GridsY)
    GridsYLable = root.findall(".//Grids/Y_Lable")[0].text.split()
    GridsZ = root.findall(".//Grids/Z")[0].text.split()
    GridsZ = XMLImportgetGridDistances(GridsZ)
    GridsZLable = root.findall(".//Grids/Z_Lable")[0].text.split()
    Zmax = max(GridsZ)

    grids = []
    for i in GridsX:
        grids.append(Line(Point(i, -GridEx, 0), Point(i, Ymax + GridEx, 0)))

    for i in GridsY:
        grids.append(Line(Point(-GridEx, i, 0), Point(Xmax + GridEx, i, 0)))

    for i in GridsZ:
        grids.append(Line(Point(0, 0, i), Point(0, Xmax, i)))

    # for i in grids:
    #   line = LineToSpeckleLine(i) #Grid to SpeckleLine
    #   gridlines.append(line)
    return grids


# def findMaterial(material):


def XMLImportPlates(XMLtree):
    # Get platedata from XML
    root = XMLtree.getroot()
    # PLATES

    platesNumbersElem = root.findall(".//Plates/Number")
    PlatesNodesElem = root.findall(".//Plates/Node")
    platesMaterialElem = root.findall(".//Plates/Material")
    platesZElem = root.findall(".//Plates/Z")
    platesThicknessElem = root.findall(".//Plates/h")
    platesTop_Center_BottomElem = root.findall(".//Plates/Top_Center_Bottom")

    platesNumbers = []
    for i in platesNumbersElem: platesNumbers.append(i.text)
    PlatesNodes = []
    for i in PlatesNodesElem: PlatesNodes.append(i.text)
    platesMaterialQuality = []
    for i in platesMaterialElem:
        platesMaterialQuality.append(i.text)
    platesMaterial = []
    lstConcrete = ["C20/25", "C25/30", "C30/37", "C35/45", "C40/50", "C45/55", "C50/60", "C53/65"]
    lstTimber = ["C14", "C16", "C18", "C20", "C22", "C24", "C27", "C30", "C35", "C40", "C50", "D18", "D24", "D30",
                 "D35", "D40", "D50", "D60", "D70"]
    lstSteel = ["S235,S275,S355"]
    lstColor = []
    for i in platesMaterialQuality:
        if i in lstConcrete:
            platesMaterial.append("Concrete")
            lstColor.append(rgb_to_int([192, 192, 192]))
        elif i in lstTimber:
            platesMaterial.append("Timber")
            lstColor.append(rgb_to_int([191, 159, 116]))
        elif i in lstSteel:
            platesMaterial.append("Steel")
            lstColor.append(rgb_to_int([237, 28, 36]))
        else:
            platesMaterial.append("Other")
            lstColor.append(rgb_to_int([150, 150, 150]))
    platesZ = []
    for i in platesZElem: platesZ.append(float(i.text))
    platesThickness = []
    for i in platesThicknessElem: platesThickness.append(float(i.text))
    platesTop_Center_Bottom = []
    for i in platesTop_Center_BottomElem: platesTop_Center_Bottom.append(i.text)

    # for loop to get each element in an array
    plateOffsets = []
    # Plate ligt standaard in de hartlijn. In het onderstaande is dit aangepast.
    for i, j, k in zip(platesZ, platesThickness, platesTop_Center_Bottom):
        if k == "Top":
            offset = -0.5 * j
        elif k == "Center":
            offset = 0
        elif k == "Bottom":
            offset = 0.5 * j
        else:
            offset = 0
        offset = offset + j
        plateOffsets.append(offset)

    rootPlates = root.findall(".//Plates")

    # XMLImportPlates(root):
    PlatesTags = []
    PlatesValues = []
    for elements in root:
        if elements.tag == "Plates":
            for element in elements:
                PlatesTags.append(element.tag)
                PlatesValues.append(element.text)

    # Iedere plate met nodes in een sublijst stoppen
    # plate
    # nodes

    ind = [i for i, x in enumerate(PlatesTags) if x == "Number"]  # indices where a new plate starts.

    platesIndices = []
    platesValues = []
    platesNodes = []
    count = 0
    for x in ind:
        count = count + 1
        try:
            platesIndices.append(PlatesTags[x:ind[count]])
            platesValues.append(PlatesValues[x:ind[count]])
            platesNodes.append(PlatesValues[x + 1:ind[count] - 5])
        except:
            platesIndices.append(PlatesTags[x::])  # voor de laatste item uit de lijst, anders out of range
            platesValues.append(PlatesValues[x::])  # voor de laatste item uit de lijst, anders out of range
            platesNodes.append(PlatesValues[x + 1:-5])

    obj = []
    XYZ = XMLImportNodes(XMLtree)[1]  # Knopen

    platesPolyCurves = []
    for i in platesNodes:
        PlatePoints = []
        for j in i:
            Point = XYZ[getXYZ(XMLtree, j)]
            PlatePoints.append(Point)
        PlatePoints.append(PlatePoints[0])
        ply = PolyCurve.byPoints(PlatePoints)
        # obj.append(ply)
        platesPolyCurves.append(ply)

    # Panels maken Building.py
    Panels = []

    for i, j, k, l, m, n in zip(platesPolyCurves, platesThickness, plateOffsets, platesMaterial, platesNumbers,
                                lstColor):
        Panels.append(Panel.byPolyCurveThickness(i, j, k, l + m, n))

    return Panels


class xmlXFEM4U:
    def __init__(self):
        self.Frame1 = "<Frame>\n"
        self.Project = "<ProjectName>" + "Building.py" + "</ProjectName>\n"
        self.ProjectNumber = "<ProjectNumber>0</ProjectNumber>\n"
        self.ExportDate = "<ExportDateTime>2023-04-08 19:55:39Z</ExportDateTime>\n"
        self.XMLVersion = "<XMLExportVersion>v4.0.30319</XMLExportVersion>\n"  #
        self.Nodes = "<Nodes></Nodes>\n"
        self.Supports = "<Supports></Supports>\n"
        self.Grids = "<Grids><X>0 5000</X><X_Lable>A B C D E F G H I J K L M N O P Q R S T U V W X Y Z AA AB AC</X_Lable><Y>0 5000</Y><Y_Lable>1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24</Y_Lable><Z>0</Z><Z_Lable>+0</Z_Lable></Grids>\n"
        self.Profiles = "<Profiles></Profiles>\n"
        self.Beamgroup = "<Beamgroup></Beamgroup>\n"
        self.Beams = "<Beams></Beams>\n"
        self.Panels = "<Panels></Panels>\n"
        self.Plates = "<Plates></Plates>\n"
        self.LoadCases = "<LoadCases></LoadCases>\n"
        self.BeamLoads = "<BeamLoads></BeamLoads>\n"
        self.NodeLoads = "<NodeLoads></NodeLoads>\n"
        self.SurfaceLoads = "<SurfaceLoads></SurfaceLoads>\n"
        self.Combinations = "<Combinations></Combinations>\n"
        self.RebarLongitudinal = "<RebarLongitudinal></RebarLongitudinal>\n"
        self.RebarStirrup = "<RebarStirrup></RebarStirrup>\n"
        self.Layers = "<Layers><Layer_number>1</Layer_number><Layer_description>Layer 1</Layer_description></Layers>\n"
        self.Frame2 = "</Frame>\n"
        self.xmlstr = None

    def addBeamsPlates(self, buildingpyobj):
        obj = buildingpyobj
        # Number of nodes:
        n = 0
        Nodes = []
        Plates = []
        Beams = []
        Beamgroup = []
        Profiles = []
<<<<<<< Updated upstream
        Supports= []
=======
        Supports = []
>>>>>>> Stashed changes
        plateN = 0  # Numbering plates
        beamsN = 0  # Numbering beams
        beamsGN = 0  # Numbering beamgroup
        profN = 0  # Numbering profiles
<<<<<<< Updated upstream
        supportN = 0 # Numbering of supports
=======
        supportN = 0 # Numbering supports

>>>>>>> Stashed changes
        Nodes.append("<Nodes>\n")
        Plates.append("<Plates>\n")
        Beams.append("<Beams>\n")
        Beamgroup.append("<Beamgroup>\n")
        Profiles.append("<Profiles>\n")
        Supports.append("<Supports>\n")

        ProfileNames = []  # all profiles
        for i in obj:
            nm = i.__class__.__name__
            if nm == "Frame":
                ProfileNames.append(i.profileName)

        ProfileNamesUnique = []  # Unique profiles
        for item in ProfileNames:
            if item not in ProfileNamesUnique:
                ProfileNamesUnique.append(item)

        for i in ProfileNamesUnique:
            profN = profN + 1
            Profiles.append("<Number>" + str(profN) + "</Number>\n")
            Profiles.append("<Profile_name>" + i + "</Profile_name>\n")
            Profiles.append("<Material_type>" + "0" + "</Material_type>\n")
            Profiles.append("<Material>" + "S235" + "</Material>\n")
            # if i.material.name == "BaseSteel":
            #    Profiles.append("<Material_type>" + "0" + "</Material_type>")
            #    Profiles.append("<Material>" + "S235" + "</Material>")
            # else:
            #    Profiles.append("<Material_type>" + "0" + "</Material_type>")
            #    Profiles.append("<Material>" + "S235" + "</Material>")
            Profiles.append("<Angle>" + "0" + "</Angle>\n")

        for i in obj:
            nm = i.__class__.__name__
            if nm == 'Panel':
                plateN = plateN + 1
                Plates.append("<Number>" + str(plateN) + "</Number>\n")
                for j in i.origincurve.points:
                    n = n + 1
                    Nodes.append("<Number>" + str(n) + "</Number>\n")
                    Nodes.append("<X>" + str(round(j.x)) + "</X>\n")
                    Nodes.append("<Y>" + str(round(j.y)) + "</Y>\n")
                    Nodes.append("<Z>" + str(round(j.z)) + "</Z>\n")
                    Plates.append("<Node>" + str(n) + "</Node>\n")
                Plates.append("<h>" + str(i.thickness) + "</h>\n")
                Plates.append(
                    "<Material_type>" + "c9a5876f475cefab7cc11281b017914a1" + "</Material_type>\n")  # material nog uitlezen
                Plates.append("<Material>" + "C20/25" + "</Material>\n")  # material nog uitlezen
                Plates.append("<Z>" + "0" + "</Z>\n")
                Plates.append("<Top_Center_Bottom>" + "Center" + "</Top_Center_Bottom>\n")

            elif nm == 'Frame':
                ProfN = ProfileNamesUnique.index(i.profileName) + 1
                beamsGN = beamsGN + 1
                Beamgroup.append("<Number>" + str(beamsGN) + "</Number>\n")

                n = n + 1
                Nodes.append("<Number>" + str(n) + "</Number>\n")
                Nodes.append("<X>" + str(round(i.start.x)) + "</X>\n")
                Nodes.append("<Y>" + str(round(i.start.y)) + "</Y>\n")
                Nodes.append("<Z>" + str(round(i.start.z)) + "</Z>\n")
                Beamgroup.append("<Startnode>" + str(n) + "</Startnode>\n")

                beamsN = beamsN + 1
                Beams.append("<Number>" + str(beamsN) + "</Number>")
                Beams.append("<Beamgroupnumber>" + str(beamsGN) + "</Beamgroupnumber>\n")
                Beams.append("<From_node_number>" + str(n) + "</From_node_number>\n")

                n = n + 1
                Nodes.append("<Number>" + str(n) + "</Number>\n")
                Nodes.append("<X>" + str(round(i.end.x)) + "</X>\n")
                Nodes.append("<Y>" + str(round(i.end.y)) + "</Y>\n")
                Nodes.append("<Z>" + str(round(i.end.z)) + "</Z>\n")

                Beamgroup.append("<Endnode>" + str(n) + "</Endnode>\n")

                Beams.append("<To_node_number>" + str(n) + "</To_node_number>\n")
                Beams.append("<Angle>" + str(i.rotation) + "</Angle>\n")
                Beams.append("<Angle_profile>" + "0" + "</Angle_profile>\n")
                ProfNstr = str(ProfN)
                Beams.append("<Profile_number>" + ProfNstr + "</Profile_number>\n")
                Beams.append("<Z>" + str(i.ZOffset) + "</Z>\n")
                Beams.append("<Top_Center_Bottom>" + i.YJustification + "</Top_Center_Bottom>\n")
            elif nm == 'Grid':
                pass
<<<<<<< Updated upstream
        for i in obj:
            nm = i.__class__.__name__
            if nm == 'Support':
                supportN = supportN = 1
                n = n + 1
                Nodes.append("<Number>" + str(n) + "</Number>\n")
                Nodes.append("<X>" + str(round(i.end.x)) + "</X>\n")
                Nodes.append("<Y>" + str(round(i.end.y)) + "</Y>\n")
                Nodes.append("<Z>" + str(round(i.end.z)) + "</Z>\n")

                Supports.append("<Number>" + str(supportN) + "</Number>")
                Supports.append("<Nodenumber>" + str(n) + "</Nodenumber>")
                Supports.append("<Tx>" + self.Tx + "</Tx>")
                Supports.append("<Ty>" + self.Ty + "</Ty>")
                Supports.append("<Tz>" + self.Tz + "</Tz>")
                Supports.append("<Rx>" + self.Rx + "</Rx>")
                Supports.append("<Ry>" + self.Ry + "</Ry>")
                Supports.append("<Rz>" + self.Rz + "</Rz>")
                Supports.append("<Kx>" + str(self.Kx) + "</Kx>")
                Supports.append("<Ky>" + str(self.Ky) + "</Ky>")
                Supports.append("<Kz>" + str(self.Kz) + "</Kz>")
                Supports.append("<Cx>" + str(self.Cx) + "</Cx>")
                Supports.append("<Cy>" + str(self.Cy) + "</Cy>")
                Supports.append("<Cz>" + str(self.Cz) + "</Cz>")
                Supports.append("<dx>" + str(self.dx) + "</dx>")
                Supports.append("<dy>" + str(self.dy) + "</dy>")
                Supports.append("<dz>" + str(self.dz) + "</dz>")

            else:
                pass


=======

        for i in obj:
            nm = i.__class__.__name__
            if nm == 'Support':
                supportN = supportN + 1
                Supports.append("<Number>" + str(supportN) + "</Number>\n")
                n = n + 1 #nodenumber
                Supports.append("<Nodenumber>" + str(n) + "</Nodenumber>\n")
                Supports.append("<Tx>" + i.Tx + "</Tx>\n")
                Supports.append("<Ty>" + i.Ty + "</Ty>\n")
                Supports.append("<Tz>" + i.Tz + "</Tz>\n")
                Supports.append("<Rx><" + i.Rx + "/Rx>\n")
                Supports.append("<Ry>" + i.Ry + "</Ry>\n")
                Supports.append("<Rz>" + i.Rz + "</Rz>\n")
                Supports.append("<Kx>" + str(i.Kx) + "</Kx>\n")
                Supports.append("<Ky>" + str(i.Ky) + "</Ky>\n")
                Supports.append("<Kz>" + str(i.Kz) + "</Kz>\n")
                Supports.append("<Cx>" + str(i.Cx) + "</Cx>\n")
                Supports.append("<Cy>" + str(i.Cy) + "</Cy>\n")
                Supports.append("<Cz>" + str(i.Cz) + "</Cz>\n")
                Supports.append("<dx>" + str(i.dx) + "</dx>\n")
                Supports.append("<dy>" + str(i.dy) + "</dy>\n")
                Supports.append("<dz>" + str(i.dz) + "</dz>\n")
                Nodes.append("<Number>" + str(n) + "</Number>\n")
                Nodes.append("<X>" + str(round(i.Point.x)) + "</X>\n")
                Nodes.append("<Y>" + str(round(i.Point.y)) + "</Y>\n")
                Nodes.append("<Z>" + str(round(i.Point.z)) + "</Z>\n")
            else:
                pass

>>>>>>> Stashed changes
        Nodes.append("</Nodes>\n")
        Plates.append("</Plates>\n")
        Beams.append("</Beams>\n")
        Profiles.append("</Profiles>\n")
        Beamgroup.append("</Beamgroup>\n")
        Supports.append("</Supports>\n")

        self.Nodes = ''.join(str(N) for N in Nodes)
        self.Plates = ''.join(str(P) for P in Plates)
        self.Beams = ''.join(str(B) for B in Beams)
        self.Beamgroup = ''.join(str(BP) for BP in Beamgroup)
        self.Profiles = ''.join(str(Pr) for Pr in Profiles)
        self.Supports = ''.join(str(Sup) for Sup in Supports)

    def addGrids(self, spacX, seqX, spacY, seqY, z):
        self.Grids = "<Grids>" + "<X>" + spacX + "</X>" + "<X_Lable>" + seqX + "</X_Lable>" + "<Y>" + spacY + "</Y>" + "<Y_Lable>" + seqY + "</Y_Lable>" + "<Z>" + "0 " + str(
            z) + "</Z>" + "<Z_Lable>" + "+0 h" + "</Z_Lable>" + "</Grids>"

    def addLoadCasesCombinations(self):
        # Load Cases
        LoadCases = []
        LoadCases.append("<Number>1</Number>")
        LoadCases.append("<Description>Permanent</Description>")
        LoadCases.append("<Type>0</Type>")
        LoadCases.append("<psi0>1</psi0>")
        LoadCases.append("<psi1>1</psi1>")
        LoadCases.append("<psi2>1</psi2>")
        LoadCases.append("<Number>2</Number>")
        LoadCases.append("<Description>Veranderlijk</Description>")
        LoadCases.append("<Type>1</Type>")
        LoadCases.append("<psi0>0,4</psi0>")
        LoadCases.append("<psi1>0,5</psi1>")
        LoadCases.append("<psi2>0,3</psi2>")

        # Load Combinations
        Combinations = []
        Combinations.append("<Combinations>")
        Combinations.append("<LoadCombinationNumber>1</LoadCombinationNumber>")
        Combinations.append("<Description>Dead")
        Combinations.append("load</Description>")
        Combinations.append("<CombTyp>0</CombTyp>")
        Combinations.append("<Case>1</Case>")
        Combinations.append("<Psi>1</Psi>")
        Combinations.append("<Gamma>1, 35</Gamma>")
        Combinations.append("<Case>2</Case>")
        Combinations.append("<Psi>1</Psi>")
        Combinations.append("<Gamma>1, 5</Gamma>")
        Combinations.append("<LoadCombinationNumber>2</LoadCombinationNumber>")
        Combinations.append("<Description>Live")
        Combinations.append("load</Description>")
        Combinations.append("<CombTyp>0</CombTyp>")
        Combinations.append("<Case>1</Case>")
        Combinations.append("<Psi>1</Psi>")
        Combinations.append("<Gamma>1, 2</Gamma>")
        Combinations.append("<Case>2</Case>")
        Combinations.append("<Psi>1</Psi>")
        Combinations.append("<Gamma>1, 5</Gamma>")
        Combinations.append("<LoadCombinationNumber>3</LoadCombinationNumber>")
        Combinations.append("<Description>Dead")
        Combinations.append("load</Description>")
        Combinations.append("<CombTyp>3</CombTyp>")
        Combinations.append("<Case>1</Case>")
        Combinations.append("<Psi>1</Psi>")
        Combinations.append("<Gamma>1</Gamma>")
        Combinations.append("<Case>2</Case>")
        Combinations.append("<Psi>1</Psi>")
        Combinations.append("<Gamma>1</Gamma>")
        Combinations.append("<LoadCombinationNumber>4</LoadCombinationNumber>")
        Combinations.append("<Description>Live")
        Combinations.append("load</Description>")
        Combinations.append("<CombTyp>3</CombTyp>")
        Combinations.append("<Case>1</Case>")
        Combinations.append("<Psi>1</Psi>")
        Combinations.append("<Gamma>1</Gamma>")
        Combinations.append("<Case>2</Case>")
        Combinations.append("<Psi>1</Psi>")
        Combinations.append("<Gamma>1</Gamma>")
        Combinations.append("<LoadCombinationNumber>5</LoadCombinationNumber>")
        Combinations.append("<Description>SLS")
        Combinations.append("Permanent</Description>")
        Combinations.append("<CombTyp>4</CombTyp>")
        Combinations.append("<Case>1</Case>")
        Combinations.append("<Psi>1</Psi>")
        Combinations.append("<Gamma>1</Gamma>")
        Combinations.append("<LoadCombinationNumber>6</LoadCombinationNumber>")
        Combinations.append("<Description>SLS")
        Combinations.append("Quasi - permanent</Description>")
        Combinations.append("<CombTyp>2</CombTyp>")
        Combinations.append("<Case>1</Case>")
        Combinations.append("<Psi>1</Psi>")
        Combinations.append("<Gamma>1</Gamma>")
        Combinations.append("<Case>2</Case>")
        Combinations.append("<Psi>0, 8</Psi>")
        Combinations.append("<Gamma>1</Gamma>")
        Combinations.append("</Combinations>")
        self.Combinations = ''.join(str(LC) for LC in Combinations)

<<<<<<< Updated upstream
    def addSurfaceLoad(self,obj):
        nm = i.__class__.__name__
        SurfaceLoads = []
        SurfaceLoads.append("<SurfaceLoads>")
        slN = 0
        for i in obj:
            slN = slN + 1
            if nm == "SurfaceLoad":
                SurfaceLoads.append("<Number>" + str(n) + "</Number>")
                SurfaceLoads.append("<LoadCaseNumber>" + str(i.LoadCase) + "</LoadCaseNumber>")
                SurfaceLoads.append("<Description>" + i.Description + "</Description>")
                for j in i.PolyCurve.points:
                    SurfaceLoads.append("<NodeX>" + str(j.X) + "</NodeX>")
                    SurfaceLoads.append("<NodeY>" + str(j.Y) + "</NodeY>")
                    SurfaceLoads.append("<NodeZ>" + str(j.Z) + "</NodeZ>")
                SurfaceLoads.append("<Coordinate_system>" + i.crs + "</Coordinate_system>")
                SurfaceLoads.append("<Direction>" + i.direction + "</Direction>")
                SurfaceLoads.append("<LoadBearingDirection>" + i.LoadBearingDirection + "</LoadBearingDirection>")
                SurfaceLoads.append("<q1>" + str(i.q1) + "</q1>")
                SurfaceLoads.append("<q2>" + str(i.q2) + "</q2>")
                SurfaceLoads.append("<q3>" + str(i.q3) + "</q3>")
                SurfaceLoads.append("<LoadConstantOrLinear>" + i.LoadConstantOrLinear + "</LoadConstantOrLinear>")
                SurfaceLoads.append("<iq1>" + str(i.iq1) + "</iq1>")
                SurfaceLoads.append("<iq2>" + str(i.iq2) + "</iq2>")
                SurfaceLoads.append("<iq3>" + str(i.iq3) + "</iq3>")
                SurfaceLoads.append("<q3>" + str(i.q3) + "</q3>")
            else:
                pass
        SurfaceLoads.append("</SurfaceLoads>")
        self.SurfaceLoads = ''.join(str(SL) for SL in SurfaceLoads)
    def addPanels(self,obj):
        nm = i.__class__.__name__
        Panels = []
        Panels.append("<Panels>")
        slN = 0
        for i in obj:
            slN = slN + 1
            if nm == "LoadPanel":
                Panels.append("<Number>" + str(n) + "</Number>")
                Panels.append("<Description>" + i.Description + "</Description>")
                for j in i.PolyCurve.points:
                    Panels.append("<NodeX>" + str(j.X) + "</NodeX>")
                    Panels.append("<NodeY>" + str(j.Y) + "</NodeY>")
                    Panels.append("<NodeZ>" + str(j.Z) + "</NodeZ>")
                Panels.append("<LoadBearingDirection>" + i.LoadBearingDirection + "</LoadBearingDirection>")
                Panels.append("<SurfaceType>" + i.LoadBearingDirection + "</SurfaceType>")
            else:
                pass
        Panels.append("</Panels>")
        self.Panels = ''.join(str(pan) for pan in Panels)

    def addProject(self,projectname):
=======
    def addProject(self, projectname):
>>>>>>> Stashed changes
        self.Project = "<ProjectName>" + projectname + "</ProjectName>"

    def addprojectnumber(self, ProjectNumber):
        self.ProjectNumber = "<ProjectNumber>" + ProjectNumber + "</ProjectNumber>"

<<<<<<< Updated upstream
=======
    def addPanels(self):
        Panels = []
        Panels.append("<Panels>")
        Panels.append("<Number>1</Number>")
        Panels.append("<Description>Panel 1</Description>")
        Panels.append("<LoadBearingDirection>X</LoadBearingDirection>")  # X or Y
        Panels.append(
            "<SurfaceType>wall</SurfaceType>")  # Wall, Free-standing wall, Flat roof, Shed roof, Saddle roof, Unknown
        Panels.append("<NodeX>0</NodeX>")
        Panels.append("<NodeY>0</NodeY>")
        Panels.append("<NodeZ>0</NodeZ>")
        Panels.append("<NodeX>10000</NodeX>")
        Panels.append("<NodeY>0</NodeY>")
        Panels.append("<NodeZ>0</NodeZ>")
        Panels.append("<NodeX>10000</NodeX>")
        Panels.append("<NodeY>1000</NodeY>")
        Panels.append("<NodeZ>0</NodeZ>")  # unclosed polygon
        Panels.append("</Panels>")
        self.Panels = ''.join(str(Pan) for Pan in Panels)

>>>>>>> Stashed changes
    def XML(self):
        self.xmlstr = self.Frame1 + self.Project + self.ProjectNumber + self.ExportDate + self.XMLVersion + self.Nodes + self.Supports + self.Grids + self.Profiles  + self.Beamgroup + self.Beams + self.Plates + self.Panels + + self.LoadCases + self.BeamLoads + self.NodeLoads + self.SurfaceLOads + self.Combinations + self.RebarLongitudinal + self.RebarStirrup + self.Layers + self.Frame2

    def __str__(self):
        return f"{__class__.__name__}(" + f"{self.xmlstr})"






