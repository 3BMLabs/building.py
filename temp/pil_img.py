import sys, os, math
from pathlib import Path
from typing import Any, List

sys.path.append(str(Path(__file__).resolve().parents[1]))

from exchange.speckle import *
from PIL import Image

class imagePyB:

    def __init__(self):
        self.imgpath = None
        self.pixels = None
        self.facenr = -1
        self.numberofpixels = 0
        self.vertx = 0
        self.verty = 0
        self.vertz = 0
        self.name = None
        self.kleurcode_rijen = []
        self.pixellist = []
        self.vert = []
        self.faces = []
        self.colorlst = []

    def rgb_to_int(self, rgb):
        r, g, b = [max(0, min(255, c)) for c in rgb]
        return (255 << 24) | (r << 16) | (g << 8) | b

    def byFile(self, imgpath):  
        self.imgpath = imgpath
        self.img = Image.open(self.imgpath)
        self.pixels = self.img.load()
        for y in range(self.img.height):
            rij_kleurcodes = []
            for x in range(self.img.width):
                rij_kleurcodes.append(self.pixels[x, y])
            self.kleurcode_rijen.append(rij_kleurcodes)

        for kleurcode_rij in self.kleurcode_rijen:
            for kleurcode in kleurcode_rij:
                self.pixellist.append(kleurcode)

        for i in self.pixellist:
            self.faces.append(4)
            self.vert.append(self.vertx)
            self.vert.append(self.verty)
            self.vert.append(self.vertz)
            self.facenr += 1
            self.faces.append(self.facenr)
            self.vertx += 1
            self.vert.append(self.vertx)
            self.vert.append(self.verty)
            self.vert.append(self.vertz)
            self.facenr += 1
            self.faces.append(self.facenr)
            self.verty -= 1
            self.vert.append(self.vertx)
            self.vert.append(self.verty)
            self.vert.append(self.vertz)
            self.facenr += 1
            self.faces.append(self.facenr)
            self.vertx -= 1
            self.vert.append(self.vertx)
            self.vert.append(self.verty)
            self.vert.append(self.vertz)
            self.facenr += 1
            self.faces.append(self.facenr)
            self.vertx += 1
            self.verty += 1
            self.numberofpixels += 1

            if self.numberofpixels == len(rij_kleurcodes):
                self.vertx = 0
                self.verty -= 1
                self.numberofpixels = 0

        for i in self.pixellist:
            argbint_color = self.rgb_to_int(i)
            self.colorlst.append(argbint_color)
            self.colorlst.append(argbint_color)
            self.colorlst.append(argbint_color)
            self.colorlst.append(argbint_color)
            #self.colorlst = None
        return self
