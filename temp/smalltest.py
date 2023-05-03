import sys, os, math
from pathlib import Path
from typing import Any, List

sys.path.append(str(Path(__file__).resolve().parents[1]))

from temp.pil_img import imagePyB
from objects.frame import *
from objects.shape import *
from exchange.speckle import *

newimg = imagePyB().byFile("C:/Users/JoasHollander/Documents/GitHub/building.py/temp/rgb.png")
#newimg = imagePyB().byFile("C:/Users/JoasHollander/Documents/GitHub/building.py/temp/bugatti-chiron.jpg")

newimg.name = "small img2"

SpeckleObj = translateObjectsToSpeckleObjects([newimg])

#sys.exit()
Commit = TransportToSpeckle("speckle.xyz", "8136460d9e", SpeckleObj, "Shiny Commit 1234567890")
