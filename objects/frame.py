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


"""This module provides tools for the modelling of framing components. Almost every object in a building is a frame
"""

__title__= "shape"
__author__ = "Maarten & Jonathan"
__url__ = "./objects/frame.py"


import sys, os, math
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))


from library.profile import *
from library.profile import profiledataToShape, justifictionToVector
from geometry.geometry2d import *
from library.material import *
from abstract.vector import *
from abstract.coordinatesystem import *
from abstract.node import *
from geometry.solid import *

# [!not included in BP singlefile - end]

def colorlist(extrus,color):
    colorlst = []
    for j in range(int(len(extrus.verts) / 3)):
        colorlst.append(color)
    return(colorlst)


# ToDo Na update van color moet ook de colorlist geupdate worden
class Frame:
    def __init__(self):
        self.id = generateID()
        self.type = __class__.__name__
        self.name = "None"
        self.profileName = "None"
        self.extrusion = None
        self.comments = None        
        self.structuralType = None
        self.start = None
        self.end = None
        self.curve = None # 2D polycurve of the sectionprofile
        self.curve3d = None # Translated 3D polycurve of the sectionprofile
        self.length = 0
        self.coordinateSystem: CoordinateSystem = CSGlobal
        self.YJustification = "Origin"  #Top, Center, Origin, Bottom
        self.ZJustification = "Origin" #Left, Center, Origin, Right
        self.YOffset = 0
        self.ZOffset = 0
        self.rotation = 0
        self.material = None
        self.color = BaseOther.color
        self.colorlst = []
        self.vector = None
        self.vector_normalised = None

    def serialize(self):
        id_value = str(self.id) if not isinstance(self.id, (str, int, float)) else self.id
        return {
            'id': id_value,
            'type': self.type,
            'name': self.name,
            'profileName': self.profileName,
            'extrusion': self.extrusion,
            'comments': self.comments,
            'structuralType': self.structuralType,
            'start': self.start,
            'end': self.end,
            'curve': self.curve,
            'curve3d': self.curve3d,
            'length': self.length,
            'coordinateSystem': self.coordinateSystem.serialize(),
            'YJustification': self.YJustification,
            'ZJustification': self.ZJustification,
            'YOffset': self.YOffset,
            'ZOffset': self.ZOffset,
            'rotation': self.rotation,
            'material': self.material,
            'color': self.color,
            'colorlst': self.colorlst,
            'vector': self.vector.serialize() if self.vector else None,
            'vector_normalised': self.vector_normalised.serialize() if self.vector_normalised else None
        }

    @staticmethod
    def deserialize(data):
        frame = Frame()
        frame.id = data.get('id')
        frame.type = data.get('type')
        frame.name = data.get('name', "None")
        frame.profileName = data.get('profileName', "None")
        frame.extrusion = data.get('extrusion')
        frame.comments = data.get('comments')
        frame.structuralType = data.get('structuralType')
        frame.start = data.get('start')
        frame.end = data.get('end')
        frame.curve = data.get('curve')
        frame.curve3d = data.get('curve3d')
        frame.length = data.get('length', 0)
        frame.coordinateSystem = CoordinateSystem.deserialize(data['coordinateSystem'])
        frame.YJustification = data.get('YJustification', "Origin")
        frame.ZJustification = data.get('ZJustification', "Origin")
        frame.YOffset = data.get('YOffset', 0)
        frame.ZOffset = data.get('ZOffset', 0)
        frame.rotation = data.get('rotation', 0)
        frame.material = data.get('material')
        frame.color = data.get('color', BaseOther.color)
        frame.colorlst = data.get('colorlst', [])
        frame.vector = Vector3.deserialize(data['vector']) if 'vector' in data else None
        frame.vector_normalised = Vector3.deserialize(data['vector_normalised']) if 'vector_normalised' in data else None

        return frame


    def props(self):
        self.vector = Vector3(self.end.x-self.start.x,self.end.y-self.start.y,self.end.z-self.start.z)
        self.vector_normalised = Vector3.normalize(self.vector)
        self.length = Vector3.length(self.vector)

    @classmethod
    def byStartpointEndpointProfileName(cls, start: Point or Node, end: Point or Node, profile_name: str, name: str, material: None, comments = None):
        # [!not included in BP singlefile - start]
        from library.profile import profiledataToShape
        # [!not included in BP singlefile - end]
        f1 = Frame()
        f1.comments = comments

        if start.type == 'Point':
            f1.start = start
        elif start.type == 'Node':
            f1.start = start.point
        if end.type == 'Point':
            f1.end = end
        elif end.type == 'Node':
            f1.end = end.point

        f1.curve = profiledataToShape(profile_name).polycurve2d #polycurve2d
        f1.directionVector = Vector3.byTwoPoints(f1.start, f1.end)
        f1.length = Vector3.length(f1.directionVector)
        f1.name = name
        f1.extrusion = Extrusion.byPolyCurveHeightVector(f1.curve, f1.length, CSGlobal, f1.start, f1.directionVector)
        f1.extrusion.name = name
        f1.curve3d = f1.extrusion.polycurve_3d_translated
        f1.profileName = profile_name
        f1.material = material
        f1.color = material.colorint
        f1.colorlst = colorlist(f1.extrusion, f1.color)
        f1.props()
        return f1

    @classmethod
    def byStartpointEndpointProfileNameShapevector(cls, start: Point or Node, end: Point or Node, profile_name: str, name: str, vector2d: Vector2, rotation: float, material: None, comments: None):
        f1 = Frame()
        f1.comments = comments

        if start.type == 'Point':
            f1.start = start
        elif start.type == 'Node':
            f1.start = start.point
        if end.type == 'Point':
            f1.end = end
        elif end.type == 'Node':
            f1.end = end.point

        try:
            curv = profiledataToShape(profile_name).polycurve2d
        except:
            print(f"Profile does not exist: {profile_name}") #Profile does not exist
        f1.rotation = rotation
        curvrot = curv.rotate(rotation)  # rotation in degrees
        f1.curve = curvrot.translate(vector2d)
        f1.XOffset = vector2d.x
        f1.YOffset = vector2d.y
        f1.directionVector = Vector3.byTwoPoints(f1.start, f1.end)
        f1.length = Vector3.length(f1.directionVector)
        f1.name = name
        f1.extrusion = Extrusion.byPolyCurveHeightVector(f1.curve, f1.length, CSGlobal, f1.start, f1.directionVector)
        f1.extrusion.name = name
        f1.curve3d = f1.extrusion.polycurve_3d_translated
        f1.profileName = profile_name
        f1.material = material
        f1.color = material.colorint
        f1.colorlst = colorlist(f1.extrusion, f1.color)
        f1.props()
        return f1

    @classmethod
    def byStartpointEndpointProfileNameJustifiction(cls, start: Point or Node, end: Point or Node, profile_name: str, name: str, XJustifiction: str, YJustifiction: str, rotation: float, material = None, ey: None = float, ez: None = float, structuralType: None = str, comments = None):
        f1 = Frame()
        f1.comments = comments

        if start.type == 'Point':
            f1.start = start
        elif start.type == 'Node':
            f1.start = start.point
        if end.type == 'Point':
            f1.end = end
        elif end.type == 'Node':
            f1.end = end.point

        f1.structuralType = structuralType
        f1.rotation = rotation

        curv = profiledataToShape(profile_name).polycurve2d
        curv = curv.translate(Vector2(ey, ez))

        # print(rotation)
        curvrot = curv.rotate(rotation)  # rotation in degrees

        v1 = justifictionToVector(curvrot, XJustifiction, YJustifiction)
        f1.XOffset = v1.x
        f1.YOffset = v1.y
        f1.curve = curvrot.translate(v1)
        f1.directionVector = Vector3.byTwoPoints(f1.start, f1.end)
        f1.length = Vector3.length(f1.directionVector)
        f1.name = name
        f1.extrusion = Extrusion.byPolyCurveHeightVector(f1.curve, f1.length, CSGlobal, f1.start, f1.directionVector)
        f1.extrusion.name = name
        f1.curve3d = f1.extrusion.polycurve_3d_translated
        f1.profileName = profile_name
        f1.material = material
        f1.color = material.colorint
        f1.colorlst = colorlist(f1.extrusion, f1.color)
        f1.props()
        return f1

            # print(profile_name) #Profile does not exist
        # curv = profiledataToShape(profile_name).prof.curve



    @classmethod
    def byStartpointEndpoint(cls, start: Point or Node, end: Point or Node, polycurve: PolyCurve2D, name: str, rotation: float, material = None, comments=None):
        # 2D polycurve
        f1 = Frame()
        f1.comments = comments

        if start.type == 'Point':
            f1.start = start
        elif start.type == 'Node':
            f1.start = start.point
        if end.type == 'Point':
            f1.end = end
        elif end.type == 'Node':
            f1.end = end.point

        # self.curve = Line(start, end)
        f1.directionVector = Vector3.byTwoPoints(f1.start, f1.end)
        f1.length = Vector3.length(f1.directionVector)
        f1.name = name
        curvrot = polycurve.rotate(rotation)  # rotation in degrees
        f1.extrusion = Extrusion.byPolyCurveHeightVector(curvrot, f1.length, CSGlobal, f1.start, f1.directionVector)
        f1.extrusion.name = name
        f1.curve3d = curvrot
        f1.profileName = name
        f1.material = material
        f1.color = material.colorint
        f1.colorlst = colorlist(f1.extrusion, f1.color)
        f1.props()
        return f1

    @classmethod
    def by_point_height_rotation(cls, start: Point or Node, height: float, polycurve: PolyCurve2D, frame_name: str, rotation: float, material = None, comments=None):
        # 2D polycurve
        f1 = Frame()
        f1.comments = comments

        if start.type == 'Point':
            f1.start = start
        elif start.type == 'Node':
            f1.start = start.point

        f1.end = Point.translate(f1.start,Vector3(0,0.00001,height))

        # self.curve = Line(start, end)
        f1.directionVector = Vector3.byTwoPoints(f1.start, f1.end)
        f1.length = Vector3.length(f1.directionVector)
        f1.name = frame_name
        f1.profileName = frame_name
        curvrot = polycurve.rotate(rotation)  # rotation in degrees
        f1.extrusion = Extrusion.byPolyCurveHeightVector(curvrot, f1.length, CSGlobal, f1.start, f1.directionVector)
        f1.extrusion.name = frame_name
        f1.curve3d = curvrot
        f1.material = material
        f1.color = material.colorint
        f1.colorlst = colorlist(f1.extrusion, f1.color)
        f1.props()
        return f1

    @classmethod
    def by_point_profile_height_rotation(cls, start: Point or Node, height: float, profile_name: str, rotation: float, material = None, comments=None):
        f1 = Frame()
        f1.comments = comments

        if start.type == 'Point':
            f1.start = start
        elif start.type == 'Node':
            f1.start = start.point
        f1.end = Point.translate(f1.start,Vector3(0,0.00001,height)) #TODO vertical column not possible

        # self.curve = Line(start, end)
        f1.directionVector = Vector3.byTwoPoints(f1.start, f1.end)
        f1.length = Vector3.length(f1.directionVector)
        f1.name = profile_name
        f1.profileName = profile_name
        curv = profiledataToShape(profile_name).polycurve2d
        curvrot = curv.rotate(rotation)  # rotation in degrees
        f1.extrusion = Extrusion.byPolyCurveHeightVector(curvrot.curves, f1.length, CSGlobal, f1.start, f1.directionVector)
        f1.extrusion.name = profile_name
        f1.curve3d = curvrot
        f1.profileName = profile_name
        f1.material = material
        f1.color = material.colorint
        f1.colorlst = colorlist(f1.extrusion, f1.color)
        f1.props()
        return f1


    @classmethod
    def byStartpointEndpointCurveJustifiction(cls, start: Point or Node, end: Point or Node, polycurve: PolyCurve2D, name: str, XJustifiction: str, YJustifiction: str, rotation: float, material = None, comments=None):
        f1 = Frame()
        f1.comments = comments

        if start.type == 'Point':
            f1.start = start
        elif start.type == 'Node':
            f1.start = start.point
        if end.type == 'Point':
            f1.end = end
        elif end.type == 'Node':
            f1.end = end.point

        # self.curve = Line(star
        # t, end)
        f1.rotation = rotation
        curv = polycurve
        curvrot = curv.rotate(rotation)  # rotation in degrees
        v1 = justifictionToVector(curvrot, XJustifiction, YJustifiction) #center, left, right, origin / center, top bottom, origin
        f1.XOffset = v1.x
        f1.YOffset = v1.y
        f1.curve = curv.translate(v1)
        f1.directionVector = Vector3.byTwoPoints(f1.start, f1.end)
        f1.length = Vector3.length(f1.directionVector)
        f1.name = name
        f1.extrusion = Extrusion.byPolyCurveHeightVector(f1.curve.curves, f1.length, CSGlobal, f1.start, f1.directionVector)
        f1.extrusion.name = name
        f1.profileName = "none"
        f1.material = material
        f1.color = material.colorint
        f1.colorlst = colorlist(f1.extrusion, f1.color)
        f1.props()
        return f1

    def write(self,project):
        project.objects.append(self)
        return self