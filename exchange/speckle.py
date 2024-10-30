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


"""This module provides tools for exporting geometry to Speckle
"""

__title__ = "speckle"
__author__ = "Maarten & Jonathan"
__url__ = "./exchange/speckle.py"

import sys
from pathlib import Path

from geometry.mesh import Mesh

sys.path.append(str(Path(__file__).resolve().parents[1]))

from BuildingPy import BuildingPy, Coords, Panel, Point
from BuildingPy import Line
from BuildingPy import PolyCurve, Polygon
from BuildingPy import Arc
from BuildingPy import Vector
from BuildingPy import Plane
from BuildingPy import Interval
from BuildingPy import Vector, Point, Line, PolyCurve
from BuildingPy import project
from packages.helper import flatten

# [!not included in BP singlefile - end]


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
from specklepy.objects.other import DisplayStyle as SpeckleDisplayStyle
from specklepy.objects.geometry import Extrusion as SpeckleExtrusion
from specklepy.objects.primitive import Interval as SpeckleInterval
from specklepy.objects.geometry import Spiral as SpeckleSpiral
from specklepy.objects.geometry import SpiralType as SpeckleSpiralType

def toSpeckle(self: BuildingPy, streamid, commitstring=None):
    try:
        import specklepy
    except ImportError:
        print("Installing requirement: specklepy")
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "specklepy"])
        import specklepy
    from exchange.speckle import translateObjectsToSpeckleObjects, TransportToSpeckle
    self.specklestream = streamid
    speckleobj = translateObjectsToSpeckleObjects(self.objects)
    TransportToSpeckle(self.speckleserver, streamid, speckleobj, commitstring)

def CreateStream(serverurl, name, description):
    #Create new stream/project in Speckle Server
    client = SpeckleClient(host=serverurl)
    account = get_default_account()
    client.authenticate_with_account(account)
    streamid = client.stream.create(name,description,True)
    return streamid

def IntervalToSpeckleInterval(interval: Interval):
    SpeckleInt = SpeckleInterval(start=interval.start, end=interval.end)
    SpeckleInt.units = project.units
    return SpeckleInt


def PointToSpecklePoint(point: Coords):
    SpecklePnt = SpecklePoint.from_coords(point.x, point.y, point.z)
    SpecklePnt.id = point.id
    SpecklePnt.units = project.units
    SpecklePnt.applicationId = project.applicationId
    return SpecklePnt


def VectorToSpeckleVector(Vector: Vector):
    SpeckleVctr = SpeckleVector.from_coords(Vector.x, Vector.y, Vector.z)
    SpeckleVctr.units = project.units
    return SpeckleVctr


def LineToSpeckleLine(line: Line):
    display_style = SpeckleDisplayStyle()
    display_style.name = "Custom Style"
    display_style.color = -854423
    display_style.linetype = "Continuous"
    display_style.lineweight = 0.25

    SpeckleLn = SpeckleLine(start = PointToSpecklePoint(line.start), end = PointToSpecklePoint(line.end))
    SpeckleLn.id = line.id
    SpeckleLn.units = project.units
    SpeckleLn.domain = project.domain
    SpeckleLn.length = line.length
    SpeckleLn.applicationId = project.applicationId
    SpeckleLn.color = 0
    SpeckleLn.displayStyle = display_style
    return SpeckleLn


def PlaneToSpecklePlane(plane: Plane):
    SpecklePln = SpecklePlane(origin = PointToSpecklePoint(plane.Origin), normal = VectorToSpeckleVector(plane.Normal), xdir = VectorToSpeckleVector(plane.v1), ydir = VectorToSpeckleVector(plane.v2))
    SpecklePln.units = project.units
    return SpecklePln


def SpecklePolylineBySpecklePoints(polycurve: PolyCurve):
    SpecklePl = [PointToSpecklePoint(point) for point in polycurve.points]
    SpecklePolyln = SpecklePolyLine.from_points(SpecklePl)
    SpecklePolyln.id = polycurve.id
    SpecklePolyln.name = polycurve.type
    SpecklePolyln.units = project.units
    SpecklePolyln.domain = project.domain
    SpecklePolyln.applicationId = project.applicationId
    try:
        SpecklePolyln.area = polycurve.area()
        SpecklePolyln.length = PolyCurve.length(polycurve)
        SpecklePolyln.closed = polycurve.closed
    except Exception as e:
        print(e)

    return SpecklePolyln

def SpecklePolygonBySpecklePoints(polycurve): #fixed
    SpecklePoints = [PointToSpecklePoint(point) for point in polycurve.points]
    SpecklePolygon = SpecklePolyLine.from_points(points=SpecklePoints)
    SpecklePolygon.id = polycurve.id
    SpecklePolygon.name = polycurve.type
    SpecklePolygon.units = project.units
    SpecklePolygon.domain = project.domain
    SpecklePolygon.applicationId = project.applicationId
    SpecklePolygon.closed = polycurve.isClosed
    SpecklePolygon.area = polycurve.area()
    SpecklePolygon.length = polycurve.length()
    SpecklePolygon.curveCount = len(polycurve.curves)
    SpecklePolygon.pointCount = len(polycurve.points)

    return SpecklePolygon

def SpecklePolyline2DBySpecklePoints2D(polycurve: PolyCurve):
    SpecklePl = [PointToSpecklePoint(point) for point in polycurve.points2D]
    SpecklePolyln = SpecklePolyLine.from_points(SpecklePl)
    SpecklePolyln.id = polycurve.id
    SpecklePolyln.units = project.units
    SpecklePolyln.domain = project.domain
    SpecklePolyln.applicationId = project.applicationId
    try:
        SpecklePolyln.area = polycurve.area()
        SpecklePolyln.length = PolyCurve.length(polycurve)
        SpecklePolyln.closed = polycurve.isClosed
    except Exception as e:
        print(e)

    return SpecklePolyln


def Line2DToSpeckleLine3D(line: Line):
    SpeckleLn = SpeckleLine(applicationId = project.applicationId, start = PointToSpecklePoint(Point(line.start.x,line.start.y,0)), end = PointToSpecklePoint(Point(line.end.x,line.end.y,0)))
    SpeckleLn.id = line.id
    SpeckleLn.units = project.units
    SpeckleLn.domain = project.domain
    SpeckleLn.length = line.length
    SpeckleLn.applicationId = project.applicationId
    return SpeckleLn


def PolyCurveToSpecklePolyLine(polycurve: PolyCurve):
    tmpList = []
    if not isinstance(polycurve, list):
        polycurve = [polycurve]
    for item in polycurve:
        spklpc = SpecklePolylineBySpecklePoints(item)
        tmpList.append(spklpc)
    return tmpList


def GridToLines(Grid):
    SpeckleLines = []
    for i in Grid.line:
        SpeckleLines.append(SpeckleLine(applicationId = project.applicationId, start = PointToSpecklePoint(i.start), end = PointToSpecklePoint(i.end), units = project.units))
    return SpeckleLines


def GridSystemToLines(GridSystem):
    SpeckleLines = []
    for j in GridSystem.gridsX:
        SpeckleLines.append(GridToLines(j))
    for k in GridSystem.gridsY:
        SpeckleLines.append(GridToLines(k))
    return SpeckleLines


def Point2DToSpecklePoint(Point: Point):
    SpecklePnt = SpecklePoint.from_coords(Point.x, Point.y, 0)
    SpecklePnt.units = project.units
    return SpecklePnt


def SpeckleMeshByMesh(mesh:Mesh):
    color = -1762845660

    SpeckleMsh = SpeckleMesh(applicationId = project.applicationId, 
                             vertices = mesh.vertices, 
                             faces = [[len(face)].extend(face) for face in mesh.faces],
                             name = mesh.name,
                             colors = [color] * len(mesh.faces), 
                             units = project.units,
                             textureCoordinates = []
                             )
    return SpeckleMsh


def TextToSpeckleCurveSurface(Text):
    returnlist = []
    for polycurves in Text.write():
        polycurve = PolyCurveToSpecklePolyLine(polycurves)
        returnlist.append(polycurve)
    return returnlist


def SpeckleMeshByImage(img):
    SpeckleMsh = SpeckleMesh(applicationId = project.applicationId, 
                             vertices = img.vert, 
                             faces = img.faces, 
                             name = img.name, 
                             colors = img.colorlst,
                             units = project.units,
                             textureCoordinates = []
                             )
    return SpeckleMsh


def ArcToSpeckleArc(arc: Arc):
    speckle_plane = SpecklePlane(
        origin = PointToSpecklePoint(arc.plane.Origin),
        normal = VectorToSpeckleVector(arc.plane.Normal),
        xdir = VectorToSpeckleVector(arc.plane.vector_1),
        ydir = VectorToSpeckleVector(arc.plane.vector_2),
        
        units = project.units
    )

    start_point = PointToSpecklePoint(arc.start)
    mid_point = PointToSpecklePoint(arc.mid)
    end_point = PointToSpecklePoint(arc.end)

    radius = arc.radius
    start_angle = arc.startAngle
    end_angle = arc.endAngle
    angle_radians = arc.angle_radian
    area = arc.area
    length = arc.length
    speckle_interval = IntervalToSpeckleInterval(Interval(start=0, end=1))


    spArc = SpeckleArc(
        applicationId = project.applicationId,
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
        units=project.units
    )

    spArc.units = project.units
    return spArc


def Arc2DToSpeckleArc(arc: Arc):
    speckle_plane = SpecklePlane(
        origin = PointToSpecklePoint(arc.plane.Origin),
        normal = VectorToSpeckleVector(arc.plane.Normal),
        xdir = VectorToSpeckleVector(arc.plane.vector_1),
        ydir = VectorToSpeckleVector(arc.plane.vector_2),
        
        units = project.units
    )

    start_point = PointToSpecklePoint(arc.start)
    mid_point = PointToSpecklePoint(arc.mid)
    end_point = PointToSpecklePoint(arc.end)

    radius = arc.radius
    start_angle = arc.startAngle
    end_angle = arc.endAngle
    angle_radians = arc.angle_radian
    area = arc.area
    length = arc.length
    speckle_interval = IntervalToSpeckleInterval(Interval(start=0, end=1))


    spArc = SpeckleArc(
        applicationId = project.applicationId,
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
        units=project.units
    )

    spArc.units = project.units
    return spArc


def TransportToSpeckle(host: str, streamid: str, SpeckleObjects: list, messageCommit: str):
    client = SpeckleClient(host=host)
    account = get_default_account()
    client.authenticate_with_account(account)
    streamid = streamid

    class SpeckleExport(Base):
        elements = None

    obj = SpeckleExport(elements = SpeckleObjects)
    transport = ServerTransport(client=client, stream_id=streamid)
    hash = operations.send(base=obj, transports=[transport])

    commit_id = client.commit.create(
        stream_id = streamid,
        object_id = hash,
        message = messageCommit,
    )

    print(f"View commit: https://{host}/streams/{streamid}/commits/{commit_id}")
    return commit_id


def translateObjectsToSpeckleObjects(Obj):
    SpeckleObj = []
    for current_object in flatten(Obj):
        nm = current_object.__class__.__name__
        if nm == "list":
            if current_object == []:
                print(f"'{nm}' Object not yet added to translateObjectsToSpeckleObjects")

        elif isinstance(current_object, Panel):
            colrs = current_object.colorlst
            SpeckleObj.append(SpeckleMesh(applicationId = project.applicationId,
                                          vertices=current_object.extrusion.verts, 
                                          faces=current_object.extrusion.faces, 
                                          colors = colrs, 
                                          name = current_object.name, 
                                          units = project.units,
                                          textureCoordinates = []
                                          ))
            
        elif nm == 'Face':
            all_vertices = []
            all_faces = []
            all_colors = []
            for index in range(len(current_object.PolyCurveList)):
                all_vertices.append(current_object.mesh[index].verts)
                all_faces.append(current_object.mesh[index].faces)
                all_colors.append(current_object.colorlst[index])
            all_vertices = flatten(all_vertices)
            all_faces = flatten(all_faces)
            all_colors = flatten(all_colors)
            SpeckleObj.append(SpeckleMesh(applicationId = project.applicationId,
                                          vertices=all_vertices,
                                          faces=all_faces, 
                                          colors=all_colors, 
                                          name=current_object.name[index], 
                                          units= project.units
                                          ))

        elif nm == 'Surface':
            all_vertices = []
            all_faces = []
            all_colors = []
            
            if len(current_object.inner_Surface) > 0:
                for each in current_object.inner_Surface:
                    SpeckleObj.append(SpeckleMesh(applicationId = project.applicationId,
                                                  surface_type = "Inner_Surface",
                                                  vertices=each.verts,
                                                  faces=each.faces, 
                                                  name=current_object.type,
                                                  units= project.units,
                                                  textureCoordinates = []
                                                  ))

            SpeckleObj.append(SpeckleMesh(applicationId = project.applicationId,
                                          surface_type = "Outer_Surface",
                                          vertices=current_object.outer_Surface.verts,
                                          faces=current_object.outer_Surface.faces, 
                                          name=current_object.type,
                                          units= project.units,
                                          textureCoordinates = [],
                                          colors = current_object.colorlst
                                          ))
            


        elif nm == 'Frame':
            try:
                if current_object.comments.type == "Scia_Params":
                    SpeckleObj.append(SpeckleMesh(applicationId = project.applicationId, 
                                                  vertices=current_object.extrusion.verts, 
                                                  faces=current_object.extrusion.faces, 
                                                  colors = current_object.colorlst, 
                                                  name = current_object.profileName, 
                                                  units = project.units,
                                                  textureCoordinates = [],
                                                  Scia_Id=current_object.comments.id, 
                                                  Scia_Justification=current_object.comments.perpendicular_alignment, 
                                                  Scia_Layer=current_object.comments.layer, 
                                                  Scia_Rotation=current_object.comments.lcs_rotation, 
                                                  Scia_Staaf=current_object.comments.name, 
                                                  Scia_Type=current_object.comments.cross_section, 
                                                  Scia_Node_Start = current_object.comments.start_node, 
                                                  Scia_Node_End = current_object.comments.end_node, 
                                                  Revit_Rotation=str(current_object.comments.revit_rot), 
                                                  Scia_Layer_Type=current_object.comments.layer_type, 
                                                  BuildingPy_XJustification=current_object.comments.Xjustification, 
                                                  BuildingPy_YJustification=current_object.comments.Yjustification))
                    
                else:
                    SpeckleObj.append(SpeckleMesh(applicationId = project.applicationId, 
                                                  vertices=current_object.extrusion.verts, 
                                                  faces=current_object.extrusion.faces, 
                                                  colors = current_object.colorlst, 
                                                  name = current_object.profileName, 
                                                  units = project.units,
                                                  textureCoordinates = []
                                                  ))
                    
            except:
                SpeckleObj.append(SpeckleMesh(applicationId = project.applicationId, 
                                                vertices=current_object.extrusion.verts, 
                                                faces=current_object.extrusion.faces, 
                                                colors = current_object.colorlst, 
                                                name = current_object.profileName, 
                                                units = project.units,
                                                textureCoordinates = []
                                                ))
                
        elif nm == "Extrusion" or nm == "Void":
            clrs = [4294901760, 4294901760, 4294901760, 4294901760, 4294901760]

            # if void, color red.
            
            mesh = SpeckleMesh(applicationId=project.applicationId,
                               vertices=current_object.verts,
                               faces=current_object.faces,
                               colors=clrs,
                               name=nm if nm == "Void" else current_object.name,
                               units=project.units,
                               textureCoordinates = []
                               )
            
            if isinstance(current_object.parameters, dict):
                current_object.parameters = [current_object.parameters]
                
            for param in current_object.parameters:
                for param, value in param.items():
                    try:
                        param_name = int(param)
                    except ValueError:
                        param_name = param
                    setattr(mesh, str(param_name), value)
            SpeckleObj.append(mesh)

            # points = [
            #     SpecklePoint(x=0, y=0, z=0),
            #     SpecklePoint(x=0, y=10, z=0),
            #     SpecklePoint(x=10, y=10, z=0),
            #     SpecklePoint(x=10, y=0, z=0),
            #     SpecklePoint(x=0, y=0, z=0)
            # ]

            # profiel = SpecklePolyLine.from_points(points)
            # extrusix = SpeckleExtrusion(
            #     area = 0,
            #     bbox = None,
            #     units = "mm",
            #     volume = 9,
            #     capped = True,
            #     profile = profiel,
            #     pathStart = SpecklePoint(x=0, y=0, z=0),
            #     pathEnd = SpecklePoint(x=0, y=10, z=120),
            #     pathCurve = SpeckleLine(start = SpecklePoint(x=0, y=0, z=0), end = SpecklePoint(x=0, y=10, z=120)),
            #     pathTangent = SpeckleVector.from_coords(1, 0, 0),
            #     length = 120,
            #     applicationId = "Test"
            # )
            
            # hoofd_profiel = SpecklePolyLine.from_points([
            #     SpecklePoint(x = 0, y = 0, z = 0),
            #     SpecklePoint(x = 0,  y = 10, z = 0),
            #     SpecklePoint(x = 10, y = 10, z = 0),
            #     SpecklePoint(x = 10, y = 0, z = 0),
            #     SpecklePoint(x = 0, y = 0, z = 0)
            # ])

            # gat_profiel = SpecklePolyLine.from_points([
            #     SpecklePoint(x = 3, y = 3, z = 0),
            #     SpecklePoint(x = 3, y = 7, z = 0),
            #     SpecklePoint(x = 7, y = 7, z = 0),
            #     SpecklePoint(x = 7, y = 3, z = 0),
            #     SpecklePoint(x = 3, y = 3, z = 0)
            # ])

            # extrusix.profiles = [hoofd_profiel, gat_profiel]
            # SpeckleObj.append(extrusix)


        elif nm == "Wall":
            clrs = []
            SpeckleObj.append(SpeckleMesh(applicationId = project.applicationId,
                                          vertices=current_object.verts, 
                                          faces=current_object.faces, 
                                          colors = clrs,
                                          name = current_object.name, 
                                          units = project.units,
                                          textureCoordinates = []
                                          ))
            
        elif nm == 'PolyCurve':
            SpeckleObj.append(SpecklePolylineBySpecklePoints(current_object))

        elif nm == 'Polygon':
            try:
                SpeckleObj.append(SpecklePolygonBySpecklePoints(current_object))
            except:
                print("Polygon could not be exported")

        elif nm == 'PolyCurve':
            SpeckleObj.append(SpecklePolyline2DBySpecklePoints2D(current_object))

        elif nm == 'Rect':
            SpeckleObj.append(SpecklePolylineBySpecklePoints(current_object))

        elif nm == 'ImagePyB':
            colrs = current_object.colorlst
            SpeckleObj.append(SpeckleMesh(applicationId = project.applicationId,
                                          vertices=current_object.verts, 
                                          faces=current_object.faces, 
                                          colors = colrs, 
                                          name = current_object.name, 
                                          units = project.units,
                                          textureCoordinates = []
                                          ))
            
        elif nm == 'Interval':
            SpeckleObj.append(IntervalToSpeckleInterval(current_object))

        elif nm == 'Line':
            SpeckleObj.append(LineToSpeckleLine(current_object))

        elif nm == 'Plane':
            SpeckleObj.append(PlaneToSpecklePlane(current_object))

        elif nm == 'Arc':
            SpeckleObj.append(ArcToSpeckleArc(current_object))

        elif nm == 'Arc2D':
            SpeckleObj.append(Arc2DToSpeckleArc(current_object))

        elif nm == 'Line2D':
            SpeckleObj.append(Line2DToSpeckleLine3D(current_object))

        elif isinstance(current_object, Coords):
            SpeckleObj.append(PointToSpecklePoint(current_object))

        elif nm == 'Node':
            SpeckleObj.append(PointToSpecklePoint(current_object.point))
            
        elif nm == 'Text':
            SpeckleObj.append(TextToSpeckleCurveSurface(current_object))

        elif nm == 'Point':
            SpeckleObj.append(Point2DToSpecklePoint(current_object))

        elif nm == 'Grid':
            for j in GridToLines(current_object):
                SpeckleObj.append(j)

        elif nm == 'GridSystem':
            for j in GridSystemToLines(current_object):
                SpeckleObj.append(j)

        elif nm == 'imagePyB':
            SpeckleObj.append(SpeckleMeshByImage(current_object))

        elif isinstance(current_object, Mesh):
            SpeckleObj.append(SpeckleMeshByMesh(current_object))

        elif nm == 'Trimesh':
            clrs = []
            SpeckleObj.append(SpeckleMesh(applicationId = project.applicationId,
                                          vertices=current_object.vertices, 
                                          faces=current_object.faces, 
                                          colors = clrs, 
                                          name = current_object.name, 
                                          units = project.units,
                                          textureCoordinates = []
                                          ))
        else:
            print(f"'{nm}' Object not yet added to translateObjectsToSpeckleObjects")

    return SpeckleObj
