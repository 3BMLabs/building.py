
from pathlib import Path
import sys
#import geometry.geometry2d

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))
from geometry.curve import Arc
from geometry.point import Point


arc = Arc(Point(-1,0,0), Point(0, 1, 0), Point(1, 0, 0))
o = arc.origin