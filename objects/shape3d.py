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


"""This module provides classes for 3d objects
"""

__title__= "shape3d"
__author__ = "Joas"
__url__ = "./objects/shape3d.py"

import sys, os, math
from pathlib import Path
from specklepy import *
from specklepy.objects.geometry import Mesh as SpeckleMesh
# from abstract.color import *

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

class Origin:
    originx = 0
    originy = 0
    originz = 0
    number_of_triangles = 300
    number_of_rectangles = 400
    r = 800
    r2 = 300
    vertices_up = [originx, originy, originz + 350]
    vertices_right = [originx + 350, originy, originz]
    vertices_front = [originx, originy + 350, originz]
    faces_up = []
    faces_right = []
    faces_front = []
    facenr = 1
    degrees = 0
    degrees2 = 360 / number_of_triangles

    # UP ARROW

    for i in range(number_of_triangles):
        x = math.cos(math.radians(degrees)) * r
        y = math.sin(math.radians(degrees)) * r
        degrees += degrees2
        vertices_up.append(originx + x)
        vertices_up.append(originy + y)
        vertices_up.append(originz + 200)

        faces_up.append(3)
        faces_up.append(0)

        if facenr < number_of_triangles:
            faces_up.append(facenr)
            faces_up.append(facenr + 1)
            facenr += 1
        else:
            faces_up.append(number_of_triangles)
            faces_up.append(1)

            faces_up.append(number_of_triangles)
            for i in range(number_of_triangles):
                faces_up.append(i + 1)


    vertices2 = []
    faces2 = []
    facenr2 = 0
    degrees3 = 0
    degrees4 = 360 / number_of_rectangles

    for i in range(number_of_rectangles):
        x = math.cos(math.radians(degrees3)) * r2
        y = math.sin(math.radians(degrees3)) * r2
        vertices2.append(originx + x)
        vertices2.append(originy + y)
        vertices2.append(originz + 200)
        vertices2.append(originx + x)
        vertices2.append(originy + y)
        vertices2.append(originz)
        degrees3 += degrees4

        if facenr2 < number_of_rectangles * 2 - 2:
            faces2.append(4)
            faces2.append(facenr2)
            faces2.append(facenr2 + 1)
            faces2.append(facenr2 + 3)
            faces2.append(facenr2 + 2)
            facenr2 += 2
        else:
            faces2.append(4)
            faces2.append(facenr2)
            faces2.append(facenr2 + 1)
            faces2.append(1)
            faces2.append(0)

            faces2.append(number_of_rectangles)
            count = 1
            for i in range(number_of_rectangles):
                if count <= number_of_rectangles * 2:
                    faces2.append(count)
                    count += 2
                else:
                    pass

    # RIGHT ARROW

    degrees = 0
    facenr = 1

    for i in range(number_of_triangles):
        z = math.cos(math.radians(degrees)) * r
        y = math.sin(math.radians(degrees)) * r
        degrees += degrees2
        vertices_right.append(originx + 200)
        vertices_right.append(originy + y)
        vertices_right.append(originz + z)

        faces_right.append(3)
        faces_right.append(0)

        if facenr < number_of_triangles:
            faces_right.append(facenr)
            faces_right.append(facenr + 1)
            facenr += 1
        else:
            faces_right.append(number_of_triangles)
            faces_right.append(1)

            faces_right.append(number_of_triangles)
            for i in range(number_of_triangles):
                faces_right.append(i + 1)


    vertices_right2 = []
    faces_right2 = []
    facenr2 = 0
    degrees3 = 0
    degrees4 = 360 / number_of_rectangles

    for i in range(number_of_rectangles):
        z = math.cos(math.radians(degrees3)) * r2
        y = math.sin(math.radians(degrees3)) * r2
        vertices_right2.append(originx + 200)
        vertices_right2.append(originy + y)
        vertices_right2.append(originz + z)
        vertices_right2.append(originx)
        vertices_right2.append(originy + y)
        vertices_right2.append(originz + z)
        degrees3 += degrees4

        if facenr2 < number_of_rectangles * 2 - 2:
            faces_right2.append(4)
            faces_right2.append(facenr2)
            faces_right2.append(facenr2 + 1)
            faces_right2.append(facenr2 + 3)
            faces_right2.append(facenr2 + 2)
            facenr2 += 2
        else:
            faces_right2.append(4)
            faces_right2.append(facenr2)
            faces_right2.append(facenr2 + 1)
            faces_right2.append(1)
            faces_right2.append(0)

            faces_right2.append(number_of_rectangles)
            count = 1
            for i in range(number_of_rectangles):
                if count <= number_of_rectangles * 2:
                    faces_right2.append(count)
                    count += 2
                else:
                    pass

    # FRONT ARROW

    degrees = 0
    facenr = 1

    for i in range(number_of_triangles):
        z = math.cos(math.radians(degrees)) * r
        x = math.sin(math.radians(degrees)) * r
        degrees += degrees2
        vertices_front.append(originx + x)
        vertices_front.append(originy + 200)
        vertices_front.append(originz + z)

        faces_front.append(3)
        faces_front.append(0)

        if facenr < number_of_triangles:
            faces_front.append(facenr)
            faces_front.append(facenr + 1)
            facenr += 1
        else:
            faces_front.append(number_of_triangles)
            faces_front.append(1)

            faces_front.append(number_of_triangles)
            for i in range(number_of_triangles):
                faces_front.append(i + 1)


    vertices_front2 = []
    faces_front2 = []
    facenr2 = 0
    degrees3 = 0
    degrees4 = 360 / number_of_rectangles

    for i in range(number_of_rectangles):
        z = math.cos(math.radians(degrees3)) * r2
        x = math.sin(math.radians(degrees3)) * r2
        vertices_front2.append(originx + x)
        vertices_front2.append(originy + 200)
        vertices_front2.append(originz + z)
        vertices_front2.append(originx + x)
        vertices_front2.append(originy)
        vertices_front2.append(originz + z)
        degrees3 += degrees4

        if facenr2 < number_of_rectangles * 2 - 2:
            faces_front2.append(4)
            faces_front2.append(facenr2)
            faces_front2.append(facenr2 + 1)
            faces_front2.append(facenr2 + 3)
            faces_front2.append(facenr2 + 2)
            facenr2 += 2
        else:
            faces_front2.append(4)
            faces_front2.append(facenr2)
            faces_front2.append(facenr2 + 1)
            faces_front2.append(1)
            faces_front2.append(0)

            faces_front2.append(number_of_rectangles)
            count = 1
            for i in range(number_of_rectangles):
                if count <= number_of_rectangles * 2:
                    faces_front2.append(count)
                    count += 2
                else:
                    pass


    def SpeckleMeshByCone(verts, face):
        spcklmesh = SpeckleMesh(vertices=verts, faces=face, name="Joas", units="mm")
        return spcklmesh

    SpeckleObjUp = [SpeckleMeshByCone(vertices_up, faces_up)]
    SpeckleObjUp2 = [SpeckleMeshByCone(vertices2, faces2)]

    SpeckleObjRight = [SpeckleMeshByCone(vertices_right, faces_right)]
    SpeckleObjRight2 = [SpeckleMeshByCone(vertices_right2, faces_right2)]

    SpeckleObjFront = [SpeckleMeshByCone(vertices_front, faces_front)]
    SpeckleObjFront2 = [SpeckleMeshByCone(vertices_front2, faces_front2)]


    lst = [SpeckleObjUp, SpeckleObjUp2, SpeckleObjRight, SpeckleObjRight2, SpeckleObjFront, SpeckleObjFront2]
    return lst
    # Commit = TransportToSpeckle("speckle.xyz", "8136460d9e", lst, "Shiny Commit")
    # Commit = TransportToSpeckle(server, stream, lst, message)
