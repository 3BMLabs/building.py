from exchange.speckle import *
from PIL import Image


def send_img_to_speckle(img):
    # img = Image.open("photo.jpg")

    pixels = img.load()
    facenr = -1
    numberofpixels = 0
    vertx = 0
    verty = 0
    vertz = 0

    kleurcode_rijen = []
    pixellist = []
    vert = []
    faces = []
    colorlst = []

    def rgb_to_int(rgb):
        r, g, b = [max(0, min(255, c)) for c in rgb]
        return (255 << 24) | (r << 16) | (g << 8) | b

    for y in range(img.height):
        rij_kleurcodes = []
        for x in range(img.width):
            rij_kleurcodes.append(pixels[x, y])
        kleurcode_rijen.append(rij_kleurcodes)

    for kleurcode_rij in kleurcode_rijen:
        for kleurcode in kleurcode_rij:
            pixellist.append(kleurcode)

    for i in pixellist:
        faces.append(4)
        vert.append(vertx)
        vert.append(verty)
        vert.append(vertz)
        facenr += 1
        faces.append(facenr)
        vertx += 1
        vert.append(vertx)
        vert.append(verty)
        vert.append(vertz)
        facenr += 1
        faces.append(facenr)
        verty -= 1
        vert.append(vertx)
        vert.append(verty)
        vert.append(vertz)
        facenr += 1
        faces.append(facenr)
        vertx -= 1
        vert.append(vertx)
        vert.append(verty)
        vert.append(vertz)
        facenr += 1
        faces.append(facenr)
        vertx += 1
        verty += 1
        numberofpixels += 1

        if numberofpixels == len(rij_kleurcodes):
            vertx = 0
            verty -= 1
            numberofpixels = 0

    for i in pixellist:
        argbint_color = rgb_to_int(i)
        colorlst.append(argbint_color)
        colorlst.append(argbint_color)
        colorlst.append(argbint_color)
        colorlst.append(argbint_color)

    def SpeckleMeshByImage(verts, faces, name):
        spcklmesh = SpeckleMesh(vertices=verts, faces=faces, name=name, colors=colorlst)
        return spcklmesh

    SpeckleObj = [SpeckleMeshByImage(vert, faces, "First img")]
    # Commit = TransportToSpeckle("speckle.xyz", "8136460d9e", SpeckleObj, "Shiny Commit")
    # Commit = TransportToSpeckle(server_url, server_token, SpeckleObj, commit_message)
    # return Commit
    return SpeckleObj
