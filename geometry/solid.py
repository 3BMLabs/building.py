# [included in BP singlefile]
# [!not included in BP singlefile - start]
# -*- coding: utf8 -*-
#***************************************************************************
#*   Copyright (c) 2024 Maarten Vroegindeweij & Jonathan van der Gouwe      *
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


"""This module provides tools to create solids
"""

__title__= "solid"
__author__ = "Maarten & Jonathan"
__url__ = "./geometry/solid.py"


import sys
from pathlib import Path

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

from geometry.curve import *
from geometry.geometry2d import PolyCurve2D
from abstract.plane import *
import helper

# [!not included in BP singlefile - end]

class Extrusion:
    #Extrude a 2D profile to a 3D mesh or solid
    def __init__(self):
        self.id = generateID()
        self.type = __class__.__name__
        self.parameters = []
        self.verts = []
        self.faces = []
        self.numberFaces = 0
        self.countVertsFaces = 0 # total number of verts per face (not the same as total verts)
        self.name = None
        self.color = (255,255,0)
        self.colorlst = []
        self.topface = None #return polycurve -> surface
        self.bottomface = None #return polycurve -> surface
        self.polycurve_3d_translated = None
        self.bottomshape = []


    def serialize(self):
        id_value = str(self.id) if not isinstance(self.id, (str, int, float)) else self.id
        return {
            'id': id_value,
            'type': self.type,
            'verts': self.verts,
            'faces': self.faces,
            'numberFaces': self.numberFaces,
            'countVertsFaces': self.countVertsFaces,
            'name': self.name,
            'color': self.color,
            'colorlst': self.colorlst,
            'topface': self.topface.serialize() if self.topface else None,
            'bottomface': self.bottomface.serialize() if self.bottomface else None,
            'polycurve_3d_translated': self.polycurve_3d_translated.serialize() if self.polycurve_3d_translated else None
        }


    @staticmethod
    def deserialize(data):
        extrusion = Extrusion()
        extrusion.id = data.get('id')
        extrusion.verts = data.get('verts', [])
        extrusion.faces = data.get('faces', [])
        extrusion.numberFaces = data.get('numberFaces', 0)
        extrusion.countVertsFaces = data.get('countVertsFaces', 0)
        extrusion.name = data.get('name', "none")
        extrusion.color = data.get('color', (255,255,0))
        extrusion.colorlst = data.get('colorlst', [])

        if data.get('topface'):
            extrusion.topface = PolyCurve.deserialize(data['topface'])
        
        if data.get('bottomface'):
            extrusion.bottomface = PolyCurve.deserialize(data['bottomface'])
        
        if data.get('polycurve_3d_translated'):
            extrusion.polycurve_3d_translated = PolyCurve.deserialize(data['polycurve_3d_translated'])

        return extrusion


    def setParameter(self, data):
        self.parameters = data
        return self


    @classmethod
    def merge(self, extrusions:list, name=None):
        Outrus = Extrusion()
        if isinstance(extrusions, list):
            Outrus.verts = []
            Outrus.faces = []
            Outrus.colorlst = []
            for ext in extrusions:
                Outrus.verts.append(ext.verts)
                Outrus.faces.append(ext.faces)
                Outrus.colorlst.append(ext.colorlst)
            Outrus.verts = flatten(Outrus.verts)
            Outrus.faces = flatten(Outrus.faces)
            Outrus.colorlst = flatten(Outrus.colorlst)
            return Outrus

        elif isinstance(extrusions, Extrusion):
            return extrusions


    @classmethod
    def byPolyCurveHeightVector(self, polycurve2d: PolyCurve2D, height, CSOld, startpoint, DirectionVector: Vector3):
        Extrus = Extrusion()
        #2D PolyCurve @ Global origin
        count = 0
        
        Extrus.polycurve_3d_translated = PolyCurve.transform_from_origin(polycurve2d,startpoint,DirectionVector)
        
        try:
            for i in polycurve2d.curves:
                startpointLow = transform_point(Point(i.start.x,i.start.y,0), CSOld, startpoint, DirectionVector)
                endpointLow = transform_point(Point(i.end.x,i.end.y,0), CSOld, startpoint, DirectionVector)
                endpointHigh = transform_point(Point(i.end.x,i.end.y,height), CSOld, startpoint, DirectionVector)
                startpointHigh = transform_point(Point(i.start.x,i.start.y,height), CSOld, startpoint, DirectionVector)

                #Construct faces perpendicular on polycurve
                Extrus.faces.append(4)
                Extrus.verts.append(startpointLow.x)
                Extrus.verts.append(startpointLow.y)
                Extrus.verts.append(startpointLow.z)
                Extrus.faces.append(count)
                count += 1
                Extrus.verts.append(endpointLow.x)
                Extrus.verts.append(endpointLow.y)
                Extrus.verts.append(endpointLow.z)
                Extrus.faces.append(count)
                count += 1
                Extrus.verts.append(endpointHigh.x)
                Extrus.verts.append(endpointHigh.y)
                Extrus.verts.append(endpointHigh.z)
                Extrus.faces.append(count)
                count += 1
                Extrus.verts.append(startpointHigh.x)
                Extrus.verts.append(startpointHigh.y)
                Extrus.verts.append(startpointHigh.z)
                Extrus.faces.append(count)
                count += 1
                Extrus.numberFaces = Extrus.numberFaces + 1

            #bottomface
            Extrus.faces.append(len(polycurve2d.curves))

            count = 0
            for i in polycurve2d.curves:
                Extrus.faces.append(count)
                Extrus.bottomshape.append(i)
                count = count + 4
            

            # topface
            Extrus.faces.append(len(polycurve2d.curves))
            count = 3
            for i in polycurve2d.curves:
                Extrus.faces.append(count)
                count = count + 4
        except:
            for i in polycurve2d.curves:
                startpointLow = transform_point(Point(i.start.x,i.start.y,0), CSOld, startpoint, DirectionVector)
                endpointLow = transform_point(Point(i.end.x,i.end.y,0), CSOld, startpoint, DirectionVector)
                endpointHigh = transform_point(Point(i.end.x,i.end.y,height), CSOld, startpoint, DirectionVector)
                startpointHigh = transform_point(Point(i.start.x,i.start.y,height), CSOld, startpoint, DirectionVector)

                #Construct faces perpendicular on polycurve
                Extrus.faces.append(4)
                Extrus.verts.append(startpointLow.x)
                Extrus.verts.append(startpointLow.y)
                Extrus.verts.append(startpointLow.z)
                Extrus.faces.append(count)
                count += 1
                Extrus.verts.append(endpointLow.x)
                Extrus.verts.append(endpointLow.y)
                Extrus.verts.append(endpointLow.z)
                Extrus.faces.append(count)
                count += 1
                Extrus.verts.append(endpointHigh.x)
                Extrus.verts.append(endpointHigh.y)
                Extrus.verts.append(endpointHigh.z)
                Extrus.faces.append(count)
                count += 1
                Extrus.verts.append(startpointHigh.x)
                Extrus.verts.append(startpointHigh.y)
                Extrus.verts.append(startpointHigh.z)
                Extrus.faces.append(count)
                count += 1
                Extrus.numberFaces = Extrus.numberFaces + 1

            #bottomface
            Extrus.faces.append(len(polycurve2d.curves))

            count = 0
            for i in polycurve2d.curves:
                Extrus.faces.append(count)
                Extrus.bottomshape.append(i)
                count = count + 4
            

            # topface
            Extrus.faces.append(len(polycurve2d.curves))
            count = 3
            for i in polycurve2d.curves:
                Extrus.faces.append(count)
                count = count + 4

        Extrus.countVertsFaces = (4 * Extrus.numberFaces)

        Extrus.countVertsFaces = Extrus.countVertsFaces + len(polycurve2d.curves)*2
        Extrus.numberFaces = Extrus.numberFaces + 2

        for j in range(int(len(Extrus.verts) / 3)):
            Extrus.colorlst.append(Extrus.color)

        return Extrus


    @classmethod
    def byPolyCurveHeight(self, polycurve: PolyCurve, height, dzloc: float):
        #global len
        Extrus = Extrusion()
        Points = polycurve.points
        V1 = Vector3.byTwoPoints(Points[0], Points[1])
        V2 = Vector3.byTwoPoints(Points[-2], Points[-1])

        p1 = Plane.byTwoVectorsOrigin(V1, V2, Points[0]) #Workplane of PolyCurve
        norm = p1.Normal

        pnts = []
        faces = []

        Extrus.polycurve_3d_translated = polycurve

        #allverts
        for pnt in Points:
            pnts.append(Point.translate(pnt, Vector3.product(dzloc, norm))) # Onderzijde verplaatst met dzloc
        for pnt in Points:
            pnts.append(Point.translate(pnt, Vector3.product((dzloc+height), norm)))  # Bovenzijde verplaatst met dzloc

        numPoints = len(Points)

        #Bottomface
        count = 0
        face = []
        for x in range(numPoints):
            face.append(count)
            count = count + 1
        faces.append(face)

        # Topface
        count = 0
        face = []
        for x in range(numPoints):
            face.append(count+numPoints)
            count = count + 1
        faces.append(face)

        # Sides
        count = 0
        length = len(faces[0])
        for i,j in zip(faces[0],faces[1]):
            face = []
            face.append(i)
            face.append(faces[0][count + 1])
            face.append(faces[1][count + 1])
            face.append(j)
            count = count + 1
            if count == length-1:
                face.append(i)
                face.append(faces[0][0])
                face.append(faces[1][0])
                face.append(j)
                faces.append(face)
                break
            else:
                pass
            faces.append(face)

        #toMeshStructure
        for i in pnts:
            Extrus.verts.append(i.x)
            Extrus.verts.append(i.y)
            Extrus.verts.append(i.z)

        for x in faces:
            Extrus.faces.append(len(x)) #Number of verts in face
            for y in x:
                Extrus.faces.append(y)

        Extrus.numberFaces = len(faces)
        Extrus.countVertsFaces = (4 * len(faces))

        for j in range(int(len(Extrus.verts) / 3)):
            Extrus.colorlst.append(Extrus.color)
        return Extrus