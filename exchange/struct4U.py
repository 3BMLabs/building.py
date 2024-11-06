# [included in BP singlefile]
# [!not included in BP singlefile - start]
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


"""This module provides an exchange with XFEM4U
"""

from BuildingPy import Support
from construction.datum import *
from construction.panel import *
from exchange.speckle import *
from geometry.curve import *
from abstract.node import *
from construction.frame import Frame
import xml.etree.ElementTree as ET
__title__ = "XFEM4U"
__author__ = "Maarten & Jonathan"
__url__ = "./exchange/struct4U.py"


# [!not included in BP singlefile - end]

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
    
    nodenumbers = [node.text for node in root.findall(".//Nodes/Number")]
    X = [float(x.text.replace(",", ".")) for x in root.findall(".//Nodes/X")]
    Y = [float(y.text.replace(",", ".")) for y in root.findall(".//Nodes/Y")]
    Z = [float(z.text.replace(",", ".")) for z in root.findall(".//Nodes/Z")]
    
    XYZ = [Point(x, y, z) for x, y, z in zip(X, Y, Z)]
    
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
            width = float(spl[1].replace(",", "."))
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
        grids.append(Line(start=Point(i, -GridEx, 0),
                     end=Point(i, Ymax+GridEx, 0)))

    for i in GridsY:
        grids.append(Line(start=Point(-GridEx, i, 0),
                     end=Point(Xmax+GridEx, i, 0)))

    for i in GridsZ:
        grids.append(Line(start=Point(0, 0, i), end=Point(0, Xmax, i)))

    obj = []
    for i in grids:
        obj.append(Grid.by_startpoint_endpoint(i, "Grid"))
     #   gridlines.append(line)
    return obj

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
    for i in platesNumbersElem:
        platesNumbers.append(i.text)
    PlatesNodes = []
    for i in PlatesNodesElem:
        PlatesNodes.append(i.text)
    platesMaterialQuality = []
    for i in platesMaterialElem:
        platesMaterialQuality.append(i.text)
    platesMaterial = []
    lstConcrete = ["C20/25", "C25/30", "C30/37",
                   "C35/45", "C40/50", "C45/55", "C50/60", "C53/65"]
    lstTimber = ["C14", "C16", "C18", "C20", "C22", "C24", "C27", "C30", "C35",
                 "C40", "C50", "D18", "D24", "D30", "D35", "D40", "D50", "D60", "D70"]
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
    for i in platesZElem:
        platesZ.append(float(i.text))
    platesThickness = []
    for i in platesThicknessElem:
        platesThickness.append(float(i.text))
    platesTop_Center_Bottom = []
    for i in platesTop_Center_BottomElem:
        platesTop_Center_Bottom.append(i.text)

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

    # indices where a new plate starts.
    ind = [i for i, x in enumerate(PlatesTags) if x == "Number"]

    platesIndices = []
    platesValues = []
    platesNodes = []
    count = 0
    for x in ind:
        count = count + 1
        try:
            platesIndices.append(PlatesTags[x:ind[count]])
            platesValues.append(PlatesValues[x:ind[count]])
            platesNodes.append(PlatesValues[x+1:ind[count]-5])
        except:
            # voor de laatste item uit de lijst, anders out of range
            platesIndices.append(PlatesTags[x::])
            # voor de laatste item uit de lijst, anders out of range
            platesValues.append(PlatesValues[x::])
            platesNodes.append(PlatesValues[x+1:-5])

    obj = []
    XYZ = XMLImportNodes(XMLtree)[1]  # Knopen

    platesPolyCurves = []
    for i in platesNodes:
        PlatePoints = []
        for j in i:
            Point = XYZ[getXYZ(XMLtree, j)]
            PlatePoints.append(Point)
        # PlatePoints.append(PlatePoints[0])
        ply = PolyCurve.by_points(PlatePoints)
        # obj.append(ply)
        platesPolyCurves.append(ply)

    # Panels maken Building.py
    Panels = []

    for i, j, k, l, m, n in zip(platesPolyCurves, platesThickness, plateOffsets, platesMaterial, platesNumbers, lstColor):
        Panels.append(Panel.by_polycurve_thickness(i, -j, k, l + m, n))
        print("Panel created")

    return Panels


class xmlXFEM4U:
    def __init__(self):
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
        self.xmlstr = None

    def addBeamsPlates(self, objects : list):
        # Number of nodes:
        node_count:int = 0
        plate_count:int = 0  # Numbering plates
        beam_count:int = 0  # Numbering beams
        beam_group_count:int = 0  # Numbering beamgroup
        profile_count:int = 0  # Numbering profiles
        support_count:int = 0  # Numbering of supports
        Nodes = []
        Beam_groups = "<Beamgroup>\n"
        Points : list[Point] = []
        Nodes.append("<Nodes>\n")
        Plates = "<Plates>"
        Beams = "<Beams>\n"
        Profiles = "<Profiles>\n"
        Supports = "<Supports>\n"

        ProfileNames = []  # all profiles
        for object in objects:
            className = object.__class__.__name__
            if className == "Frame":
                ProfileNames.append([object, object.profileName])

        ProfileNamesUnique = []  # Unique profiles
        ItemsOfUniqueProfileName = []
        for item in ProfileNames:
            if item[1] not in ProfileNamesUnique:
                ProfileNamesUnique.append(item[1])
                ItemsOfUniqueProfileName.append(item[0])

        for name, item in zip(ProfileNamesUnique, ItemsOfUniqueProfileName):
            profile_count = profile_count + 1
            Profiles += "<Number>" + str(profile_count) + "</Number>\n"
            if item.material.name == "Steel":
                Profiles += "<Profile_name>" + name + "</Profile_name>\n"
                Profiles += "<Material_type>" + "0" + "</Material_type>\n"
                Profiles += "<Material>" + "S235" + "</Material>\n"
                Profiles += "<Angle>" + "0" + "</Angle>\n"
            elif item.material.name == "Timber":
                Profiles += "<Profile_name>" + "Profile " + str(profile_count) + "</Profile_name>\n"
                Profiles += "<Material_type>" + "2" + "</Material_type>\n"
                Profiles += "<Material>" + "C24" + "</Material>\n"
                Profiles += "<Angle>" + "0" + "</Angle>\n"
                Profiles += "<ServiceClass>" + "0" + "</ServiceClass>\n"
                Profiles += "<Profile_shape>" + "6" + "</Profile_shape>\n"
                Profiles += "<h>" + str(item.profile.h) + "</h>\n"
                Profiles += "<b>" + str(item.profile.b) + "</b>\n"
                Profiles += "<tf>" + str(item.profile.h) + "</tf>\n"
                Profiles += "<tw>10</tw>\n"
                Profiles += "<r1>5</r1>\n"
                Profiles += "<r2>5</r2>\n"
            elif item.material.name == "Concrete":
                Profiles += "<Profile_name>" + "Profile " + str(profile_count) + "</Profile_name>\n"
                Profiles += "<Material_type>" + "1" + "</Material_type>\n"
                Profiles += "<Material>" + "C20/25" + "</Material>\n"
                Profiles += "<Angle>" + "0" + "</Angle>\n"
                Profiles += "<Profile_shape>" + "1" + "</Profile_shape>\n"
                Profiles += "<h>" + str(item.profile.h) + "</h>\n"
                Profiles += "<b>" + str(item.profile.b) + "</b>\n"
                Profiles += "<h1>50</h1>\n"
                Profiles += "<b1>50</b1>\n"
                Profiles += "<h2>50</h2>\n"
                Profiles += "<b2>50</b2>\n"
                Profiles += "<h3>50</h3>\n"
                Profiles += "<b3>50</b3>\n"
                Profiles += "<h4>50</h4>\n"
                Profiles += "<b4>50</b4>\n"
        for object in objects:
            match object.__class__.__name__:
                case 'Panel':
                    panel : Panel = object
                    plate_count = plate_count + 1
                    Plates += "<Number>" + str(plate_count) + "</Number>\n"
                    PlatePoints = panel.origincurve.points[: -1]
                    for platePoint in PlatePoints:
                        node_count = node_count + 1
                        Nodes.append("<Number>" + str(node_count) + "</Number>\n")
                        Nodes.append("<X>" + str(round(platePoint.x)) + "</X>\n")
                        Nodes.append("<Y>" + str(round(platePoint.y)) + "</Y>\n")
                        Nodes.append("<Z>" + str(round(platePoint.z)) + "</Z>\n")
                        Plates += "<Node>" + str(node_count) + "</Node>\n"
                        Points.append([platePoint, node_count])
                    Plates += "<h>" + str(panel.thickness) + "</h>\n"
                    Plates.append(
                        "<Material_type>" + "c4aeb39b3f8d45cf9613e8377bdf73624" + "</Material_type>\n")  # material nog uitlezen #Concrete: c9a5876f475cefab7cc11281b017914a1 # Steel: c4aeb39b3f8d45cf9613e8377bdf73624
                    # material nog uitlezen
                    Plates += "<Material>" + "S235" + "</Material>\n"
                    Plates += "<Z>" + "0" + "</Z>\n"
                    Plates.append("<Top_Center_Bottom>" +
                                  "Center" + "</Top_Center_Bottom>\n")


                case 'Frame':
                    frame : Frame = object
                    ProfN = ProfileNamesUnique.index(frame.profileName) + 1
                    beam_group_count = beam_group_count + 1
                    Beam_groups += "<Number>" + str(beam_group_count) + "</Number>\n"
                    node_count = node_count + 1 # frame object (node number)
                    Nodes.append("<Number>" + str(node_count) + "</Number>\n")
                    Nodes.append("<X>" + str(round(frame.start.x)) + "</X>\n")
                    Nodes.append("<Y>" + str(round(frame.start.y)) + "</Y>\n")
                    Nodes.append("<Z>" + str(round(frame.start.z)) + "</Z>\n")

                    Beam_groups += "<Startnode>" + str(node_count) + "</Startnode>\n"

                    Points.append([frame.start, node_count])
                    
                    #1 based index?
                    beam_count += 1
                    Beams += "<Number>" + str(beam_count) + "</Number>"
                    Beams.append("<Beamgroupnumber>" +
                                 str(beam_group_count) + "</Beamgroupnumber>\n")
                    Beams.append("<From_node_number>" +
                                 str(node_count) + "</From_node_number>\n")

                    node_count += 1
                    Nodes.append("<Number>" + str(node_count) + "</Number>\n")
                    Nodes.append("<X>" + str(round(frame.end.x)) + "</X>\n")
                    Nodes.append("<Y>" + str(round(frame.end.y)) + "</Y>\n")
                    Nodes.append("<Z>" + str(round(frame.end.z)) + "</Z>\n")

                    Beam_groups += "<Endnode>" + str(node_count) + "</Endnode>\n"

                    Points.append([frame.end, node_count])

                    Beams.append("<To_node_number>" +
                                 str(node_count) + "</To_node_number>\n")
                    Beams += "<Angle>" + str(frame.rotation) + "</Angle>\n"
                    Beams += "<Angle_profile>" + "0" + "</Angle_profile>\n"
                    ProfNstr = str(ProfN)
                    Beams.append("<Profile_number>" + ProfNstr +
                                 "</Profile_number>\n")
                    Beams += "<Z>" + str(frame.ZOffset) + "</Z>\n"
                    Beams.append("<Top_Center_Bottom>" +
                                 frame.YJustification + "</Top_Center_Bottom>\n")
                case 'Grid':
                    pass
        node_count = int((len(Nodes)-1)/4) #every node has 4 lines. Min 1 line voor xml-tag
        for object in objects:
            className = object.__class__.__name__
            if className == 'Support':
                support: Support = object
                support_count = support_count + 1

                bools = []
                for point in Points: # Moet Nodesnumber zijn niet points
                    bools.append(Point.intersect(support.Point, point[0]))
                if sum(bools) > 0:  # Means intersection with existing point/node
                    no = bools.index(1)+1 #nodenumber which intersects
                else:  # No intersection, so new node is required
                    node_count = int((len(Nodes) - 1) / 4)  # every node has 4 lines. Min 1 line voor xml-tag
                    node_count = node_count + 1
                    no = node_count
                    Nodes.append("<Number>" + str(node_count) + "</Number>\n")
                    Nodes.append("<X>" + str(round(support.Point.x)) + "</X>\n")
                    Nodes.append("<Y>" + str(round(support.Point.y)) + "</Y>\n")
                    Nodes.append("<Z>" + str(round(support.Point.z)) + "</Z>\n")
                Supports += "<Number>" + str(support_count) + "</Number>\n"
                Supports += "<Nodenumber>" + str(no) + "</Nodenumber>\n"
                Supports += "<Tx>" + support.Tx + "</Tx>\n"
                Supports += "<Ty>" + support.Ty + "</Ty>\n"
                Supports += "<Tz>" + support.Tz + "</Tz>\n"
                Supports += "<Rx>" + support.Rx + "</Rx>\n"
                Supports += "<Ry>" + support.Ry + "</Ry>\n"
                Supports += "<Rz>" + support.Rz + "</Rz>\n"
                Supports += "<Kx>" + str(support.Kx) + "</Kx>\n"
                Supports += "<Ky>" + str(support.Ky) + "</Ky>\n"
                Supports += "<Kz>" + str(support.Kz) + "</Kz>\n"
                Supports += "<Cx>" + str(support.Cx) + "</Cx>\n"
                Supports += "<Cy>" + str(support.Cy) + "</Cy>\n"
                Supports += "<Cz>" + str(support.Cz) + "</Cz>\n"
                Supports += "<dx>" + str(support.dx) + "</dx>\n"
                Supports += "<dy>" + str(support.dy) + "</dy>\n"
                Supports += "<dz>" + str(support.dz) + "</dz>\n"
            else:
                pass

        Nodes.append("</Nodes>\n")
        Plates += "</Plates>\n"
        Beams += "</Beams>\n"
        Profiles += "</Profiles>\n"
        Beam_groups += "</Beamgroup>\n"
        Supports += "</Supports>\n"

        self.Nodes = ''.join(str(N) for N in Nodes)
        self.Plates = Plates
        self.Beams = Beams
        self.Beamgroup = Beam_groups
        self.Profiles = Profiles
        self.Supports = Supports

    def addGrids(self, spacX=None, seqX=None, spacY=None, seqY=None, z=None):
        if spacX is None:
            self.Grids = "<Grids>" + "</Grids>"
        else:
            self.Grids = "<Grids>" + "<X>" + spacX + "</X>" + "<X_Lable>" + seqX + "</X_Lable>" + "<Y>" + spacY + "</Y>" + "<Y_Lable>" + seqY + "</Y_Lable>" + "<Z>" + "0 " + str(
                z) + "</Z>" + "<Z_Lable>" + "+0 h" + "</Z_Lable>" + "</Grids>"

    def addSurfaceLoad(self, obj=None):
        SurfaceLoads = []
        SurfaceLoads.append("<SurfaceLoads>\n")
        if obj != None:
            slN = 0
            for i in obj:
                nm = i.__class__.__name__
                if nm == "SurfaceLoad":
                    slN = slN + 1
                    SurfaceLoads.append("<Number>" + str(slN) + "</Number>\n")
                    SurfaceLoads.append(
                        "<LoadCaseNumber>" + str(i.LoadCase) + "</LoadCaseNumber>\n")
                    SurfaceLoads.append(
                        "<Description>" + i.Description + "</Description>\n")
                    for j in i.PolyCurve.points:
                        SurfaceLoads.append(
                            "<NodeX>" + str(j.x) + "</NodeX>\n")
                        SurfaceLoads.append(
                            "<NodeY>" + str(j.y) + "</NodeY>\n")
                        SurfaceLoads.append(
                            "<NodeZ>" + str(j.z) + "</NodeZ>\n")
                    SurfaceLoads.append(
                        "<Coordinate_system>" + i.crs + "</Coordinate_system>\n")
                    SurfaceLoads.append(
                        "<Direction>" + i.direction + "</Direction>\n")
                    SurfaceLoads.append(
                        "<LoadBearingDirection>" + i.LoadBearingDirection + "</LoadBearingDirection>\n")
                    SurfaceLoads.append("<q1>" + str(i.q1) + "</q1>\n")
                    SurfaceLoads.append("<q2>" + str(i.q2) + "</q2>\n")
                    SurfaceLoads.append("<q3>" + str(i.q3) + "</q3>\n")
                    SurfaceLoads.append(
                        "<LoadConstantOrLinear>" + i.LoadConstantOrLinear + "</LoadConstantOrLinear>\n")
                    SurfaceLoads.append("<iq1>" + str(i.iq1) + "</iq1>\n")
                    SurfaceLoads.append("<iq2>" + str(i.iq2) + "</iq2>\n")
                    SurfaceLoads.append("<iq3>" + str(i.iq3) + "</iq3>\n")
                else:
                    pass
        SurfaceLoads.append("</SurfaceLoads>\n")
        self.SurfaceLoads = ''.join(str(SL) for SL in SurfaceLoads)

    def convert_panels_to_xml(self, objects=None) -> string:
        Panels = "<Panels>"
        if objects != None:
            slN = 0
            for object in objects:
                nm = object.__class__.__name__
                if nm == "LoadPanel":
                    slN = slN + 1
                    Panels += "<Number>" + str(slN) + "</Number>\n"
                    Panels += "<Description>" + object.Description + "</Description>\n"
                    for j in object.PolyCurve.points:
                        Panels += "<NodeX>" + str(j.x) + "</NodeX>\n"
                        Panels += "<NodeY>" + str(j.y) + "</NodeY>\n"
                        Panels += "<NodeZ>" + str(j.z) + "</NodeZ>\n"
                    Panels.append(
                        "<LoadBearingDirection>" + object.LoadBearingDirection + "</LoadBearingDirection>\n")
                    Panels.append("<SurfaceType>" +
                                  object.LoadBearingDirection + "</SurfaceType>\n")
                else:
                    pass
        Panels += "</Panels>\n"
        return Panels
        
    def __str__(self):
        return f"{__class__.__name__}(" + f"{self.xmlstr})"

def convert_to_XFEM4U_XML(project: BuildingPy, gridinputs) -> string:
    xmlS4U = xmlXFEM4U()  # Create XML object with standard values
    # Add Beams, Profiles, Plates, Beamgroups, Nodes
    xmlS4U.addBeamsPlates(project.objects)
    
    if gridinputs is None:
        xmlS4U.addGrids()  # Grids
    else:
        xmlS4U.addGrids(gridinputs[0],gridinputs[1],gridinputs[2],gridinputs[3],gridinputs[4])
    
    ProjectNumber = 0
    
            #the layout of this giant export function is like the file itself. 
    xmlstr = \
    "<Frame>" + \
       "<ProjectName>" + project.name + """</ProjectName>
        <ProjectNumber>""" + ProjectNumber + """</ProjectNumber>
        <ExportDateTime>2023-04-08 19:55:39Z</ExportDateTime>
        <XMLExportVersion>v4.0.30319</XMLExportVersion>\n""" +\
            project.Nodes + project.Supports + project.Grids + project.Profiles + project.Beamgroup + project.Beams + \
            project.Plates +\
            xmlS4U.convert_panels_to_xml(project.objects) + \
        """
        <LoadCases>\n
            <Number>1</Number>\n
            <Description>Permanent</Description>\n
            <Type>0</Type>\n
            <psi0>1</psi0>\n
            <psi1>1</psi1>\n
            <psi2>1</psi2>\n
            <Number>2</Number>\n
            <Description>Veranderlijk</Description>\n
            <Type>1</Type>\n
            <psi0>0,4</psi0>\n
            <psi1>0,5</psi1>\n
            <psi2>0,3</psi2>\n
        </LoadCases>\n""" + \
            project.BeamLoads + project.NodeLoads + project.SurfaceLoads + \
            """
        <Combinations>\n
            <LoadCombinationNumber>1</LoadCombinationNumber>\n
            <Description>Dead load</Description>\n
            <CombTyp>0</CombTyp>\n
            <Case>1</Case>\n
            <Psi>1</Psi>\n
            <Gamma>1, 35</Gamma>\n
            <Case>2</Case>\n
            <Psi>1</Psi>\n
            <Gamma>1, 5</Gamma>\n
            <LoadCombinationNumber>2</LoadCombinationNumber>\n
            <Description>Live load</Description>\n
            <CombTyp>0</CombTyp>\n
            <Case>1</Case>\n
            <Psi>1</Psi>\n
            <Gamma>1, 2</Gamma>\n
            <Case>2</Case>\n
            <Psi>1</Psi>\n
            <Gamma>1, 5</Gamma>\n
            <LoadCombinationNumber>3</LoadCombinationNumber>\n
            <Description>Dead load</Description>\n
            <CombTyp>3</CombTyp>
            <Case>1</Case>
            <Psi>1</Psi>
            <Gamma>1</Gamma>
            <Case>2</Case>
            <Psi>1</Psi>
            <Gamma>1</Gamma>
            <LoadCombinationNumber>4</LoadCombinationNumber>
            <Description>Live load</Description>
            <CombTyp>3</CombTyp>
            <Case>1</Case>
            <Psi>1</Psi>
            <Gamma>1</Gamma>
            <Case>2</Case>
            <Psi>1</Psi>
            <Gamma>1</Gamma>
            <LoadCombinationNumber>5</LoadCombinationNumber>
            <Description>SLS
            Permanent</Description>
            <CombTyp>4</CombTyp>
            <Case>1</Case>
            <Psi>1</Psi>
            <Gamma>1</Gamma>
            <LoadCombinationNumber>6</LoadCombinationNumber>
            <Description>SLS Quasi - permanent</Description>
            <CombTyp>2</CombTyp>
            <Case>1</Case>
            <Psi>1</Psi>
            <Gamma>1</Gamma>
            <Case>2</Case>
            <Psi>0, 8</Psi>
            <Gamma>1</Gamma>
        </Combinations>
        <RebarLongitudinal>
        </RebarLongitudinal>
        <RebarStirrup>
        </RebarStirrup>
        <Layers>
            <Layer_number>1</Layer_number>
            <Layer_description>Layer 1</Layer_description>
        </Layers>
    </Frame>"""
    
    return xmlS4U.xmlstr

def createXFEM4UXML(project: BuildingPy, filepathxml: str, gridinputs=None):
    # Export to XFEM4U XMLK-file
    
    #create XML data
    XMLString = convert_to_XFEM4U_XML(project, gridinputs)

    filepath = filepathxml
    file = open(filepath, "w")
    a = file.write(XMLString)
    file.close()

    return filepath


def writeDirectCommandsfile(xmlfilepath: str):
    # Write Ini-file for directcommands
    pathdirectcommands = os.path.join(
        os.getenv('LOCALAPPDATA'), 'Struct4u', 'DirectCommands_XFEM4U.ini')
    row1 = '[Struct4u]\n'
    row2 = 'Import_XML=' + xmlfilepath + '\n'
    content = row1 + row2

    file = open(pathdirectcommands, "w")
    a = file.write(content)
    file.close()


def openXMLInXFEM4U(fileName):
    #Open XML file in XFEM4U
    os.system("C:/Struct4u/XFEM4U/wframe3d.exe " + fileName)

def openXFrame2D(fileName):
    #Open XML file in XFEM4U
    os.system("C:/Program Files (x86)/Struct4u/XFrame2d/XFrame2d.exe " + fileName)

def openXFEM4U():
    #Run XFEM4U
    path = r"C:/Struct4u/XFEM4U/wframe3d.exe"
    os.spawnl(os.P_NOWAIT,  # flag
              path,  # program
              path)  # arguments
    #import subprocess
    #try:
    #    subprocess.run("C:/Struct4u/XFEM4U/wframe3d.exe", shell=True, check=False)
    #except:
    #    print("exception")

def process_exists(process_name):
    import subprocess
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    # use buildin check_output right away
    output = subprocess.check_output(call).decode()
    # check in last line for process name
    last_line = output.strip().split('\r\n')[-1]
    # because Fail message could be translated
    return last_line.lower().startswith(process_name.lower())

def OpenXMLXFEM4U(pathxml):
    import time
    # CHECK IF XFEM4U IS OPENED. IF NOT OPEN XFEM4U
    if process_exists("wframe3d.exe") is True:
        pass
    else:
        openXFEM4U()
        time.sleep(20)
    # WRITE DIRECTCOMMANDS TO XFEM4U, THEN XML-FILE IS OPENED IN XFEM4U
    writeDirectCommandsfile(pathxml)