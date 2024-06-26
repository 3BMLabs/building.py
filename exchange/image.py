# [included in BP singlefile]
# [!not included in BP singlefile - start]
# -*- coding: utf8 -*-
#***************************************************************************
#*   Copyright (c) 2024 Maarten Vroegindeweij                              *
#*   maarten@3bm.co.nl                                                     *
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


"""This module provides import data from PAT file
"""

__title__= "image"
__author__ = "Maarten"
__url__ = "./exchange/image.py"

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from PIL import Image, ImageDraw
from objects.steelshape import *
from geometry.point import Point
from geometry.curve import Arc

# [!not included in BP singlefile - end]

def img(width,height,scalefactor):
    SF = scalefactor
    img = Image.new("RGB", (width, height))
    img1 = ImageDraw.Draw(img)

    return img

def PolyCurve2DToIMG(PC, widthimgpix: float, img1, scalefactor):
    SF = scalefactor
    bounds = PolyCurve2D.bounds(PC)
    dx = 50
    xmin = bounds[0] - dx
    ymin = bounds[2] - dx

    for i in PC.curves:
        if i.__class__.__name__ == "Arc2D":
            AC = Arc(Point(i.start.x, i.start.y, 0), Point(i.mid.x, i.mid.y, 0), Point(i.end.x, i.end.y, 0))
            lines = Arc.segmented_arc(AC, 10)
            for i in lines:
                x0 = (i.start.x - xmin) * SF
                y0 = (i.start.y - ymin) * SF
                x1 = (i.end.x - xmin) * SF
                y1 = (i.end.y - ymin) * SF
                coords = [(x0, y0), (x1, y1)]
                img1.line(coords, fill="red", width=1)
        elif i.__class__.__name__ == "Line2D":
            coords = [((i.start.x - xmin) * SF, (i.start.y - ymin) * SF),
                      ((i.end.x - xmin) * SF, (i.end.y - ymin) * SF)]
            img1.line(coords, fill="red", width=1)
        else:
            print("unknown curve is used")

        return img1