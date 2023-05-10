import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from temp.pil_img import imagePyB
from exchange.speckle import *

# newimg = imagePyB().byFile("C:/Users/JoasHollander/Documents/GitHub/building.py/temp/rgb.png", 50, 100, 10, -10, -10)
newimg = imagePyB().byFile("C:/Users/JoasHollander/Documents/GitHub/building.py/temp/bugatti-chiron.jpg", 100, 100, dx=10, dy=10)
newimg2 = imagePyB().byStream("https://onlinejpgtools.com/images/examples-onlinejpgtools/sunflower.jpg")

newimg.name = "small img2"
SpeckleObj = translateObjectsToSpeckleObjects([newimg2])
Commit = TransportToSpeckle("speckle.xyz", "8136460d9e", SpeckleObj, "Shiny Commit 1234567890")

# ====================================

from objects.shape3d import Origin

# neworigin = Origin().CreateOrigin()
# SpeckleObj = translateObjectsToSpeckleObjects([neworigin])
# Commit = TransportToSpeckle("speckle.xyz", "8136460d9e", SpeckleObj, "Shiny Commit 1234567890")
# lst = [SpeckleObjUp, SpeckleObjUp2, SpeckleObjRight, SpeckleObjRight2, SpeckleObjFront, SpeckleObjFront2]

# blabla = Origin.SpeckleOb()

# Commit = TransportToSpeckle("speckle.xyz", "8136460d9e", lst, "Shiny Commit")
