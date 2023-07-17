import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

# from temp.pil_img import imagePyB
from exchange.speckle import *
from temp.joastemp import Origin


neworigin = Origin().CreateOrigin()
print(neworigin)
SpeckleObj = translateObjectsToSpeckleObjects([neworigin])
Commit = TransportToSpeckle("speckle.xyz", "8136460d9e", SpeckleObj, "Shiny Commit")

# newimg = imagePyB().byFile("C:/Users/JoasHollander/Documents/GitHub/building.py/temp/rgb.png", 50, 100, 10, -10, -10)
# newimg2 = imagePyB().byStream("https://onlinejpgtools.com/images/examples-onlinejpgtools/sunflower.jpg")
# SpeckleObj = translateObjectsToSpeckleObjects([newimg2])
# Commit = TransportToSpeckle("speckle.xyz", "8136460d9e", SpeckleObj, "Shiny Commit 1234567890")
