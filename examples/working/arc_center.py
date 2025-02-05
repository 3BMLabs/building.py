
from pathlib import Path
import sys
#import geometry.geometry2d

from geometry.curve import Arc
from geometry.point import Point


arc = Arc.by_start_mid_end(Point(-1,0,0), Point(0, 1, 0), Point(1, 0, 0))
o = arc.origin