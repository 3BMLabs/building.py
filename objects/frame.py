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


"""This module provides tools for the modelling of framing components. Almost every object in a building is a frame
"""

__title__ = "shape"
__author__ = "Maarten & Jonathan"
__url__ = "./objects/frame.py"

import sys, os, math
from pathlib import Path
from typing import Union


sys.path.append(str(Path(__file__).resolve().parents[1]))

from library.profile import *
from library.profile import nameToProfile, justifictionToVector
from geometry.geometry2d import *
from library.material import *
from abstract.vector import *
from abstract.coordinatesystem import *
from objects import profile

from abstract.node import *
from geometry.solid import *
from abstract.serializable import Serializable

# [!not included in BP singlefile - end]

def colorlist(extrus, color):
    colorlst = []
    for j in range(int(len(extrus.verts) / 3)):
        colorlst.append(color)
    return (colorlst)


# ToDo Na update van color moet ook de colorlist geupdate worden
class Frame(Serializable):
    def __init__(self):
        self.id = generateID()
        self.name = "None"
        self.profileName = "None"
        self.extrusion = None
        self.comments = None
        self.structuralType = None
        self.start = None
        self.end = None
        self.curve = None  # 2D polycurve of the sectionprofile
        self.curve3d = None  # Translated 3D polycurve of the sectionprofile
        self.length = 0
        self.points = []
        self.coordinateSystem: CoordinateSystem = CSGlobal
        self.YJustification = "Origin"  # Top, Center, Origin, Bottom
        self.ZJustification = "Origin"  # Left, Center, Origin, Right
        self.YOffset = 0
        self.ZOffset = 0
        self.rotation = 0
        self.material : Material = None
        self.color = BaseOther.color
        self.profile_data = None #2D polycurve of the sectionprofile (DOUBLE TO BE REMOVED)
        self.profile = None #object of 2D profile
        self.colorlst = []
        self.vector = None
        self.vector_normalised = None
        self.centerbottom = None

    def props(self):
        self.vector = Vector(self.end.x-self.start.x,
                              self.end.y-self.start.y, self.end.z-self.start.z)
        self.vector_normalised = Vector.normalize(self.vector)
        self.length = Vector.length(self.vector)

    @classmethod
    def by_startpoint_endpoint(cls, start: Union[Point, Node], end: Union[Point, Node], profile: Union[str, Profile], name: str, material: None, comments=None):
        # [!not included in BP singlefile - start]
        from library.profile import nameToProfile
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

        if isinstance(profile,Profile):
            f1.curve = profile.curve
            f1.profile = profile
        elif type(profile).__name__ == "str":
            res = nameToProfile(profile)
            f1.curve = res.polycurve2d  # polycurve2d
            f1.points = res.polycurve2d.points
            f1.profile = res.profile
        else:
            print("[by_startpoint_endpoint_profile], input is not correct.")
            sys.exit()

        f1.directionVector = Vector.by_two_points(f1.start, f1.end)
        f1.length = Vector.length(f1.directionVector)
        f1.name = name
        f1.extrusion = Extrusion.by_polycurve_height_vector(
            f1.curve, f1.length, CSGlobal, f1.start, f1.directionVector)
        f1.extrusion.name = name
        f1.curve3d = f1.extrusion.polycurve_3d_translated
        f1.profileName = profile
        f1.material = material
        f1.color = material.colorint
        f1.colorlst = colorlist(f1.extrusion, f1.color)
        f1.props()
        return f1

    @classmethod
    def by_startpoint_endpoint_profile_shapevector(cls, start: Union[Point, Node], end: Union[Point, Node], profile_name: str, name: str, vector2d: Vector2, rotation: float, material: None, comments: None):
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
            
        #try:
        curv = nameToProfile(profile_name).polycurve2d
        #except Exception as e:
            # Profile does not exist
        #print(f"Profile does not exist: {profile_name}\nError: {e}")

        f1.rotation = rotation
        curvrot = curv.rotate(rotation)  # rotation in degrees
        f1.curve = curvrot.translate(vector2d)
        f1.XOffset = vector2d.x
        f1.YOffset = vector2d.y
        f1.directionVector = Vector.by_two_points(f1.start, f1.end)
        f1.length = Vector.length(f1.directionVector)
        f1.name = name
        f1.extrusion = Extrusion.by_polycurve_height_vector(
            f1.curve, f1.length, CSGlobal, f1.start, f1.directionVector)
        f1.extrusion.name = name
        f1.curve3d = f1.extrusion.polycurve_3d_translated
        f1.profileName = profile_name
        f1.material = material
        f1.color = material.colorint
        f1.colorlst = colorlist(f1.extrusion, f1.color)
        f1.props()
        return f1

    @classmethod
    def by_startpoint_endpoint_profile_justifiction(cls, start: Union[Point, Node], end: Union[Point, Node], profile: Union[str, PolyCurve2D], name: str, XJustifiction: str, YJustifiction: str, rotation: float, material=None, ey: None = float, ez: None = float, structuralType: None = str, comments=None):
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

        if type(profile).__name__ == "PolyCurve2D":
            profile_name = "None"
            f1.profile_data = profile
            curve = f1.profile_data
        elif type(profile).__name__ == "Polygon":
            profile_name = "None"
            f1.profile_data = PolyCurve2D.by_points(profile.points)
            curve = f1.profile_data
        elif type(profile).__name__ == "str":
            profile_name = profile
            f1.profile_data = nameToProfile(profile).polycurve2d  # polycurve2d
            curve = f1.profile_data
        else:
            print("[by_startpoint_endpoint_profile], input is not correct.")
            sys.exit()

        # curve = f1.profile_data.polycurve2d

        v1 = justifictionToVector(curve, XJustifiction, YJustifiction)  # 1
        f1.XOffset = v1.x
        f1.YOffset = v1.y
        curve = curve.translate(v1)
        curve = curve.translate(Vector2(ey, ez))  # 2
        curve = curve.rotate(f1.rotation)  # 3
        f1.curve = curve

        f1.directionVector = Vector.by_two_points(f1.start, f1.end)
        f1.length = Vector.length(f1.directionVector)
        f1.name = name
        f1.extrusion = Extrusion.by_polycurve_height_vector(
            f1.curve, f1.length, CSGlobal, f1.start, f1.directionVector)
        f1.extrusion.name = name
        f1.curve3d = f1.extrusion.polycurve_3d_translated

        try:
            pnew = PolyCurve.by_joined_curves(f1.curve3d.curves)
            f1.centerbottom = PolyCurve.centroid(pnew)
        except:
            pass

        f1.profileName = profile_name
        f1.material = material
        f1.color = material.colorint
        f1.colorlst = colorlist(f1.extrusion, f1.color)
        f1.props()
        return f1

    @classmethod
    def by_startpoint_endpoint_rect(cls, start: Union[Point, Node], end: Union[Point, Node], width: float, height: float, name: str, rotation: float, material=None, comments=None):
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

        f1.directionVector = Vector.by_two_points(f1.start, f1.end)
        f1.length = Vector.length(f1.directionVector)
        f1.name = name

        prof = Rectangle(str(width)+"x"+str(height),width,height)
        polycurve = prof.curve
        f1.profile = prof
        curvrot = polycurve.rotate(rotation)
        f1.extrusion = Extrusion.by_polycurve_height_vector(
            curvrot, f1.length, CSGlobal, f1.start, f1.directionVector)
        f1.extrusion.name = name
        f1.curve3d = curvrot
        f1.profileName = name
        f1.material = material
        f1.color = material.colorint
        f1.colorlst = colorlist(f1.extrusion, f1.color)
        f1.props()
        return f1


    @classmethod
    def by_point_height_rotation(cls, start: Union[Point, Node], height: float, polycurve: PolyCurve2D, frame_name: str, rotation: float, material=None, comments=None):
        # 2D polycurve
        f1 = Frame()
        f1.comments = comments

        if start.type == 'Point':
            f1.start = start
        elif start.type == 'Node':
            f1.start = start.point

        f1.end = Point.translate(f1.start, Vector(0, 0.00001, height))

        # self.curve = Line(start, end)
        f1.directionVector = Vector.by_two_points(f1.start, f1.end)
        f1.length = Vector.length(f1.directionVector)
        f1.name = frame_name
        f1.profileName = frame_name
        curvrot = polycurve.rotate(rotation)  # rotation in degrees
        f1.extrusion = Extrusion.by_polycurve_height_vector(
            curvrot, f1.length, CSGlobal, f1.start, f1.directionVector)
        f1.extrusion.name = frame_name
        f1.curve3d = curvrot
        f1.material = material
        f1.color = material.colorint
        f1.colorlst = colorlist(f1.extrusion, f1.color)
        f1.props()
        return f1

    @classmethod
    def by_point_profile_height_rotation(cls, start: Union[Point, Node], height: float, profile_name: str, rotation: float, material=None, comments=None):
        f1 = Frame()
        f1.comments = comments

        if start.type == 'Point':
            f1.start = start
        elif start.type == 'Node':
            f1.start = start.point
        # TODO vertical column not possible
        f1.end = Point.translate(f1.start, Vector(0, height))

        # self.curve = Line(start, end)
        f1.directionVector = Vector.by_two_points(f1.start, f1.end)
        f1.length = Vector.length(f1.directionVector)
        f1.name = profile_name
        f1.profileName = profile_name
        curv = nameToProfile(profile_name).polycurve2d
        curvrot = curv.rotate(rotation)  # rotation in degrees
        f1.extrusion = Extrusion.by_polycurve_height_vector(
            curvrot.curves, f1.length, CSGlobal, f1.start, f1.directionVector)
        f1.extrusion.name = profile_name
        f1.curve3d = curvrot
        f1.profileName = profile_name
        f1.material = material
        f1.color = material.colorint
        f1.colorlst = colorlist(f1.extrusion, f1.color)
        f1.props()
        return f1

    @classmethod
    def by_startpoint_endpoint_curve_justifiction(cls, start: Union[Point, Node], end: Union[Point, Node], polycurve: PolyCurve2D, name: str, XJustifiction: str, YJustifiction: str, rotation: float, material=None, comments=None):
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

        f1.rotation = rotation
        curv = polycurve
        curvrot = curv.rotate(rotation)  # rotation in degrees
        # center, left, right, origin / center, top bottom, origin
        v1 = justifictionToVector(curvrot, XJustifiction, YJustifiction)
        f1.XOffset = v1.x
        f1.YOffset = v1.y
        f1.curve = curv.translate(v1)
        f1.directionVector = Vector.by_two_points(f1.start, f1.end)
        f1.length = Vector.length(f1.directionVector)
        f1.name = name
        f1.extrusion = Extrusion.by_polycurve_height_vector(
            f1.curve.curves, f1.length, CSGlobal, f1.start, f1.directionVector)
        f1.extrusion.name = name
        f1.profileName = "none"
        f1.material = material
        f1.color = material.colorint
        f1.colorlst = colorlist(f1.extrusion, f1.color)
        f1.props()
        return f1

    def write(self, project):
        project.objects.append(self)
        return self
