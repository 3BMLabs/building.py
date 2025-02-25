import sys, os


from construction.beam import *
from exchange.scia import *

from construction.analytical import *
from project.fileformat import BuildingPy

file_name = 'project/data.json'

with open(file_name, 'r') as file:
    serialized_data = file.read()


serialized_objects = json.loads(serialized_data)

project.objects = []
for serialized_obj in serialized_objects:
    obj_data = json.loads(serialized_obj)
    print(obj_data)
    if obj_data['type'] == 'Point':
        deserialize = Point.deserialize(obj_data)
        project.objects.append(deserialize)
    if obj_data['type'] == 'Vector':
        deserialize = Vector.deserialize(obj_data)
        project.objects.append(deserialize)
    if obj_data['type'] == 'Line':
        deserialize = Line.deserialize(obj_data)
        project.objects.append(deserialize)
project.to_speckle("c6e11e74cb")
# project.open(path) #check valid path, else corrupt