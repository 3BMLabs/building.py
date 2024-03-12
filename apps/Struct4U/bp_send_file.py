from bp_single_file import *

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


def IntervalToSpeckleInterval(interval: Interval):
    SpeckleInt = SpeckleInterval(start=interval.start, end=interval.end)
    SpeckleInt.units = project.units
    return SpeckleInt


def PointToSpecklePoint(point: Point or Point2D):
    if point.type == "Point":
        SpecklePnt = SpecklePoint.from_coords(point.x, point.y, point.z)
    elif point.type == "Point2D":
        SpecklePnt = SpecklePoint.from_coords(point.x, point.y, 0)
    SpecklePnt.id = point.id
    SpecklePnt.units = project.units
    SpecklePnt.applicationId = project.applicationId
    return SpecklePnt


def VectorToSpeckleVector(vector3: Vector3):
    SpeckleVctr = SpeckleVector.from_coords(vector3.x, vector3.y, vector3.z)
    SpeckleVctr.units = project.units
    return SpeckleVctr


def LineToSpeckleLine(line: Line):
    SpeckleLn = SpeckleLine(start = PointToSpecklePoint(line.start), end = PointToSpecklePoint(line.end))
    SpeckleLn.id = line.id
    SpeckleLn.units = project.units
    SpeckleLn.domain = project.domain
    SpeckleLn.length = line.length
    SpeckleLn.applicationId = project.applicationId
    SpeckleLn.color = 0
    return SpeckleLn


def PlaneToSpecklePlane(plane: Plane):
    SpecklePln = SpecklePlane(origin = PointToSpecklePoint(plane.Origin), normal = VectorToSpeckleVector(plane.Normal), xdir = VectorToSpeckleVector(plane.v1), ydir = VectorToSpeckleVector(plane.v2))
    SpecklePln.units = project.units
    return SpecklePln


def SpecklePolylineBySpecklePoints(polycurve: PolyCurve):
    SpecklePl = [PointToSpecklePoint(point) for point in polycurve.points]
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


def SpecklePolyline2DBySpecklePoints2D(polycurve: PolyCurve2D):
    SpecklePl = [PointToSpecklePoint(point) for point in polycurve.points2D]
    SpecklePolyln = SpecklePolyLine.from_points(SpecklePl)
    SpecklePolyln.id = polycurve.id
    SpecklePolyln.units = project.units
    SpecklePolyln.domain = project.domain
    SpecklePolyln.applicationId = project.applicationId
    try:
        SpecklePolyln.area = polycurve.area()
        SpecklePolyln.length = PolyCurve2D.length(polycurve)
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


def Point2DToSpecklePoint(Point2D: Point2D):
    SpecklePnt = SpecklePoint.from_coords(Point2D.x, Point2D.y, 0)
    SpecklePnt.units = project.units
    return SpecklePnt


def SpeckleMeshByMesh(MeshPB):
    color = -1762845660
    colrs = []
    for i in range(MeshPB.countVertsFaces):
        colrs.append(color)
    #colors = colrs
    SpeckleMsh = SpeckleMesh(applicationId = project.applicationId, vertices = MeshPB.verts, faces = MeshPB.faces, name = MeshPB.name, colors = colrs, units = project.units)
    return SpeckleMsh


def TextToSpeckleCurveSurface(Text):
    returnlist = []
    for polyc in Text.write():
        pc = PolyCurveToSpecklePolyLine(polyc)
        returnlist.append(pc)
    return returnlist


def SpeckleMeshByImage(img):
    SpeckleMsh = SpeckleMesh(applicationId = project.applicationId, vertices = img.vert, faces = img.faces, name = img.name, colors = img.colorlst)
    return SpeckleMsh


def ArcToSpeckleArc(arc: Arc):
    speckle_plane = SpecklePlane(
        origin = PointToSpecklePoint(arc.plane.Origin),
        normal = VectorToSpeckleVector(arc.plane.Normal),
        xdir = VectorToSpeckleVector(arc.plane.v1),
        ydir = VectorToSpeckleVector(arc.plane.v2),
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

def TransportToSpeckle(credential_data: str, SpeckleObjects: list):
    print(credential_data)
    new_streamid = None
    try:
        host = credential_data["speckle_server"]
        client = SpeckleClient(host=host)
        client.authenticate_with_token(credential_data["api_token"])
    except Exception as e:
        return False, f"Incorrect credentials, Error: {e}."

    if credential_data["stream_id"] == "":
        streamid = client.stream.create(name="Export from Struct4U", is_public=True) #credential_data["stream_name"]
    else:
        streamid = credential_data["stream_id"]
    
    messageCommit = credential_data["message_commit"]

    class SpeckleExport(Base):
        objects = None

    try:
        obj = SpeckleExport(objects = SpeckleObjects)
        transport = ServerTransport(client=client, stream_id=streamid)
        hash = operations.send(base=obj, transports=[transport])
    except Exception as e:
        return False, f"Failed to transport items to Speckle, Error: {e}."

    try:
        commit_id = client.commit.create(
            stream_id = streamid,
            object_id = hash,
            message = messageCommit,
        )
    except Exception as e:
        return False, f"Failed to create Speckle commit_id, Error: {e}."

    url = f"{host}/streams/{streamid}/commits/{commit_id}"
    return [True, url, streamid, commit_id]


def translateObjectsToSpeckleObjects(Obj):
    SpeckleObj = []
    for i in Obj:
        nm = i.__class__.__name__
        if nm == "list":
            if i == []:
                pass

        elif nm == 'Panel':
            colrs = i.colorlst
            SpeckleObj.append(SpeckleMesh(applicationId = project.applicationId,vertices=i.extrusion.verts, faces=i.extrusion.faces, colors = colrs, name = i.name, units = project.units))
        
        elif nm == 'Surface' or nm == 'Face':
            all_vertices = []
            all_faces = []
            all_colors = []
            for index in range(len(i.PolyCurveList)):
                all_vertices.append(i.mesh[index].verts)
                all_faces.append(i.mesh[index].faces)
                all_colors.append(i.colorlst[index])
            all_vertices = flatten(all_vertices)
            all_faces = flatten(all_faces)
            all_colors = flatten(all_colors)
            SpeckleObj.append(SpeckleMesh(applicationId = project.applicationId,vertices=all_vertices, faces=all_faces, colors=all_colors, name=i.name[index], units= project.units))

        elif nm == 'Frame':
            try:
                if i.comments.type == "Scia_Params":
                    SpeckleObj.append(SpeckleMesh(applicationId = project.applicationId, vertices=i.extrusion.verts, faces=i.extrusion.faces, colors = i.colorlst, name = i.profileName, units = project.units, Scia_Id=i.comments.id, Scia_Justification=i.comments.perpendicular_alignment, Scia_Layer=i.comments.layer, Scia_Rotation=i.comments.lcs_rotation, Scia_Staaf=i.comments.name, Scia_Type=i.comments.cross_section, Scia_Node_Start = i.comments.start_node, Scia_Node_End = i.comments.end_node, Revit_Rotation=str(i.comments.revit_rot), Scia_Layer_Type=i.comments.layer_type, Scia_XJustification=i.comments.Xjustification, Scia_YJustification=i.comments.Yjustification))
                else:
                    SpeckleObj.append(SpeckleMesh(applicationId = project.applicationId, vertices=i.extrusion.verts, faces=i.extrusion.faces, colors = i.colorlst, name = i.profileName, units = project.units))
            except:
                SpeckleObj.append(SpeckleMesh(applicationId = project.applicationId, vertices=i.extrusion.verts, faces=i.extrusion.faces, colors = i.colorlst, name = i.profileName, units = project.units))

        elif nm == "Extrusion":
            clrs = [] #i.colorlst
            SpeckleObj.append(SpeckleMesh(applicationId = project.applicationId,vertices=i.verts, faces=i.faces, colors = clrs, name = "n", units = project.units))

        elif nm == 'PolyCurve':
            SpeckleObj.append(SpecklePolylineBySpecklePoints(i))

        elif nm == 'PolyCurve2D':
            SpeckleObj.append(SpecklePolyline2DBySpecklePoints2D(i))

        elif nm == 'BoundingBox2d':
            SpeckleObj.append(SpecklePolylineBySpecklePoints(i))

        elif nm == 'ImagePyB':
            colrs = i.colorlst
            SpeckleObj.append(SpeckleMesh(applicationId = project.applicationId,vertices=i.verts, faces=i.faces, colors = colrs, name = i.name, units = project.units))

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

        elif nm == 'Node':
            SpeckleObj.append(PointToSpecklePoint(i.point))
            
#        elif nm == 'Text' or 'Text2':
#            SpeckleObj.append(TextToSpeckleCurveSurface(i))

        elif nm == 'Point2D':
            SpeckleObj.append(Point2DToSpecklePoint(i))

        elif nm == 'Grid':
            for j in GridToLines(i):
                SpeckleObj.append(j)

        elif nm == 'GridSystem':
            for j in GridSystemToLines(i):
                SpeckleObj.append(j)

        elif nm == 'imagePyB':
            SpeckleObj.append(SpeckleMeshByImage(i))

        else:
            print(f"{nm} Object not yet added to translateObjectsToSpeckleObjects")

    return SpeckleObj