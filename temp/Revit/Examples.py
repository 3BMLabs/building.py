import sys, os
# from pathlib import Path

# sys.path.append(str(Path(__file__).resolve().parents[2]))

# from objects.frame import *
# from exchange.scia import *

# from exchange.struct4U import *

# from objects.analytical import *
# from project.fileformat import project


# filepath = f"{os.getcwd()}\\temp\\Scia\\Examples buildingpy\\scia_temp.xml"

# project = BuildingPy("TempCommit", "0")

# LoadXML(filepath, project)

# project.toSpeckle("c6e11e74cb")
def test():
    return 12


# C:\Users\Jonathan\AppData\Local\python-3.9.12-embed-amd64\Lib
# import dateU
localapp = os.getenv(r'LOCALAPPDATA')
sys.path.append(os.path.join(localapp, r'python-3.9.12-embed-amd64\Lib'))

OUT = sys.path

#send the loadxml objects back
#so after send return the project.objects (start and end coords)
#all objects information send back