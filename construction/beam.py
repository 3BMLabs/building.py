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


"""This module provides tools for the modelling of framing components. Almost every object in a building is a frame"""

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
from library.material import BaseSteel, Material, BaseOther
from library.profile import profile_by_name, justification_to_vector

from abstract.serializable import Serializable
from abstract.node import Node
from construction.profile import Profile, RectangleProfile

# [!not included in BP singlefile - end]


# ToDo Na update van color moet ook de colorlist geupdate worden
class Beam(Serializable, Meshable):
    def __init__(self, start: Point, end: Point, profile: Profile, material: Material = BaseSteel, justification: Vector = Vector()):
        self.name = "None"
        self.comments = None
        self.start = start
        self.end = end
        self.profile = profile
        self.justification = justification
        self.material = material

        self.rotation = 0

        self.profile_data = (
            None  # 2D polycurve of the sectionprofile (DOUBLE TO BE REMOVED)
        )
        self.centerbottom = None

    def to_mesh(self, settings: TesselationSettings) -> Mesh:
        return self.extrusion.to_mesh(settings)

    @classmethod
    def by_startpoint_endpoint(
        cls,
        start: Union[Point, Node],
        end: Union[Point, Node],
        profile: Profile,
        name: str,
        material: None,
    ):
        beam = Beam(start, end, profile, material, Vector())
        beam.name = name
        return name

    @classmethod
    def by_startpoint_endpoint_profile_shapevector(
        cls,
        start: Union[Point, Node],
        end: Union[Point, Node],
        profile_name: str,
        name: str,
        vector2d: Vector,
        rotation: float,
        material: None,
        comments: None,
    ):
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

        # try:
        curv = profile_by_name(profile_name).curve
        # except Exception as e:
        # Profile does not exist
        # print(f"Profile does not exist: {profile_name}\nError: {e}")

        f1.rotation = rotation
        curvrot = curv.rotate(rotation)  # rotation in degrees
        f1.curve = curvrot.translate(vector2d)
        f1.XOffset = vector2d.x
        f1.YOffset = vector2d.y
        f1.name = name
        f1.extrusion = Extrusion.by_2d_polycurve_vector(
            f1.curve, f1.start, f1.end - f1.start
        )
        f1.extrusion.name = name
        f1.material = material
        return f1

    @classmethod
    def by_startpoint_endpoint_profile_justification(
        cls,
        start: Union[Point, Node],
        end: Union[Point, Node],
        profile: Union[str, PolyCurve],
        name: str,
        XJustifiction: str,
        YJustifiction: str,
        rotation: float,
        material=None,
        ey: None = float,
        ez: None = float,
        comments=None,
    ):
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
            f1.profile_data = profile_by_name(profile).curve  # polycurve2d
            curve = f1.profile_data
        else:
            print("[by_startpoint_endpoint_profile], input is not correct.")
            sys.exit()

        # curve = f1.profile_data.polycurve2d

        v1 = justification_to_vector(curve, XJustifiction, YJustifiction)  # 1
        f1.XOffset = v1.x
        f1.YOffset = v1.y
        curve = curve.translate(v1)
        curve = curve.translate(Vector(ey, ez))  # 2
        curve = curve.rotate(f1.rotation)  # 3
        f1.curve = curve

        f1.name = name
        f1.extrusion = Extrusion.by_2d_polycurve_vector(
            f1.curve, f1.start, f1.end - f1.start
        )
        f1.extrusion.name = name

        try:
            pnew = PolyCurve.by_joined_curves(f1.curve3d.curves)
            f1.centerbottom = PolyCurve.centroid(pnew)
        except:
            pass

        f1.material = material
        return f1

    @classmethod
    def by_point_height_rotation(
        cls,
        start: Union[Point, Node],
        height: float,
        polycurve: PolyCurve,
        frame_name: str,
        rotation: float,
        material=None,
        comments=None,
    ):
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
        curvrot = polycurve.rotate(rotation)  # rotation in degrees
        f1.extrusion = Extrusion.by_2d_polycurve_vector(
            curvrot, f1.start, f1.end - f1.start
        )
        f1.extrusion.name = frame_name
        f1.material = material

        return f1

    @classmethod
    def by_point_profile_height_rotation(
        cls,
        start: Union[Point, Node],
        height: float,
        profile_name: str,
        rotation: float,
        material=None,
        comments=None,
    ):
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
        curv = profile_by_name(profile_name).curve
        curvrot = curv.rotate(rotation)  # rotation in degrees
        f1.extrusion = Extrusion.by_2d_polycurve_vector(
            curvrot.curves, f1.start, f1.end - f1.start
        )
        f1.extrusion.name = profile_name
        f1.material = material

        return f1

    @classmethod
    def by_startpoint_endpoint_curve_justification(
        cls,
        start: Union[Point, Node],
        end: Union[Point, Node],
        polycurve: PolyCurve,
        name: str,
        XJustifiction: str,
        YJustifiction: str,
        rotation: float,
        material=None,
        comments=None,
    ):
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
        v1 = justification_to_vector(curvrot, XJustifiction, YJustifiction)
        f1.XOffset = v1.x
        f1.YOffset = v1.y
        f1.curve = curv.translate(v1)
        f1.name = name
        f1.extrusion = Extrusion.by_2d_polycurve_vector(
            f1.curve.curves, f1.start, f1.end - f1.start
        )
        f1.extrusion.name = name
        f1.profileName = "none"
        f1.material = material


        return f1

    def write(self, project):
        project.objects.append(self)
        return self


Column = Beam
# columns and beams are the same, the profiles are the same, but they function as beams or columns.
