from BuildingPy import *

TotalWidth = 7700
Height = 4000
Length = 5000
Spacing = 610

div = DivisionSystem().by_fixed_distance_equal_division(Length,Spacing,0)

print(div.distances)