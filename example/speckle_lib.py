#Point
#SpeckleLine
#SpeckleArc
#Polyline
#SpeckleMesh
#Vector (cannot be visualised)
#Plane
#SpeckleInterval

#Section 1:
# -> Create plane / platform
# -> import text, check if text has converter ose
# -> text by each specklepy object.
# -> send to speckleserver (default method)
# -> consequent variable names / clean space after comma
# -> show everything in the right scale


from specklepy.api import operations
from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_default_account
from specklepy.transports.server import ServerTransport
from specklepy.objects import Base
from specklepy.objects.geometry import Point, Line, Arc, Polyline, Mesh, Vector, Plane, Interval


def send_to_speckle(host, stream_id, objects, msg=None):
    account = get_default_account()
    client = SpeckleClient(host=host)
    client.authenticate_with_account(account)
    transport = ServerTransport(client=client, stream_id=stream_id)
    class SpeckleExport(Base):
        objects = None
    obj = SpeckleExport(objects=objects)
    hash = operations.send(base=obj, transports=[transport])
    commit_id = client.commit.create(stream_id = stream_id, object_id = hash, message = msg)
    print(f"Export ID: {commit_id}")

#Vector - start, note: cannot be visualised
vectorObj = Vector.from_coords(1, 0, 0)
#Vector - end

#Point - start
pointObj = Point(x=0, y=0, z=0)
#Point - end

#Line - start
lineObj = Line(start=Point(x=10, y=0, z=0), end=Point(x=20, y=0, z=0))
#Line - end

#Arc - start
arcPlane = Plane(origin = Point.from_coords(10, 0, 0), normal = Vector.from_coords(0, 0, 1), xdir = Vector.from_coords(1, 0, 0), ydir = Vector.from_coords(0, 1, 0))
arcInterval = Interval(start=0, end=1, totalChildrenCount=1)
arcObj = Arc(startPoint=Point.from_coords(0, 0, 0), midPoint=Point.from_coords(1000, 0, 0), endPoint=Point.from_coords(2000, 500, 0), plane=arcPlane, radius=1, interval=arcInterval)
#Arc - end

#Polyline - start
polylineObj = Polyline.from_points([Point.from_coords(0,0,0), Point.from_coords(10,0,0), Point.from_coords(10,10,0), Point.from_coords(0,10,0), Point.from_coords(0,0,0)])
#Polyline - end

#Mesh - start
vertices=[0,0,0 , 1000,0,0 , 1000,1000,0 , 0,1000,0 , 0,0,1000 , 1000,0,1000 , 1000,1000,1000 , 0,1000,1000]
faces = [4,0,1,2,3, 4,0,1,5,4, 4,1,2,6,5, 4,4,5,6,7, 4,0,3,7,4, 4,3,2,6,7]

meshObj = Mesh(
    vertices=vertices,
    faces=faces,
    units="mm"
)
#Mesh - end



send_to_speckle(host="https://3bm.exchange", stream_id="fa4e56aed4", objects=[meshObj], msg="Point")

