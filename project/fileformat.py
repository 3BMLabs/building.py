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


"""This module provides the fileformat class
"""

__title__= "fileformat"
__author__ = "Maarten & Jonathan"
__url__ = "./fileformat/fileformat.py"


import sys, os, math
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from geometry.point import Point

class BuildingPy:
    def __init__(self, name=None, number=None):
        self.name: str = name
        self.number: str = number
        self.objects = []
        self.units = "mm"
        self.decimals = 3 #not implemented yet
        self.origin = Point(0,0,0)
        self.scale = 1
        #prefix objects (name)
        #Geometry settings

        #export selection info
        self.domain = None
        self.applicationId = "OPEN-AEC | BuildingPy"

        #different settings for company's?

        #rename this to autoclose?
        self.closed: bool = True #auto close polygons? By default true, else overwrite
        self.round: bool = True #If True then arcs will be segmented. Can be used in Speckle.

        #Speckle settings
        self.speckleserver = "3bm.exchange"
        self.specklestream = None

    # @property
    # def units(self):
    #     return "mm"


    def toSpeckle(self, streamid, commitstring=None):
        from exchange.speckle import translateObjectsToSpeckleObjects, TransportToSpeckle
        self.specklestream = streamid
        speckleobj = translateObjectsToSpeckleObjects(self.objects)
        TransportToSpeckle(self.speckleserver,streamid,speckleobj,commitstring)


project = BuildingPy("Project","0")