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

import sys
from typing import Union




from abstract.segmentation import Meshable, TesselationSettings
from abstract.vector import Vector
from geometry.curve import PolyCurve, Polygon
from geometry.mesh import Mesh
from abstract.vector import Point
from geometry.solid import Extrusion
from library.material import Material, BaseOther
from library.profile import get_profile_by_name, justificationToVector

from abstract.serializable import Serializable
from abstract.node import Node
from construction.profile import Profile, Rectangle

# [!not included in BP singlefile - end]




# ToDo Na update van color moet ook de colorlist geupdate worden
class Beam(Serializable, Meshable):
    def __init__(self):
        self.name = "None"
        self.profileName = "None"
        self.extrusion = None
        self.comments = None
        self.structuralType = None
        self.start = None
        self.end = None
        self.curve = None  # 2D polycurve of the sectionprofile
        self.YJustification = "Origin"  # Top, Center, Origin, Bottom
        self.ZJustification = "Origin"  # Left, Center, Origin, Right
        self.YOffset = 0
        self.ZOffset = 0
        self.rotation = 0
        self.material : Material = None
        self.color = BaseOther.color
        self.profile_data = None #2D polycurve of the sectionprofile (DOUBLE TO BE REMOVED)
        self.profile = None #object of 2D profile
        self.centerbottom = None

    def to_mesh(self, settings: TesselationSettings) -> Mesh:
        return self.extrusion.to_mesh(settings)
  
    @classmethod
    def by_startpoint_endpoint(cls, start: Union[Point, Node], end: Union[Point, Node], profile: Union[str, Profile], name: str, material: None, comments=None):
        f1 = Beam()
        f1.comments = comments

        if isinstance(start, Point):
            f1.start = start
        elif isinstance(start, Node):
            f1.start = start.point
        if isinstance(end, Point):
            f1.end = end
        elif isinstance(end, Node):
            f1.end = end.point

        if isinstance(profile,Profile):
            f1.curve = profile.curve
            f1.profile = profile
        elif isinstance(profile, str):
            res = get_profile_by_name(profile)
            f1.curve = res.curve  # polycurve2d
            f1.profile = res
        else:
            print("[by_startpoint_endpoint_profile], input is not correct.")
            sys.exit()

        f1.name = name
        f1.extrusion = Extrusion.by_2d_polycurve_height_vector(
            f1.curve, f1.start, f1.end - f1.start)
        f1.extrusion.name = name
        f1.profileName = profile
        f1.material = material
        f1.color = material.colorint
        return f1

    @classmethod
    def by_startpoint_endpoint_profile_shapevector(cls, start: Union[Point, Node], end: Union[Point, Node], profile_name: str, name: str, vector2d: Vector, rotation: float, material: None, comments: None):
        f1 = Beam()
        f1.comments = comments

        if isinstance(start, Point):
            f1.start = start
        elif isinstance(start, Node):
            f1.start = start.point
        if isinstance(end, Point):
            f1.end = end
        elif isinstance(end, Node):
            f1.end = end.point
            
        #try:
        curv = get_profile_by_name(profile_name).curve
        #except Exception as e:
            # Profile does not exist
        #print(f"Profile does not exist: {profile_name}\nError: {e}")

        f1.rotation = rotation
        curvrot = curv.rotate(rotation)  # rotation in degrees
        f1.curve = curvrot.translate(vector2d)
        f1.XOffset = vector2d.x
        f1.YOffset = vector2d.y
        f1.name = name
        f1.extrusion = Extrusion.by_2d_polycurve_height_vector(
            f1.curve, f1.start, f1.end - f1.start)
        f1.extrusion.name = name
        f1.profileName = profile_name
        f1.material = material
        f1.color = material.colorint
        return f1

    @classmethod
    def by_startpoint_endpoint_profile_justification(cls, start: Union[Point, Node], end: Union[Point, Node], profile: Union[str, PolyCurve], name: str, XJustifiction: str, YJustifiction: str, rotation: float, material=None, ey: None = float, ez: None = float, structuralType: None = str, comments=None):
        f1 = Beam()
        f1.comments = comments

        if isinstance(start, Point):
            f1.start = start
        elif isinstance(start, Node):
            f1.start = start.point
        if isinstance(end, Point):
            f1.end = end
        elif isinstance(end, Node):
            f1.end = end.point

        f1.structuralType = structuralType
        f1.rotation = rotation

        if isinstance(profile, PolyCurve):
            profile_name = "None"
            f1.profile_data = profile
            curve = f1.profile_data
        elif isinstance(profile, Polygon):
            profile_name = "None"
            f1.profile_data = PolyCurve.by_points(profile.points)
            curve = f1.profile_data
        elif isinstance(profile, str):
            profile_name = profile
            f1.profile_data = get_profile_by_name(profile).curve  # polycurve2d
            curve = f1.profile_data
        else:
            print("[by_startpoint_endpoint_profile], input is not correct.")
            sys.exit()

        # curve = f1.profile_data.polycurve2d

        v1 = justificationToVector(curve, XJustifiction, YJustifiction)  # 1
        f1.XOffset = v1.x
        f1.YOffset = v1.y
        curve = curve.translate(v1)
        curve = curve.translate(Vector(ey, ez))  # 2
        curve = curve.rotate(f1.rotation)  # 3
        f1.curve = curve

        f1.name = name
        f1.extrusion = Extrusion.by_2d_polycurve_height_vector(
            f1.curve, f1.start, f1.end - f1.start)
        f1.extrusion.name = name

        try:
            pnew = PolyCurve.by_joined_curves(f1.curve3d.curves)
            f1.centerbottom = PolyCurve.centroid(pnew)
        except:
            pass

        f1.profileName = profile_name
        f1.material = material
        f1.color = material.colorint
        return f1

    @classmethod
    def by_startpoint_endpoint_rect(cls, start: Union[Point, Node], end: Union[Point, Node], width: float, height: float, name: str, rotation: float, material=None, comments=None):
        # 2D polycurve
        f1 = Beam()
        f1.comments = comments

        if isinstance(start, Point):
            f1.start = start
        elif isinstance(start, Node):
            f1.start = start.point
        if isinstance(end, Point):
            f1.end = end
        elif isinstance(end, Node):
            f1.end = end.point

        f1.name = name

        prof = Rectangle(str(width)+"x"+str(height),width,height)
        polycurve = prof.curve
        f1.profile = prof
        curvrot = polycurve.rotate(rotation)
        f1.extrusion = Extrusion.by_2d_polycurve_height_vector(
            curvrot, f1.start, f1.end - f1.start)
        f1.extrusion.name = name
        f1.profileName = name
        f1.material = material
        f1.color = material.colorint
        return f1


    @classmethod
    def by_point_height_rotation(cls, start: Union[Point, Node], height: float, polycurve: PolyCurve, frame_name: str, rotation: float, material=None, comments=None):
        # 2D polycurve
        f1 = Beam()
        f1.comments = comments

        if isinstance(start, Point):
            f1.start = start
        elif isinstance(start, Node):
            f1.start = start.point

        f1.end = Point.translate(f1.start, Vector(0, 0.00001, height))

        # self.curve = Line(start, end)
        f1.name = frame_name
        f1.profileName = frame_name
        curvrot = polycurve.rotate(rotation)  # rotation in degrees
        f1.extrusion = Extrusion.by_2d_polycurve_height_vector(
            curvrot, f1.start, f1.end - f1.start)
        f1.extrusion.name = frame_name
        f1.material = material
        f1.color = material.colorint
        return f1

    @classmethod
    def by_point_profile_height_rotation(cls, start: Union[Point, Node], height: float, profile_name: str, rotation: float, material=None, comments=None):
        f1 = Beam()
        f1.comments = comments

        if isinstance(start, Point):
            f1.start = start
        elif isinstance(start, Node):
            f1.start = start.point
        # TODO vertical column not possible
        f1.end = Point.translate(f1.start, Vector(0, height))

        # self.curve = Line(start, end)
        f1.name = profile_name
        f1.profileName = profile_name
        curv = get_profile_by_name(profile_name).curve
        curvrot = curv.rotate(rotation)  # rotation in degrees
        f1.extrusion = Extrusion.by_2d_polycurve_height_vector(
            curvrot.curves, f1.start, f1.end - f1.start)
        f1.extrusion.name = profile_name
        f1.profileName = profile_name
        f1.material = material
        f1.color = material.colorint
        return f1

    @classmethod
    def by_startpoint_endpoint_curve_justification(cls, start: Union[Point, Node], end: Union[Point, Node], polycurve: PolyCurve, name: str, XJustifiction: str, YJustifiction: str, rotation: float, material=None, comments=None):
        f1 = Beam()
        f1.comments = comments

        if isinstance(start, Point):
            f1.start = start
        elif isinstance(start, Node):
            f1.start = start.point
        if isinstance(end, Point):
            f1.end = end
        elif isinstance(end, Node):
            f1.end = end.point

        f1.rotation = rotation
        curv = polycurve
        curvrot = curv.rotate(rotation)  # rotation in degrees
        # center, left, right, origin / center, top bottom, origin
        v1 = justificationToVector(curvrot, XJustifiction, YJustifiction)
        f1.XOffset = v1.x
        f1.YOffset = v1.y
        f1.curve = curv.translate(v1)
        f1.name = name
        f1.extrusion = Extrusion.by_2d_polycurve_height_vector(
            f1.curve.curves, f1.start, f1.end - f1.start)
        f1.extrusion.name = name
        f1.profileName = "none"
        f1.material = material
        f1.color = material.colorint

        return f1

    def write(self, project):
        project.objects.append(self)
        return self

Column = Beam
#columns and beams are the same, the profiles are the same, but they function as beams or columns.