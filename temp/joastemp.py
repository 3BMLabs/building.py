import math
# from exchange.speckle import *
#
#
# def SpeckleMeshByMesh(verts, faces):
#     spcklmesh = SpeckleMesh(vertices=verts, faces=faces, name="Joas", units="mm")
#     return spcklmesh


number_of_triangles = 60
r = 10
vertices = [0, 0, 200]

z = 0
faces = []
facenr = 1
degrees = 0
degrees2 = 360 / number_of_triangles

for i in range(number_of_triangles):
    x = math.cos(math.radians(degrees)) * r
    y = math.sin(math.radians(degrees)) * r
    degrees += degrees2
    vertices.append(x)
    vertices.append(y)
    vertices.append(z)

    faces.append(3)
    faces.append(0)

    if facenr < number_of_triangles:
        faces.append(facenr)
        faces.append(facenr + 1)
        facenr += 1
    else:
        faces.append(number_of_triangles)
        faces.append(1)

print(vertices)
print(faces)
