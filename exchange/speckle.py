# -*- coding: utf8 -*-
# ***************************************************************************
# *   Copyright (c) 2023 Jonathan Van der Gouwe & Maarten Vroegindeweij     *
# *   jonathan@3bm.co.nl & maarten@3bm.co.nl                                *
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

from geometry.point import Point
from geometry.curve import Line
from geometry.flat import Point2D

from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_default_account
from specklepy.objects import Base
from specklepy.objects.geometry import Point as SpecklePoint
from specklepy.objects.geometry import Line as SpeckleLine
from specklepy.objects.geometry import Mesh as SpeckleMesh
from specklepy.objects.geometry import Polyline
# from specklepy.objects.geometry import Surface
from specklepy.transports.server import ServerTransport
from specklepy.api import operations

def PolylineByPoints(SpecklePoints):
    Polyline.from_points(SpecklePoints)
    return Polyline


def PointToSpecklePoint(Point: Point):
    SpecklePnt = SpecklePoint.from_coords(Point.x, Point.y, Point.z)
    return SpecklePnt


def LineToSpeckleLine(Line: Line):
    SpeckleLn = SpeckleLine(start = PointToSpecklePoint(Line.start), end = PointToSpecklePoint(Line.end), units = "mm")
    return SpeckleLn


def Point2DToSpecklePoint(Point2D: Point2D):
    SpecklePnt = SpecklePoint.from_coords(Point2D.x, Point2D.y, 0)
    return SpecklePnt


def SpeckleMeshByMesh(MeshPB):
    color = -1762845660
    colrs = []
    for i in range(MeshPB.numberFaces*4):
        colrs.append(color)
    #colors = colrs
    spcklmesh = SpeckleMesh(vertices = MeshPB.verts, faces = MeshPB.faces, name = MeshPB.name, units = "mm")
    return spcklmesh


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
    commid_id = client.commit.create(
        stream_id = streamid,
        object_id = hash,
        message = messageCommit,
    )

    return (commid_id)
