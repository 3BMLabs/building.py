import sys, os, math
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from objects.panel import *
from objects.frame import *
from objects.steelshape import *
from exchange.speckle import *
from library.profile import data as jsondata
from library.material import *
from library.profile import profiledataToShape
from objects.annotation import *
from abstract.intersect2d import *
from geometry.systemsimple import *
from objects.shape import *
from sandbox_dev.Workspace.WorkEnvObject import *

project = BuildingPy("Split and Intersect examples","0")
project.speckleserver = "speckle.xyz"


c1 = PolyCurve.byPoints([Point(0,0,0), Point(100,0,0), Point(100,100,0), Point(0,100,0)])
c2 = Extrusion.byPolyCurveHeight(c1, 100, -100)


project.objects.append(c2)
for line in gridPlane(1000,500,100):
    project.objects.append(line)


def normalize(arr, t_min, t_max):
    norm_arr = []
    diff = t_max - t_min
    diff_arr = max(arr) - min(arr)
    for i in arr:
        temp = (((i - min(arr))*diff)/1) + t_min
        norm_arr.append(temp)
    return norm_arr


class Geometry:
    def Translate(object, v):
        if object.type == 'Point':
            p1 = Point.to_matrix(object)
            v1 = Vector3.to_matrix(v)

            ar1 = np.array([p1])
            ar2 = np.array([v1])

            c = np.add(ar1,ar2)[0]
            return Point(c[0], c[1], c[2])

        elif object.type == 'Line':
            return Line(Geometry.Translate(object.start, v), (Geometry.Translate(object.end, v)))

        elif object.type == "PolyCurve":
            translated_points = []

            # Extract the direction components from the Vector3 object
            direction_x, direction_y, direction_z = v.x, v.y, v.z

            for point in object.points:
                p1 = Point.to_array(point)
                # Apply the translation
                c = np.add(p1, [direction_x, direction_y, direction_z])
                translated_points.append(Point(c[0], c[1], c[2]))

            return PolyCurve.byPoints(translated_points)
        else:
            print(f"[translate] '{object.type}' object is not added yet")


class CoordinateSystem:
    #UNITY VECTORS REQUIRED
    def __init__(self, origin: Point, xaxis=None, yaxis=None, zaxis=None):
        self.type = __class__.__name__        
        self.Origin = origin
        self.Xaxis = xaxis or XAxis
        self.Yaxis = yaxis or YAxis
        self.Zaxis = zaxis or ZAxis
        # self.Length = length or 1
        # self.XScaleFactor = 0
        # self.YScaleFactor = 0
        # self.ZScaleFactor = 0

    @classmethod
    def ByOrigin(self, origin: Point):
        from abstract.coordinatesystem import XAxis, YAxis, ZAxis
        return self(origin, xaxis=XAxis, yaxis=YAxis, zaxis=ZAxis)


    @classmethod
    def ByOriginVectors(cls, origin: Point, XAxis, YAxis, ZAxis):
        XAxis = np.array([XAxis.x, XAxis.y, XAxis.z])
        YAxis = np.array([YAxis.x, YAxis.y, YAxis.z])
        ZAxis = np.array([ZAxis.x, ZAxis.y, ZAxis.z])

        XAxis = XAxis / np.linalg.norm(XAxis)

        YAxis = YAxis / np.linalg.norm(YAxis)
           
        ZAxis = ZAxis / np.linalg.norm(ZAxis)

        YAxis = YAxis - np.dot(YAxis, XAxis) * XAxis
        YAxis = YAxis / np.linalg.norm(YAxis)

        ZAxis = ZAxis - np.dot(ZAxis, XAxis) * XAxis - np.dot(ZAxis, YAxis) * YAxis
        ZAxis = ZAxis / np.linalg.norm(ZAxis)

        if str(XAxis[0]) == "nan" and str(XAxis[1]) == "nan" and str(XAxis[2]) == "nan":
            XAxis = np.array([0, 0, 0])

        if str(YAxis[0]) == "nan" and str(YAxis[1]) == "nan" and str(YAxis[2]) == "nan":
            YAxis = np.array([0, 0, 0])

        if str(ZAxis[0]) == "nan" and str(ZAxis[1]) == "nan" and str(ZAxis[2]) == "nan":
            ZAxis = np.array([0, 0, 0])

        return cls(origin, xaxis=Vector3.from_matrix(XAxis), yaxis=Vector3.from_matrix(YAxis), zaxis=Vector3.from_matrix(ZAxis))


    def Translate(CSOld, direction):
        from abstract.vector import Vector3
        pt = CSOld.Origin
        new_origin = Geometry.Translate(pt, direction)
        
        XAxis = Vector3(1, 0, 0)

        YAxis = Vector3(0, 1, 0)

        ZAxis = Vector3(0, 0, 1)

        CSNew = CoordinateSystem(new_origin,xaxis=XAxis,yaxis=YAxis,zaxis=ZAxis)

        CSNew.Origin = new_origin
        return CSNew

    @staticmethod
    def normalize(v):
        norm = np.linalg.norm(v)
        return v / norm if norm > 0 else v

    # @staticmethod
    # def Transform(CS1, CS2):
    #     # INCORRECT - start
    #     origin1 = np.array(CS1.Origin)
    #     origin2 = np.array(CS2.Origin)

    #     translated_origin = Point.to_matrix(origin1) + (Point.to_matrix(origin2) - Point.to_matrix(origin1))

    #     rotation_matrix = CoordinateSystem.CalculateRotationMatrix(CS1, CS2)

    #     new_xaxis = CoordinateSystem.normalize(np.dot(rotation_matrix, CS1.Xaxis))
    #     new_yaxis = CoordinateSystem.normalize(np.dot(rotation_matrix, CS1.Yaxis))
    #     new_zaxis = CoordinateSystem.normalize(np.dot(rotation_matrix, CS1.Zaxis))

    #     return CoordinateSystem(translated_origin, new_xaxis, new_yaxis, new_zaxis)
    #     # INCORRECT - end


    @staticmethod
    def TranslateOrigin(origin1, origin2):

        origin1_np = np.array([origin1.x, origin1.y, origin1.z])
        origin2_np = np.array([origin2.x, origin2.y, origin2.z])

        new_origin_np = origin1_np + (origin2_np - origin1_np)
        return Point(new_origin_np[0], new_origin_np[1], new_origin_np[2])

    @staticmethod
    def CalculateRotationMatrix(xaxis1, yaxis1, zaxis1, xaxis2, yaxis2, zaxis2):
        R1 = np.array([Vector3.to_matrix(xaxis1), Vector3.to_matrix(yaxis1), Vector3.to_matrix(zaxis1)]).T
        R2 = np.array([Vector3.to_matrix(xaxis2), Vector3.to_matrix(yaxis2), Vector3.to_matrix(zaxis2)]).T

        rotation_matrix = np.dot(R2, np.linalg.inv(R1))
        return rotation_matrix

    def __str__(self):
        return f"{__class__.__name__}(Origin = " + f"{self.Origin}, XAxis = {self.Xaxis}, YAxis = {self.Yaxis}, ZAxis = {self.Zaxis})"


def scale(object, v):
    if object.type == 'Point':
        p1 = Point.to_matrix(object)
        v1 = Vector3.to_matrix(v)

        p1 = np.array(p1).flatten()
        v1 = np.array(v1).flatten()

        c = p1 * v1
        return Point(c[0], c[1], c[2])

    elif object.type == 'Line':
        return Line(scale(object.start, v), scale(object.end, v))
    
    elif object.type == 'PolyCurve':
        ptList = []
        for point in object.points:
            ptList.append(scale(point, v))
        return PolyCurve.byPoints(ptList)
    else:
        print(f"[scale] '{object.type}' object is not added yet")

pt1 = Point(0,0,0)

c1 = CoordinateSystem.ByOrigin(pt1)

c2 = CoordinateSystem.Translate(c1, Vector3(0,1000,0))

c3 = CoordinateSystem.Translate(c2, Vector3(4500,-40,80))

print(c3)

pt2 = Point(9023,928,192)

v1 = Vector3(28,291,321)
v2 = Vector3(0,0,0)
v3 = Vector3(-902,3,54)

cs1 = CoordinateSystem.ByOriginVectors(pt2, v1, v2, v3)
print(cs1)

cs2 = CoordinateSystem.Transform(c3, cs1)
print(cs2)
# print(CSGlobal)
project.toSpeckle("75ccb04eec")