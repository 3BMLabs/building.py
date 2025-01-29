from construction.datum import *
from construction.panel import *
from geometry.systemsimple import *
from abstract.color import *

project = BuildingPy("Project warehouse","Progent")
project.speckleserver = "speckle.xyz"
grid_width = 1500
grid_length = 1000
grid_height = 1000

# name / x pos/ y neg /z pos
pallets = [
["C1R1P3",0,0,0],
["C1R1P2",1,0,0],
["C1R1P1",2,0,0],
["C1R2P3",0,2,0],
["C1R2P2",1,2,0],
["C1R2P1",2,2,0],
["C1R3P3",0,3,0],
["C1R3P2",1,3,0],
["C1R3P1",2,3,0],
["C1R4P3",0,5,0],
["C1R4P2",1,5,0],
["C1R4P1",2,5,0],
["C1R5P3",0,6,0],
["C1R5P2",1,6,0],
["C1R5P1",2,6,0],
["C1R6P3",0,8,0],
["C1R6P2",1,8,0],
["C1R6P1",2,8,0],
["C1R7P3",0,9,0],
["C1R7P2",1,9,0],
["C1R7P1",2,9,0],
["C1R8P3",0,11,0],
["C1R8P2",1,11,0],
["C1R8P1",2,11,0],
["C1R9P3",0,12,0],
["C1R9P2",1,12,0],
["C1R9P1",2,12,0],
["C1R10P3",0,14,0],
["C1R10P2",1,14,0],
["C1R10P1",2,14,0],
["C1R11P3",5,0,0],
["C1R11P2",6,0,0],
["C1R11P1",7,0,0],
["C1R12P3",5,2,0],
["C1R12P2",6,2,0],
["C1R12P1",7,2,0],
["C1R13P3",5,3,0],
["C1R13P2",6,3,0],
["C1R13P1",7,3,0],
["C1R14P3",5,5,0],
["C1R14P2",6,5,0],
["C1R14P1",7,5,0],
["C1R15P3",5,6,0],
["C1R15P2",6,6,0],
["C1R15P1",7,6,0],
["C1R16P3",5,8,0],
["C1R16P2",6,8,0],
["C1R16P1",7,8,0],
["C1R17P3",5,9,0],
["C1R17P2",6,9,0],
["C1R17P1",7,9,0],
["C1R18P3",5,11,0],
["C1R18P2",6,11,0],
["C1R18P1",7,11,0],
["C1R19P3",5,12,0],
["C1R19P2",6,12,0],
["C1R19P1",7,12,0],
["C1R20P3",5,14,0],
["C1R20P2",6,14,0],
["C1R20P1",7,14,0],
["C2R1P3",8,0,0],
["C2R1P2",9,0,0],
["C2R1P1",10,0,0],
["C2R2P3",8,2,0],
["C2R2P2",9,2,0],
["C2R2P1",10,2,0],
["C2R3P3",8,3,0],
["C2R3P2",9,3,0],
["C2R3P1",10,3,0],
["C2R4P3",8,5,0],
["C2R4P2",9,5,0],
["C2R4P1",10,5,0],
["C2R5P3",8,6,0],
["C2R5P2",9,6,0],
["C2R5P1",10,6,0],
["C2R6P3",8,8,0],
["C2R6P2",9,8,0],
["C2R6P1",10,8,0],
["C2R7P3",8,9,0],
["C2R7P2",9,9,0],
["C2R7P1",10,9,0],
["C2R8P3",8,11,0],
["C2R8P2",9,11,0],
["C2R8P1",10,11,0],
["C2R9P3",8,12,0],
["C2R9P2",9,12,0],
["C2R9P1",10,12,0],
["C2R10P3",8,14,0],
["C2R10P2",9,14,0],
["C2R10P1",10,14,0],
["C2R11P3",13,0,0],
["C2R11P2",14,0,0],
["C2R11P1",15,0,0],
["C2R12P3",13,2,0],
["C2R12P2",14,2,0],
["C2R12P1",15,2,0],
["C2R13P3",13,3,0],
["C2R13P2",14,3,0],
["C2R13P1",15,3,0],
["C2R14P3",13,5,0],
["C2R14P2",14,5,0],
["C2R14P1",15,5,0],
["C2R15P3",13,6,0],
["C2R15P2",14,6,0],
["C2R15P1",15,6,0],
["C2R16P3",13,8,0],
["C2R16P2",14,8,0],
["C2R16P1",15,8,0],
["C2R17P3",13,9,0],
["C2R17P2",14,9,0],
["C2R17P1",15,9,0],
["C2R18P3",13,11,0],
["C2R18P2",14,11,0],
["C2R18P1",15,11,0],
["C2R19P3",13,12,0],
["C2R19P2",14,12,0],
["C2R19P1",15,12,0],
["C2R20P3",13,14,0],
["C2R20P2",14,14,0],
["C2R20P1",15,14,0]
]

for pallet in pallets:
    z = 0
    n = 0
    for i in range(6):
        p1 = Point(pallet[1] * grid_width, pallet[2] * grid_length *-1, z)
        p2 = Point(pallet[1] * grid_width + grid_width, pallet[2] * grid_length * -1, z)
        p3 = Point(pallet[1] * grid_width + grid_width, pallet[2] * grid_length * -1-grid_length, z)
        p4 = Point(pallet[1] * grid_width, pallet[2] * grid_length * -1 - grid_length, z)
        PC = PolyCurve.by_points([p1,p2,p3,p4,p1])
        name = pallet[0] + "_level" + str(n)
        palletgeom = Panel.by_polycurve_thickness(PC,grid_height,0,name,rgb_to_int([237, 28, 36]))
        project.objects.append(palletgeom)
        z = z + grid_height
        n = n + 1

project.to_speckle("8fa09cee4f")