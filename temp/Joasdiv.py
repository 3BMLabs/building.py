from objects.panel import *
from objects.frame import *
from objects.steelshape import *
from exchange.speckle import *
from library.profile import searchProfile

# pan1 = Panel.byBaselineHeight(Line(start= Point(1000,0,0),end=Point(3000,0,0)),2500,150,"wand")
# pan2 = Panel.byBaselineHeight(Line(start= Point(1000,0,0),end=Point(3000,0,0)),2500,150,"wand")

test = searchProfile("R8")
print(test.shape_coords)


# lshape = Frame.byStartpointEndpoint(Point(0, 0, 0), Point(0, 0, 50),
#                                     Lshape("joas", 300, 200, 50, 50).curve, "L-frame", 0, "Steel")
# e1shape = Frame.byStartpointEndpoint(Point(400, 0, 0), Point(400, 0, 50),
#                                      Eshape("joas", 300, 200, 50).curve, "E1-frame", 0, "Steel")
# nshape = Frame.byStartpointEndpoint(Point(800, 0, 0), Point(800, 0, 50),
#                                     Nshape("joas", 300, 200, 50).curve, "N-frame", 0, "Steel")
# tshape = Frame.byStartpointEndpoint(Point(1200, 0, 0), Point(1200, 0, 50),
#                                     Tshape("joas", 300, 200, 60, 50).curve, "T-frame", 0, "Steel")
# e2shape = Frame.byStartpointEndpoint(Point(1600, 0, 0), Point(1600, 0, 50),
#                                      Eshape("joas", 300, 200, 50).curve, "E2-frame", 0, "Steel")
# arrowshape = Frame.byStartpointEndpoint(Point(2000, 0, 0), Point(2000, 0, 50),
#                                         Arrowshape("joas", 300, 200, 50, 100).curve, "Arrow-frame", 0, "Steel")


class Arrow:
    def __init__(self, x, y, z):

        self.arrowlist = None
        self.x = x
        self.y = y
        self.z = z

    def draw_arrow(self):
        self.arrowlist = []
        l1 = Line(start=Point(self.x, self.y, self.z), end=Point(self.x, self.y + 500, self.z))
        self.arrowlist.append(l1)
        l2 = Line(start=Point(self.x, self.y + 500, self.z), end=Point(self.x - 200, self.y + 500, self.z))
        self.arrowlist.append(l2)
        l3 = Line(start=Point(self.x - 200, self.y + 500, self.z), end=Point(self.x + 100, self.y + 1000, self.z))
        self.arrowlist.append(l3)
        l4 = Line(start=Point(self.x + 100, self.y + 1000, self.z), end=Point(self.x + 400, self.y + 500, self.z))
        self.arrowlist.append(l4)
        l5 = Line(start=Point(self.x + 400, self.y + 500, self.z), end=Point(self.x + 200, self.y + 500, self.z))
        self.arrowlist.append(l5)
        l6 = Line(start=Point(self.x + 200, self.y + 500, self.z), end=Point(self.x + 200, self.y, self.z))
        self.arrowlist.append(l6)
        l7 = Line(start=Point(self.x + 200, self.y, self.z), end=Point(self.x, self.y, self.z))
        self.arrowlist.append(l7)

        # self.arrowlist.append([l1, l2, l3, l4, l5, l6, l7])

        return self


a = Arrow(2400, -200, 0).draw_arrow()


SpeckleObj = translateObjectsToSpeckleObjects(a.arrowlist)
# SpeckleObj = translateObjectsToSpeckleObjects([lshape, e1shape, nshape, tshape, e2shape, arrowshape] + a.arrowlist)


# Commit = TransportToSpeckle("speckle.xyz", "8136460d9e", SpeckleObj, "Shiny Commit")
