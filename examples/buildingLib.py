
from construction.panel import *
from construction.frame import *
from construction.profile import *
from exchange.speckle import *
from library.profile import data as jsondata
from library.material import *
from library.profile import nameToProfile
from construction.annotation import *
import threading

project = BuildingPy("Library Profiles","0")

# Export all steelprofiles to Speckle
lst = []
for item in jsondata:
	for i in item.values():
		lst.append(i[0]["synonyms"][0])

test = nameToProfile("HEA200")

#sys.exit()
#3D Frames
x = 0
y = 0
spacing = 1000
spacing_vert = 1500
height = 2000
count = 0
shape = "HEA"
type = "HEA"
#Mat = Material.byNameColor("Steel", Color().RGB([237, 237, 237]))

for i in lst:
	Mat = BaseSteel
	try:
		prof = i[:3]
		shape = i[:3]
		fram = Frame.by_startpoint_endpoint(Point(x, y, 0), Point(x, y, height), i, i, Mat).write(project)
		ColumnTag.by_frame(fram).write(project)

		x = x + spacing
		if type == shape:
			y = y
		else:
			x = 0
			y = y + spacing_vert
			type = shape
	except:
		print(i)

#project.to_speckle("4a80729464")