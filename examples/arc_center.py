
from pathlib import Path
import sys
#import geometry.geometry2d

import sys, os, math
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from geometry.curve import Arc
from geometry.point import Point


arc = Arc.by_start_mid_end(Point(-1,0,0), Point(0, 1, 0), Point(1, 0, 0))
o = arc.origin