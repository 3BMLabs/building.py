FREECADPATH = 'C:\\Program Files\\FreeCAD 0.20\\bin' # path to your FreeCAD.so or FreeCAD.pyd file,
# for Windows you must either use \\ or / in the path, using a single \ is problematic
# FREECADPATH = 'C:\\FreeCAD\\bin'

import sys

sys.path.append(FREECADPATH)
import FreeCAD
#import FreeCAD as App

from pathlib import Path

# The folder and filename we will use:
fld = 'C:\\TEMP\\'
fnm = fld + 'test.FCStd'

# Make sure fld exists:
Path(fld).mkdir(parents=True, exist_ok=True)

doc = FreeCAD.newDocument()

sys.exit()
doc.saveAs(fnm)
doc.save()
doc = FreeCAD.open(fnm)

box = doc.addObject("Part::Box", "myBox")
box.Length = 4
box.Width = 8
box.Height = 12
box.Placement = App.Placement(App.Vector(1, 2, 3), App.Rotation(75, 60, 30))

doc.recompute()

doc.save()
FreeCAD.closeDocument(doc.Name)

