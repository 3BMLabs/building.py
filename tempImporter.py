# Import "specklepy.objects.geometry" could not be resolved

import sys, os, math
from pathlib import Path

file = Path(__file__).resolve()
package_root_directory = file.parents[0]
sys.path.append(str(package_root_directory))

# import packages.requests.requests as requests
# r = requests.get('https://google.com')
# print(r.status_code)

import packages.specklepy as specklepy
from packages.specklepy.api.client import SpeckleClient

from packages.specklepy.api.credentials import get_default_account
from packages.specklepy.transports.server import ServerTransport
from packages.specklepy.api import operations

#ERRORS
from packages.specklepy.objects import Base
# from packages.speckleEnv.specklepy.objects.geometry import Point as SpecklePoint