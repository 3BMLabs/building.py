# -*- coding: utf8 -*-
#***************************************************************************
#*   Copyright (c) 2023 Maarten Vroegindeweij & Jonathan van der Gouwe      *
#*   maarten@3bm.co.nl & jonathan@3bm.co.nl                                *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   This program is distributed in the hope that it will be useful,       *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Library General Public License for more details.                  *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************


"""This module provides an exchange with XFEM4U
"""

__title__= "XFEM4U"
__author__ = "Maarten & Jonathan"
__url__ = "./exchange/Struct4U.py"

import xml.etree.ElementTree as ET
from geometry.curve import *
from exchange.speckle import *

#To do:
#Line to Grid Object
#Grid Object with building.py line --> convert to Speckle Line with pattern

def getXYZ(XMLtree, nodenumber):
    root = XMLtree.getroot()
    # POINTS
    n = root.findall(".//Nodes/Number")
    nodenumbers = []

    for i in n:
        nodenumbers.append(i.text)
    #Search
    rest = nodenumbers.index(nodenumber)
    return(rest)

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
    return nodenumbers,XYZ

def XMLImportgetGridDistances(Grids):
    #Function to create grids from the format 0, 4x5400, 4000, 4000 to absolute XYZ-values
    GridsNew = []
    distance = 0.0
    #GridsNew.append(distance)
    for i in Grids:
        #del Grids[0]
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

def XMLImportGrids(XMLtree,gridExtension):
    #create lines in Speckle from the grids
    root = XMLtree.getroot()
    gridlines = []

    #GRIDS
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
        grids.append(Line(Point(i, -GridEx, 0),Point(i, Ymax+GridEx, 0)))

    for i in GridsY:
        grids.append(Line(Point(-GridEx, i, 0),Point(Xmax+GridEx, i, 0)))

    for i in GridsZ:
        grids.append(Line(Point(0, 0, i) , Point(0, Xmax, i)))

    for i in grids:
        line = LineToSpeckleLine(i) #Grid to SpeckleLine
        gridlines.append(line)
    return gridlines


def XMLImportPlates(XMLtree):
    #Get platedata from XML
    root = XMLtree.getroot()
    #PLATES

    PlatesNumber = root.findall(".//Plates/Number")
    PlatesNodes = root.findall(".//Plates/Node")

    # for loop to get each element in an array

    rootPlates = root.findall(".//Plates")

    #XMLImportPlates(root):
    PlatesTags = []
    PlatesValues = []
    for elements in root:
        if elements.tag == "Plates":
            for element in elements:
                PlatesTags.append(element.tag)
                PlatesValues.append(element.text)

    #Iedere plate met nodes in een sublijst stoppen
        #plate
            #nodes

    ind = [i for i, x in enumerate(PlatesTags) if x == "Number"] # indices where a new plate starts.

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
            platesIndices.append(PlatesTags[x::]) # voor de laatste item uit de lijst, anders out of range
            platesValues.append(PlatesValues[x::]) # voor de laatste item uit de lijst, anders out of range
            platesNodes.append(PlatesValues[x+1:-5])

    obj = []

    XYZ = XMLImportNodes(XMLtree)[1] #Knopen

    platesPlatePoints = []
    for i in platesNodes:
        SpecklePlatePoints = []
        PlatePoints = []
        for j in i:
            Point = XYZ[getXYZ(XMLtree,j)]
            PlatePoints.append(Point)
            SpecklePlatePoints.append(PointToSpecklePoint(Point))
        SpecklePlatePoints.append(SpecklePlatePoints[0])
        PlatePoints.append(PlatePoints[0])
        ply = SpecklePolyLine.from_points(SpecklePlatePoints)
        obj.append(ply)
        platesPlatePoints.append(PlatePoints)
    return obj, platesPlatePoints

