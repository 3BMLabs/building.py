from exchange.speckle import *

number_of_triangles = 30
r = 100
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

        faces.append(number_of_triangles)
        for i in range(number_of_triangles):
            faces.append(i + 1)


number_of_rectangles = 30
r2 = 30
vertices2 = []
faces2 = []
facenr2 = 0
degrees3 = 0
degrees4 = 360 / number_of_rectangles

for i in range(number_of_rectangles):
    x = math.cos(math.radians(degrees3)) * r2
    y = math.sin(math.radians(degrees3)) * r2
    vertices2.append(x)
    vertices2.append(y)
    vertices2.append(z)
    vertices2.append(x)
    vertices2.append(y)
    vertices2.append(-200)
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


def SpeckleMeshByCone(verts, face):
    spcklmesh = SpeckleMesh(vertices=verts, faces=face, name="Joas", units="mm")
    return spcklmesh


SpeckleObj = [SpeckleMeshByCone(vertices, faces)]
SpeckleObj2 = [SpeckleMeshByCone(vertices2, faces2)]
lst = [SpeckleObj, SpeckleObj2]
Commit = TransportToSpeckle("speckle.xyz", "8136460d9e", lst, "Shiny Commit")
