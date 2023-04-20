from exchange.speckle import *
from abstract.color import *

originx = 700
originy = 500
originz = -500
number_of_triangles = 30
number_of_rectangles = 40
r = 80
r2 = 30
vertices_up = [originx, originy, originz + 350]
vertices_right = [originx + 350, originy, originz]
vertices_front = [originx, originy + 350, originz]
faces_up = []
faces_right = []
faces_front = []
facenr = 1
degrees = 0
degrees2 = 360 / number_of_triangles

# UP ARROW ----------------------------------

for i in range(number_of_triangles):
    x = math.cos(math.radians(degrees)) * r
    y = math.sin(math.radians(degrees)) * r
    degrees += degrees2
    vertices_up.append(originx + x)
    vertices_up.append(originy + y)
    vertices_up.append(originz + 200)

    faces_up.append(3)
    faces_up.append(0)

    if facenr < number_of_triangles:
        faces_up.append(facenr)
        faces_up.append(facenr + 1)
        facenr += 1
    else:
        faces_up.append(number_of_triangles)
        faces_up.append(1)

        faces_up.append(number_of_triangles)
        for i in range(number_of_triangles):
            faces_up.append(i + 1)


vertices2 = []
faces2 = []
facenr2 = 0
degrees3 = 0
degrees4 = 360 / number_of_rectangles

for i in range(number_of_rectangles):
    x = math.cos(math.radians(degrees3)) * r2
    y = math.sin(math.radians(degrees3)) * r2
    vertices2.append(originx + x)
    vertices2.append(originy + y)
    vertices2.append(originz + 200)
    vertices2.append(originx + x)
    vertices2.append(originy + y)
    vertices2.append(originz)
    degrees3 += degrees4

    if facenr2 < number_of_rectangles * 2 - 2:
        faces2.append(4)
        faces2.append(facenr2)
        faces2.append(facenr2 + 1)
        faces2.append(facenr2 + 3)
        faces2.append(facenr2 + 2)
        facenr2 += 2
    else:
        faces2.append(4)
        faces2.append(facenr2)
        faces2.append(facenr2 + 1)
        faces2.append(1)
        faces2.append(0)

        faces2.append(number_of_rectangles)
        count = 1
        for i in range(number_of_rectangles):
            if count <= number_of_rectangles * 2:
                faces2.append(count)
                count += 2
            else:
                pass

# RIGHT ARROW ----------------------------------

degrees = 0
facenr = 1

for i in range(number_of_triangles):
    z = math.cos(math.radians(degrees)) * r
    y = math.sin(math.radians(degrees)) * r
    degrees += degrees2
    vertices_right.append(originx + 200)
    vertices_right.append(originy + y)
    vertices_right.append(originz + z)

    faces_right.append(3)
    faces_right.append(0)

    if facenr < number_of_triangles:
        faces_right.append(facenr)
        faces_right.append(facenr + 1)
        facenr += 1
    else:
        faces_right.append(number_of_triangles)
        faces_right.append(1)

        faces_right.append(number_of_triangles)
        for i in range(number_of_triangles):
            faces_right.append(i + 1)


vertices_right2 = []
faces_right2 = []
facenr2 = 0
degrees3 = 0
degrees4 = 360 / number_of_rectangles

for i in range(number_of_rectangles):
    z = math.cos(math.radians(degrees3)) * r2
    y = math.sin(math.radians(degrees3)) * r2
    vertices_right2.append(originx + 200)
    vertices_right2.append(originy + y)
    vertices_right2.append(originz + z)
    vertices_right2.append(originx)
    vertices_right2.append(originy + y)
    vertices_right2.append(originz + z)
    degrees3 += degrees4

    if facenr2 < number_of_rectangles * 2 - 2:
        faces_right2.append(4)
        faces_right2.append(facenr2)
        faces_right2.append(facenr2 + 1)
        faces_right2.append(facenr2 + 3)
        faces_right2.append(facenr2 + 2)
        facenr2 += 2
    else:
        faces_right2.append(4)
        faces_right2.append(facenr2)
        faces_right2.append(facenr2 + 1)
        faces_right2.append(1)
        faces_right2.append(0)

        faces_right2.append(number_of_rectangles)
        count = 1
        for i in range(number_of_rectangles):
            if count <= number_of_rectangles * 2:
                faces_right2.append(count)
                count += 2
            else:
                pass

# FRONT ARROW ----------------------------------

degrees = 0
facenr = 1

for i in range(number_of_triangles):
    z = math.cos(math.radians(degrees)) * r
    x = math.sin(math.radians(degrees)) * r
    degrees += degrees2
    vertices_front.append(originx + x)
    vertices_front.append(originy + 200)
    vertices_front.append(originz + z)

    faces_front.append(3)
    faces_front.append(0)

    if facenr < number_of_triangles:
        faces_front.append(facenr)
        faces_front.append(facenr + 1)
        facenr += 1
    else:
        faces_front.append(number_of_triangles)
        faces_front.append(1)

        faces_front.append(number_of_triangles)
        for i in range(number_of_triangles):
            faces_front.append(i + 1)


vertices_front2 = []
faces_front2 = []
facenr2 = 0
degrees3 = 0
degrees4 = 360 / number_of_rectangles

for i in range(number_of_rectangles):
    z = math.cos(math.radians(degrees3)) * r2
    x = math.sin(math.radians(degrees3)) * r2
    vertices_front2.append(originx + x)
    vertices_front2.append(originy + 200)
    vertices_front2.append(originz + z)
    vertices_front2.append(originx + x)
    vertices_front2.append(originy)
    vertices_front2.append(originz + z)
    degrees3 += degrees4

    if facenr2 < number_of_rectangles * 2 - 2:
        faces_front2.append(4)
        faces_front2.append(facenr2)
        faces_front2.append(facenr2 + 1)
        faces_front2.append(facenr2 + 3)
        faces_front2.append(facenr2 + 2)
        facenr2 += 2
    else:
        faces_front2.append(4)
        faces_front2.append(facenr2)
        faces_front2.append(facenr2 + 1)
        faces_front2.append(1)
        faces_front2.append(0)

        faces_front2.append(number_of_rectangles)
        count = 1
        for i in range(number_of_rectangles):
            if count <= number_of_rectangles * 2:
                faces_front2.append(count)
                count += 2
            else:
                pass


def SpeckleMeshByCone(verts, face):
    spcklmesh = SpeckleMesh(vertices=verts, faces=face, name="Joas", units="mm")
    return spcklmesh


SpeckleObjup = [SpeckleMeshByCone(vertices_up, faces_up)]
SpeckleObjup2 = [SpeckleMeshByCone(vertices2, faces2)]

SpeckleObjright = [SpeckleMeshByCone(vertices_right, faces_right)]
SpeckleObjright2 = [SpeckleMeshByCone(vertices_right2, faces_right2)]

SpeckleObjfront = [SpeckleMeshByCone(vertices_front, faces_front)]
SpeckleObjfront2 = [SpeckleMeshByCone(vertices_front2, faces_front2)]

lst = [SpeckleObjright, SpeckleObjright2, SpeckleObjup, SpeckleObjup2, SpeckleObjfront, SpeckleObjfront2]
# lst = [SpeckleObjright, SpeckleObjright2]
Commit = TransportToSpeckle("speckle.xyz", "8136460d9e", lst, "Shiny Commit")
