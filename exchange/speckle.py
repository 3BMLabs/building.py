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

from geometry.point import *
from geometry.curve import Line
from geometry.curve import PolyCurve
from geometry.curve import Arc
from geometry.geometry2d import Point2D
from abstract.vector import Vector3

#from packages.specklepy.api.client import SpeckleClient
#from packages.specklepy.api.credentials import get_default_account
#from packages.specklepy.transports.server import ServerTransport
#from packages.specklepy.api import operations

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
#from specklepy.objects.primitive import Interval as SpeckleInterval


def SpecklePolylineBySpecklePoints(SpecklePoints):
    SpecklePolyLine.from_points(SpecklePoints)
    return SpecklePolyLine

def PointToSpecklePoint(Point: Point):
    SpecklePnt = SpecklePoint.from_coords(Point.x, Point.y, Point.z)
    return SpecklePnt

def VectorToSpeckleVector(Vector3: Vector3):
    Vectr = SpeckleVector.from_coords(Vector3.x, Vector3.y, Vector3.z)
    return Vectr

def LineToSpeckleLine(Line: Line):
    SpeckleLn = SpeckleLine(start = PointToSpecklePoint(Line.start), end = PointToSpecklePoint(Line.end), units = "mm")
    return SpeckleLn

def Line2DToSpeckleLine3D(ln):
    SpeckleLn = SpeckleLine(start = PointToSpecklePoint(Point(ln.start.x,ln.start.y,0)), end = PointToSpecklePoint(Point(ln.end.x,ln.end.y,0)), units = "mm")
    return SpeckleLn

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

def ArcToSpeckleArc(Arc: Arc):
    return SpeckleArc(
        startPoint=PointToSpecklePoint,
        midPoint=PointToSpecklePoint,
        endPoint=PointToSpecklePoint,
        domain=SpeckleInterval(start=0, end=1),
        plane=SpecklePlane(origin=PointToSpecklePoint, normal=VectorToSpeckleVector, xdir=VectorToSpeckleVector, ydir=VectorToSpeckleVector),
        radius= Arc.radius,
        startAngle= Arc.radius,
        endAngle= Arc.radius,
        angleRadians= Arc.radius,
        area= Arc.radius,
        length= Arc.radius,
        units= Arc.radius
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
    print(f"Commit ID: {commit_id}")
    return commit_id

def translateObjectsToSpeckleObjects(Obj):
    SpeckleObj = []
    for i in Obj:
        nm = i.__class__.__name__
        if nm == 'Panel':
            colrs = i.colorlst
            SpeckleObj.append(SpeckleMesh(vertices=i.extrusion.verts, faces=i.extrusion.faces, colors = colrs, name = i.name, units = "mm"))
        elif nm == 'Frame':
            colrs = i.colorlst
            SpeckleObj.append(SpeckleMesh(vertices=i.extrusion.verts, faces=i.extrusion.faces, colors = colrs, name = i.profileName, units = "mm"))
        elif nm == 'PolyCurve':
            pnts = []
            for j in i.points:
                pnts.append(PointToSpecklePoint(j))
            SpeckleObj.append(SpecklePolylineBySpecklePoints(pnts))
        elif nm == 'Line':
            SpeckleObj.append(LineToSpeckleLine(i))
        elif nm == 'Line2D':
            SpeckleObj.append(Line2DToSpeckleLine3D(i))
        elif nm == 'Point':
            SpeckleObj.append(PointToSpecklePoint(i))
        elif nm == 'Point2D':
            SpeckleObj.append(Point2DToSpecklePoint(i))
        elif nm == 'Grid':
            for j in GridToLines(i):
                SpeckleObj.append(j)

    return SpeckleObj
