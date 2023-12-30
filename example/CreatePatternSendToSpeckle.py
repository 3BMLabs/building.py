from exchange.pat import *
from geometry.curve import Line, Point
from project.fileformat import BuildingPy
import sys

project = BuildingPy("Test patterns","0")
project.speckleserver = "speckle.xyz"

pat1 = PAT().TilePattern("500x500", 500, 500, Revitmodelpattern)
pat2 = PAT().BlockPattern("Blokpatroon",300,4,Revitmodelpattern)
pat3 = PAT().ParallelLines("Bamboe",[0,150,100,100,50,150,50,100,100],Revitmodelpattern)

#CreatePatFile([pat1,pat2,pat3],'C:/TEMP/test3.pat')

# rules: ;;;angle, x-origin, y-origin, shift_pattern, offset(spacing), pen_down, pen_up (negatief waarde)

test = PATRow().create(0,0,0,0,250,0,0)
test = PATRow().create(0,0,0,0,250,0,0)
def PatRowGeom(patrow: PATRow, width: float, height: float):
    nlines = int(height /  patrow.offset_spacing)
    lines = []
    n = 0
    for i in range(nlines):
        if patrow.dash == 0 and patrow.space == 00:
            x_start = patrow.x_orig + patrow.shift_pattern
            y_start = patrow.y_orig + n * patrow.offset_spacing
            x_end = width + patrow.shift_pattern
            y_end = patrow.y_orig + math.tan(math.radians(patrow.angle))*width + n * patrow.offset_spacing
            lines.append(Line(Point(x_start,y_start,0),Point(x_end,y_end,0)))
            n = n + 1
    return lines

lines = PatRowGeom(test,2000,1000)

for i in lines:
    project.objects.append(i)

project.toSpeckle("3e34ec62e2")


#self.angle = 0
#self.x_orig = 0
#self.y_orig = 0
#self.shift_pattern = 0
#self.offset = 0

#self.dash = 0
#self.space = 0
#self.patstr = ""