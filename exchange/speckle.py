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

__title__ = "speckle"
__author__ = "Maarten & Jonathan"
__url__ = "./exchange/speckle.py"

import sys, os, math
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from geometry.point import Point
from geometry.curve import Line
from geometry.curve import PolyCurve
from geometry.curve import Arc
from geometry.geometry2d import Point2D
from abstract.vector import Vector3
from abstract.plane import Plane
from abstract.interval import Interval
from packages.helper import *

from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_default_account
from specklepy.transports.server import ServerTransport
from specklepy.api import operations

from specklepy.objects import Base
from specklepy.objects.geometry import Point as SpecklePoint
from specklepy.objects.geometry import Line as SpeckleLine
from specklepy.objects.geometry import Mesh as SpeckleMesh
from specklepy.objects.geometry import Polyline as SpecklePolyLine
from specklepy.objects.geometry import Vector as SpeckleVector
from specklepy.objects.geometry import Plane as SpecklePlane
from specklepy.objects.geometry import Arc as SpeckleArc
from specklepy.objects.primitive import Interval as SpeckleInterval
from project.fileformat import project


def IntervalToSpeckleInterval(Interval: Interval):
    SpeckleInt = SpeckleInterval(start=Interval.start, end=Interval.end)
    return SpeckleInt

def PointToSpecklePoint(Point: Point):
    try:
        SpecklePnt = SpecklePoint.from_coords(Point.x, Point.y, Point.z)
    except:
        SpecklePnt = SpecklePoint.from_coords(Point.x, Point.y, 0)
    
    SpecklePnt.units = project.units
    return SpecklePnt


def VectorToSpeckleVector(Vector3: Vector3):
    SpeckleVctr = SpeckleVector.from_coords(Vector3.x, Vector3.y, Vector3.z)
    return SpeckleVctr


def LineToSpeckleLine(Line: Line):
    SpeckleLn = SpeckleLine(start = PointToSpecklePoint(Line.start), end = PointToSpecklePoint(Line.end), units = "mm")
    return SpeckleLn


def PlaneToSpecklePlane(Plane: Plane):
    SpecklePln = SpecklePlane(origin = PointToSpecklePoint(Plane.Origin), normal = VectorToSpeckleVector(Plane.Normal), xdir = VectorToSpeckleVector(Plane.v1), ydir = VectorToSpeckleVector(Plane.v2))
    return SpecklePln


def SpecklePolylineBySpecklePoints(SpecklePoints: list[Point]):
    SpecklePl = [PointToSpecklePoint(point) for point in SpecklePoints]
    SpecklePolyline = SpecklePolyLine.from_points(SpecklePl)
    SpecklePolyline.units = project.units
    return SpecklePolyline


def Line2DToSpeckleLine3D(ln):
    SpeckleLn = SpeckleLine(start = PointToSpecklePoint(Point(ln.start.x,ln.start.y,0)), end = PointToSpecklePoint(Point(ln.end.x,ln.end.y,0)), units = "mm")
    return SpeckleLn


def PolyCurveToSpecklePolyLine(polycurve: PolyCurve):
    tmpList = []
    for item in polycurve:
        nList = []
        for n in item.points:
            p = PointToSpecklePoint(n)
            nList.append(p)
        spklpc = SpecklePolylineBySpecklePoints(nList)
        tmpList.append(spklpc)
       
    return tmpList


def GridToLines(Grid):
    SpeckleLines = []
    for i in Grid.line:
        SpeckleLines.append(SpeckleLine(start = PointToSpecklePoint(i.start), end = PointToSpecklePoint(i.end), units = "mm")) #, units = "mm"
    return SpeckleLines


def Point2DToSpecklePoint(Point2D: Point2D):
    SpecklePnt = SpecklePoint.from_coords(Point2D.x, Point2D.y, 0)
    return SpecklePnt


def SpeckleMeshByMesh(MeshPB):
    color = -1762845660
    colrs = []
    for i in range(MeshPB.countVertsFaces):
        colrs.append(color)
    #colors = colrs
    spcklmesh = SpeckleMesh(vertices = MeshPB.verts, faces = MeshPB.faces, name = MeshPB.name, colors = colrs, units = "mm")
    return spcklmesh


def TextToSpeckleCurveSurface(Text):
    returnlist = []
    for polyc in Text.write():
        pc = PolyCurveToSpecklePolyLine(polyc)
        returnlist.append(pc)
    return returnlist

def SpeckleMeshByImage(img):
    spcklmesh = SpeckleMesh(vertices = img.vert, faces = img.faces, name = img.name, colors = img.colorlst)
    return spcklmesh

def ArcToSpeckleArc(Arc: Arc):
    speckle_plane = SpecklePlane(
        origin = PointToSpecklePoint(Arc.plane.Origin),
        normal = VectorToSpeckleVector(Arc.plane.Normal),
        xdir = VectorToSpeckleVector(Arc.plane.v1),
        ydir = VectorToSpeckleVector(Arc.plane.v2)
    )
    start_point = PointToSpecklePoint(Arc.start)
    mid_point = PointToSpecklePoint(Arc.mid)
    end_point = PointToSpecklePoint(Arc.end)
    radius = Arc.radius
    start_angle = Arc.startAngle
    end_angle = Arc.endAngle
    angle_radians = Arc.angleRadian
    area = Arc.area
    length = Arc.length
    units = Arc.units
    speckle_interval = IntervalToSpeckleInterval(Interval(start=0, end=1))
    return SpeckleArc(
        startPoint=start_point,
        midPoint=mid_point,
        endPoint=end_point,
        domain=speckle_interval,
        plane=speckle_plane,
        radius=radius,
        startAngle=start_angle,
        endAngle=end_angle,
        angleRadians=angle_radians,
        area=area,
        length=length,
        units=units
    )


def TransportToSpeckle(host: str, streamid: str, SpeckleObjects: list, messageCommit: str):
    # initialise the client
    client = SpeckleClient(host=host)  # or whatever your host is
    # client = SpeckleClient(host="localhost:3000", use_ssl=False) or use local server

    # authenticate the client with a token
    account = get_default_account()
    client.authenticate_with_account(account)

    # new_stream = client.stream.get(id=)
    streamid = streamid

    class SpeckleExport(Base):
        # Hoofdclass waar alle objecten uit het model in gezet worden.
        objects = None

    obj = SpeckleExport(objects=SpeckleObjects)

    # next create a server transport - this is the vehicle through which you will send and receive
    transport = ServerTransport(client=client, stream_id=streamid)

    # this serialises the block and sends it to the transport
    hash = operations.send(base=obj, transports=[transport])

    # you can now create a commit on your stream with this object
    commit_id = client.commit.create(
        stream_id = streamid,
        object_id = hash,
        message = messageCommit,
    )
    
    print(f"View commit: https://{host}/streams/{streamid}/commits/{commit_id}")
    return commit_id

def translateObjectsToSpeckleObjects(Obj):
    SpeckleObj = []
    for i in Obj:
        nm = i.__class__.__name__
        # print(nm)
        if nm == 'Panel':
            colrs = i.colorlst
            SpeckleObj.append(SpeckleMesh(vertices=i.extrusion.verts, faces=i.extrusion.faces, colors = colrs, name = i.name, units = "mm"))
        
        all_vertices = []
        all_faces = []
        all_colors = []
        if nm == 'Surface' or nm == 'Face':
            for index in range(len(i.PolyCurveList)):
                all_vertices.append(i.mesh[index].verts)
                all_faces.append(i.mesh[index].faces)
                all_colors.append(i.colorlst[index])
            all_vertices = flatten(all_vertices)
            all_faces = flatten(all_faces)
            all_colors = flatten(all_colors)
            SpeckleObj.append(SpeckleMesh(vertices=all_vertices, faces=all_faces, colors=all_colors, name=i.name[index], units="mm"))
            # print(all_vertices, all_faces, all_colors)

        # if nm == 'Surface' or nm == 'Face':
        #     for index in range(len(i.PolyCurveList)):
        #         colrs = i.colorlst[index]
        #         SpeckleObj.append(SpeckleMesh(vertices=i.extrusion[index].verts, faces=i.extrusion[index].faces, colors = colrs, name = i.name[index], units = "mm"))

        elif nm == 'Frame':
            colrs = i.colorlst
            SpeckleObj.append(SpeckleMesh(vertices=i.extrusion.verts, faces=i.extrusion.faces, colors = colrs, name = i.profileName, units = "mm"))
        elif nm == 'PolyCurve':
            pnts = []
            for point in i.points:
                pnts.append(point)
            SpeckleObj.append(SpecklePolylineBySpecklePoints(pnts))
        elif nm == 'ImagePyB':
            colrs = i.colorlst
            SpeckleObj.append(SpeckleMesh(vertices=i.verts, faces=i.faces, colors = colrs, name = i.name, units = "mm"))
        elif nm == 'Interval':
            SpeckleObj.append(IntervalToSpeckleInterval(i))
        elif nm == 'Line':
            SpeckleObj.append(LineToSpeckleLine(i))
        elif nm == 'Plane':
            SpeckleObj.append(PlaneToSpecklePlane(i))
        elif nm == 'Arc':
            SpeckleObj.append(ArcToSpeckleArc(i))
        elif nm == 'Line2D':
            SpeckleObj.append(Line2DToSpeckleLine3D(i))
        elif nm == 'Point':
            SpeckleObj.append(PointToSpecklePoint(i))
        elif nm == 'Text':
            SpeckleObj.append(TextToSpeckleCurveSurface(i))
        elif nm == 'Point2D':
            SpeckleObj.append(Point2DToSpecklePoint(i))
        elif nm == 'Grid':
            for j in GridToLines(i):
                SpeckleObj.append(j)
        elif nm == 'imagePyB':
            SpeckleObj.append(SpeckleMeshByImage(i))
    return SpeckleObj
