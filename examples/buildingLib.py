from construction.panel import *
from construction.beam import *
from construction.profile import *
from exchange.speckle import *
from library.profile import data as jsondata
from library.material import *
from library.profile import get_profile_by_name
from construction.annotation import *

project = BuildingPy("Library Profiles", "0")

# Export all steelprofiles to Speckle
lst = [
    profile_name[0]["synonyms"][0]
    for item in jsondata
    for profile_name in item.values()
]


test = get_profile_by_name("HEA200")

# sys.exit()
# 3D Frames
x = 0
y = 0
spacing = 1000
spacing_vert = 1500
height = 2000
count = 0
last_type = None
# Mat = Material.byNameColor("Steel", Color().RGB([237, 237, 237]))

for profile_name in lst:
    #try:
        type = profile_name[:3]
        if last_type != None:
            if type == last_type:
                x = x + spacing
            else:
                x = 0
                y = y + spacing_vert
        last_type = type
        Mat = BaseSteel
        beam = Beam.by_startpoint_endpoint(
            Point(x, y, 0), Point(x, y, height), profile_name, profile_name, Mat
        )
        project += beam
        # ColumnTag.by_beam(beam).write(project)
    #except UnboundLocalError:
    #    pass

project.to_speckle("ed88c2cdb3")
