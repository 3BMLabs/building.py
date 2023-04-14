#EXPORTER.py
from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_default_account
from specklepy.transports.server import ServerTransport
from specklepy.objects.geometry import Brep, Point
from specklepy.objects import Base
from specklepy.api import operations

def send_to_speckle(INhost, INstream_id, INobjects):
    account = get_default_account()
    client = SpeckleClient(host=INhost)
    client.authenticate_with_account(account)
    transport = ServerTransport(client=client, stream_id=INstream_id)
    class SpeckleExport(Base):
        objects = None
    obj = SpeckleExport(objects=INobjects)
    hash = operations.send(base=obj, transports=[transport])
    commit_id = client.commit.create(stream_id = INstream_id, object_id = hash, message = "NAN")
    print(commit_id)