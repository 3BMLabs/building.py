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
from library.profile import profiledataToShape
from geometry.geometry2d import *
from library.material import *
from abstract.vector import *
from abstract.coordinatesystem import *
from geometry.solid import *


def colorlist(extrus,color):
    colorlst = []
    for j in range(int(len(extrus.verts) / 3)):
        colorlst.append(color)
    return(colorlst)


# ToDo Na update van color moet ook de colorlist geupdate worden
class Frame:
    # Frame
    def __init__(self):
        self.extrusion = None
        self.name = "none"
        self.profileName = "none"
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

    def props(self):
        self.vector = Vector3(self.end.x-self.start.x,self.end.y-self.start.y,self.end.z-self.start.z)
        self.vector_normalised = Vector3.normalize(self.vector)
        self.length = Vector3.length(self.vector)

    @classmethod
    def byStartpointEndpointProfileName(cls, start: Point, end: Point, profile_name: str, name: str, material):
        from library.profile import profiledataToShape
        f1 = Frame()
        f1.start = start
        f1.end = end
        # self.curve = Line(start, end)
        f1.curve = profiledataToShape(profile_name).polycurve2d #polycurve2d
        #except:
            #print(profile_name)
        f1.directionVector = Vector3.byTwoPoints(start, end)
        f1.length = Vector3.length(f1.directionVector)
        f1.name = name
        f1.extrusion = Extrusion.byPolyCurveHeightVector(f1.curve, f1.length, CSGlobal, start, f1.directionVector)
        f1.extrusion.name = name
        f1.curve3d = f1.extrusion.polycurve_3d_translated
        f1.profileName = profile_name
        f1.material = material
        f1.color = material.colorint
        f1.colorlst = colorlist(f1.extrusion, f1.color)
        f1.props()
        return f1

    @classmethod
    def byStartpointEndpointProfileNameShapevector(cls, start: Point, end: Point, profile_name: str, name: str, vector2d: Vector2, rotation: float, material = None):
        f1 = Frame()
        f1.start = start
        f1.end = end
        # self.curve = Line(start, end)
        try:
            curv = profiledataToShape(profile_name).polycurve2d
        except:
            pass
            # print(profile_name) #Profile does not exist
        f1.rotation = rotation
        curvrot = curv.rotate(rotation)  # rotation in degrees
        f1.curve = curvrot.translate(vector2d)
        f1.XOffset = vector2d.x
        f1.YOffset = vector2d.y
        f1.directionVector = Vector3.byTwoPoints(start, end)
        f1.length = Vector3.length(f1.directionVector)
        f1.name = name
        f1.extrusion = Extrusion.byPolyCurveHeightVector(f1.curve, f1.length, CSGlobal, start, f1.directionVector)
        f1.extrusion.name = name
        f1.curve3d = f1.extrusion.polycurve_3d_translated
        f1.profileName = profile_name
        f1.material = material
        f1.color = material.colorint
        f1.colorlst = colorlist(f1.extrusion, f1.color)
        f1.props()
        return f1

    @classmethod
    def byStartpointEndpointProfileNameJustifiction(cls, start: Point, end: Point, profile_name: str, name: str, XJustifiction: str, YJustifiction: str, rotation: float, material = None):
        f1 = Frame()
        f1.start = start
        f1.end = end
        # self.curve = Line(start, end)
        f1.rotation = rotation
        curv = profiledataToShape(profile_name).prof.curve
        curvrot = curv.rotate(rotation)  # rotation in degrees
        v1 = justifictionToVector(curvrot, XJustifiction, YJustifiction)
        f1.XOffset = v1.x
        f1.YOffset = v1.y
        f1.curve = curv.translate(v1)
        f1.directionVector = Vector3.byTwoPoints(start, end)
        f1.length = Vector3.length(f1.directionVector)
        f1.name = name
        f1.extrusion = Extrusion.byPolyCurveHeightVector(f1.curve.curves, f1.length, CSGlobal, start, f1.directionVector)
        f1.extrusion.name = name
        f1.curve3d = f1.extrusion.polycurve_3d_translated
        f1.profileName = profile_name
        f1.material = material
        f1.color = material.colorint
        f1.colorlst = colorlist(f1.extrusion, f1.color)
        f1.props()
        return f1


    @classmethod
    def byStartpointEndpoint(cls, start: Point, end: Point, polycurve: PolyCurve2D, name: str, rotation: float, material = None):
        # 2D polycurve
        f1 = Frame()
        f1.start = start
        f1.end = end
        # self.curve = Line(start, end)
        f1.directionVector = Vector3.byTwoPoints(start, end)
        f1.length = Vector3.length(f1.directionVector)
        f1.name = name
        curvrot = polycurve.rotate(rotation)  # rotation in degrees
        f1.extrusion = Extrusion.byPolyCurveHeightVector(curvrot, f1.length, CSGlobal, start, f1.directionVector)
        f1.extrusion.name = name
        f1.curve3d = curvrot
        f1.profileName = name
        f1.material = material
        f1.color = material.colorint
        f1.colorlst = colorlist(f1.extrusion, f1.color)
        f1.props()
        return f1

    @classmethod
    def by_point_height_rotation(cls, start: Point, height: float, polycurve: PolyCurve2D, frame_name: str, rotation: float, material = None):
        # 2D polycurve
        f1 = Frame()
        f1.start = start
        f1.end = Point.translate(start,Vector3(0,0.00001,height))
        # self.curve = Line(start, end)
        f1.directionVector = Vector3.byTwoPoints(start, f1.end)
        f1.length = Vector3.length(f1.directionVector)
        f1.name = frame_name
        f1.profileName = frame_name
        curvrot = polycurve.rotate(rotation)  # rotation in degrees
        f1.extrusion = Extrusion.byPolyCurveHeightVector(curvrot, f1.length, CSGlobal, start, f1.directionVector)
        f1.extrusion.name = frame_name
        f1.curve3d = curvrot
        f1.material = material
        f1.color = material.colorint
        f1.colorlst = colorlist(f1.extrusion, f1.color)
        f1.props()
        return f1

    @classmethod
    def by_point_profile_height_rotation(cls, start: Point, height: float, profile_name: str, rotation: float, material = None):
        f1 = Frame()
        f1.start = start
        f1.end = Point.translate(start,Vector3(0,0.00001,height)) #TODO vertical column not possible
        # self.curve = Line(start, end)
        f1.directionVector = Vector3.byTwoPoints(start, f1.end)
        f1.length = Vector3.length(f1.directionVector)
        f1.name = profile_name
        f1.profileName = profile_name
        curv = profiledataToShape(profile_name).polycurve2d
        curvrot = curv.rotate(rotation)  # rotation in degrees
        f1.extrusion = Extrusion.byPolyCurveHeightVector(curvrot.curves, f1.length, CSGlobal, start, f1.directionVector)
        f1.extrusion.name = profile_name
        f1.curve3d = curvrot
        f1.profileName = profile_name
        f1.material = material
        f1.color = material.colorint
        f1.colorlst = colorlist(f1.extrusion, f1.color)
        f1.props()
        return f1


    @classmethod
    def byStartpointEndpointCurveJustifiction(cls, start: Point, end: Point, polycurve: PolyCurve2D, name: str, XJustifiction: str, YJustifiction: str, rotation: float, material = None):
        f1 = Frame()
        f1.start = start
        f1.end = end
        # self.curve = Line(start, end)
        f1.rotation = rotation
        curv = polycurve
        curvrot = curv.rotate(rotation)  # rotation in degrees
        v1 = justifictionToVector(curvrot, XJustifiction, YJustifiction) #center, left, right, origin / center, top bottom, origin
        f1.XOffset = v1.x
        f1.YOffset = v1.y
        f1.curve = curv.translate(v1)
        f1.directionVector = Vector3.byTwoPoints(start, end)
        f1.length = Vector3.length(f1.directionVector)
        f1.name = name
        f1.extrusion = Extrusion.byPolyCurveHeightVector(f1.curve.curves, f1.length, CSGlobal, start, f1.directionVector)
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