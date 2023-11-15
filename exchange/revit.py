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
__url__ = "./exchange/revit.py"


import sys
from pathlib import Path
# import specklepy

sys.path.append(str(Path(__file__).resolve().parents[1]))

from geometry.point import Point
from geometry.curve import Line

# from specklepy.api.client import SpeckleClient
# from specklepy.api.credentials import get_default_account
# from specklepy.transports.server import ServerTransport
# from specklepy.api import operations

# from specklepy.objects import Base
# from specklepy.objects.geometry import Point as SpecklePoint
# from specklepy.objects.geometry import Line as SpeckleLine

#convert from our line class to Revit line (3d model line)


#draw line in revit using specklepy


