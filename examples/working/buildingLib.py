from abstract.vector import Point
from construction.beam import Beam
from library.material import BaseSteel
from library.profile import data as jsondata

from library.profile import profile_by_name
from project.fileformat import BuildingPy


project = BuildingPy("Library Profiles", "0")

# Export all steelprofiles to Speckle
lst = [
    profile_name[0]["synonyms"][0]
    for item in jsondata
    for profile_name in item.values()
]


test = profile_by_name("HEA200")

# sys.exit()
# 3D Frames
x = 0
y = 0
spacing = 1000
spacing_vert = 1500
height = 2000
count = 0
last_type = None
# Mat = Material.byNameColor("Steel", Color.RGB([237, 237, 237]))

for profile_name in lst:
    type = profile_name[:3]
    if last_type != None:
        if type == last_type:
            x = x + spacing
        else:
            x = 0
            y = y + spacing_vert
    last_type = type
    Mat = BaseSteel
    beam = Beam(
        Point(x, y, 0), Point(x, y, height), profile_name, profile_name, Mat
    )
    project += beam
    # ColumnTag.by_beam(beam).write(project)

project.to_speckle("ed88c2cdb3")
