import math
import urllib.request
import json
sqrt2 = math.sqrt(2)

class Vector:
    def __init__(self, x, y, z):
        self.x: float = 0.0
        self.y: float = 0.0
        self.z: float = 0.0

        self.x = x
        self.y = y
        self.z = z

    @staticmethod
    def sum(v1, v2):
        return Vector(
            v1.x + v2.x,
            v1.y + v2.y,
            v1.z + v2.z
        )

    @staticmethod
    def sum3(v1, v2, v3):
        return Vector(
            v1.x + v2.x + v3.x,
            v1.y + v2.y + v3.y,
            v1.z + v2.z + v3.z
        )

    @staticmethod
    def diff(v1, v2):
        return Vector(
            v1.x - v2.x,
            v1.y - v2.y,
            v1.z - v2.z
        )

    @staticmethod
    def divide(v1, v2):
        return Vector(
            v1.x / v2.x,
            v1.y / v2.y,
            v1.z / v2.z
        )

    @staticmethod
    def square(v1):
        return Vector(
            v1.x ** 2,
            v1.y ** 2,
            v1.z ** 2
        )

    @staticmethod
    def to_point(v1):
        from geometry.point import Point
        return Point(x=v1.x, y=v1.y, z=v1.z)

    @staticmethod
    def to_line(v1, v2):
        from geometry.point import Point
        from geometry.curve import Line
        return Line(start=Point(x=v1.x, y=v1.y, z=v1.z), end=Point(x=v2.x, y=v2.y, z=v2.z))

    @staticmethod
    def by_line(l1):
        from geometry.curve import Line
        return Vector(l1.dx, l1.dy, l1.dz)

    @staticmethod
    def line_by_length(v1, length: float):
        from geometry.point import Point
        from geometry.curve import Line
        return None
        # return Line(start = Point(x=v1.x,y=v1.y,z=v1.z), end = Point(x=v2.x,y=v2.y,z=v2.z))

    @staticmethod  # Returns vector perpendicular on the two vectors
    def cross_product(v1, v2):
        return Vector(
            v1.y * v2.z - v1.z * v2.y,
            v1.z * v2.x - v1.x * v2.z,
            v1.x * v2.y - v1.y * v2.x
        )

    @staticmethod  # inwendig product, if zero, then vectors are perpendicular
    def dot_product(v1, v2):
        return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z

    @staticmethod
    def product(n, v1):  # Same as scale
        return Vector(
            v1.x * n,
            v1.y * n,
            v1.z * n
        )

    @staticmethod
    def length(v1):
        return math.sqrt(v1.x * v1.x + v1.y * v1.y + v1.z * v1.z)

    # @staticmethod
    # def length(v1):
    #     return (v1.x ** 2 + v1.y ** 2 + v1.z ** 2) ** 0.5

    @staticmethod
    def pitch(v1, angle):
        return Vector(
            v1.x,
            v1.y * math.cos(angle) - v1.z * math.sin(angle),
            v1.y * math.sin(angle) + v1.z * math.cos(angle)
        )

    @staticmethod
    def angle_between(v1, v2):
        return math.degrees(math.acos((Vector.dot_product(v1, v2) / (Vector.length(v1) * Vector.length(v2)))))

    @staticmethod
    def angle_radian_between(v1, v2):
        return math.acos((Vector.dot_product(v1, v2) / (Vector.length(v1) * Vector.length(v2))))

    @staticmethod
    def value(v1):
        roundValue = 4
        return (round(v1.x, roundValue), round(v1.y, roundValue), round(v1.z, roundValue))

    @staticmethod
    def reverse(v1):
        return Vector(
            v1.x * -1,
            v1.y * -1,
            v1.z * -1
        )

    @staticmethod
    def perpendicular(v1):
        # Vector Lokale x en Lokale y haaks op gegeven vector en in globale z-richting.
        lokX = Vector(v1.y, -v1.x, 0)
        lokZ = Vector.cross_product(v1, lokX)
        if lokZ.z < 0:
            lokZ = Vector.reverse(lokZ)
        return lokX, lokZ

    @staticmethod
    def normalize(v1):
        length = Vector.length(v1)
        if length == 0:
            scale = 1
        else:
            scale = 1 / length
        return Vector(v1.x * scale, v1.y * scale, v1.z * scale)

    @staticmethod
    def by_two_points(p1, p2):
        return Vector(
            p2.x - p1.x,
            p2.y - p1.y,
            p2.z - p1.z
        )

    @staticmethod
    def rotate_XY(v1, Beta):
        return Vector(
            math.cos(Beta) * v1.x - math.sin(Beta) * v1.y,
            math.sin(Beta) * v1.x + math.cos(Beta) * v1.y,
            v1.z
        )

    @staticmethod
    def scale(v1, scalefactor):
        return Vector(
            v1.x * scalefactor,
            v1.y * scalefactor,
            v1.z * scalefactor
        )

    @staticmethod
    def new_length(v1, newlength: float):
        scale = newlength / Vector.length(v1)

        return Vector.scale(v1, scale)

    def __str__(self):
        return f"{__class__.__name__}(" + f"{self.x},{self.y},{self.z})"


X_axis = Vector(1, 0, 0)

Y_Axis = Vector(0, 1, 0)

Z_Axis = Vector(0, 0, 1)


class Point:
    def __init__(self, x, y, z):
        self.x: float = 0.0
        self.y: float = 0.0
        self.z: float = 0.0
        self.x = x
        self.y = y
        self.z = z
        self.value = self.x, self.y, self.z
        self.units = "mm"

    def __str__(self) -> str:
        return f"{__class__.__name__}({self.x},{self.y},{self.z})"

    @staticmethod
    def distance(point1, point2):
        return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2 + (point1.z - point2.z) ** 2)

    @staticmethod
    def distance_list(points: list) -> float:
        distances = []
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                distances.append((points[i], points[j], Point.distance(points[i], points[j])))
        distances.sort(key=lambda x: x[2])
        return distances

    @staticmethod
    def difference(pointxyz1, pointxyz2):
        from abstract.vector import Vector
        return Vector(
            pointxyz2.x - pointxyz1.x,
            pointxyz2.y - pointxyz1.y,
            pointxyz2.z - pointxyz1.z
        )

    @staticmethod
    def translate(point, vector):
        return Point(
            point.x + vector.x,
            point.y + vector.y,
            point.z + vector.z
        )

    @staticmethod
    def origin(point1, point2):
        return Point(
            (point1.x + point2.x) / 2,
            (point1.y + point2.y) / 2,
            (point1.z + point2.z) / 2
        )

    @staticmethod
    def point_2D_to_3D(point2D):
        from geometry.geometry2d import Point2D
        return Point(
            point2D.x,
            point2D.y,
            0
        )

    @staticmethod
    def to_vector(point1):
        from abstract.vector import Vector
        return Vector(
            point1.x,
            point1.y,
            point1.z
        )

    @staticmethod
    def sum(p1, p2):
        return Point(
            p1.x + p2.x,
            p1.y + p2.y,
            p1.z + p2.z
        )

    @staticmethod
    def diff(p1, p2):
        return Point(
            p1.x - p2.x,
            p1.y - p2.y,
            p1.z - p2.z
        )

    @staticmethod
    def rotate_XY(p1, Beta, dz):
        return Point(
            math.cos(math.radians(Beta)) * p1.x - math.sin(math.radians(Beta)) * p1.y,
            math.sin(math.radians(Beta)) * p1.x + math.cos(math.radians(Beta)) * p1.y,
            p1.z + dz
        )

    @staticmethod
    def product(n, p1):  # Same as scale
        return Point(
            p1.x * n,
            p1.y * n,
            p1.z * n
        )

    @staticmethod
    def intersect(p1, p2):
        # Intersection of two points
        if p1.x == p2.x and p1.y == p2.y and p1.z == p2.z:
            return 1
        else:
            return 0


class CoordinateSystem:
    #UNITY VECTORS REQUIRED #TOdo organize resic
    def __init__(self, origin: Point, x_axis, y_axis, z_axis):
        self.Origin = origin
        self.Xaxis = Vector.normalize(x_axis)
        self.Y_axis = Vector.normalize(y_axis)
        self.Z_axis = Vector.normalize(z_axis)

    @classmethod
    def by_origin(self, origin: Point):
        self.Origin = origin
        self.Xaxis = X_axis
        self.Y_axis = Y_Axis
        self.Z_axis = Z_Axis
        return self

    @staticmethod
    def translate(CSOld, direction):
        CSNew = CoordinateSystem(CSOld.Origin, CSOld.X_axis, CSOld.Y_axis, CSOld.Z_axis)
        new_origin = Point.translate(CSNew.Origin, direction)
        CSNew.Origin = new_origin
        return CSNew

    @staticmethod
    def move_local(CSOld,x: float, y:float, z:float):
        #move coordinatesystem by y in local coordinates(not global)
        xloc_vect_norm = CSOld.X_axis
        xdisp = Vector.scale(xloc_vect_norm,x)
        yloc_vect_norm = CSOld.X_axis
        ydisp = Vector.scale(yloc_vect_norm, y)
        zloc_vect_norm = CSOld.X_axis
        zdisp = Vector.scale(zloc_vect_norm, z)
        disp = Vector.sum3(xdisp,ydisp,zdisp)
        CS = CoordinateSystem.translate(CSOld,disp)
        return CS

    @staticmethod
    def by_point_main_vector(self, NewOriginCoordinateSystem: Point, DirectionVectorZ):
        vz = DirectionVectorZ  # LineVector and new Z-axis
        vz = Vector.normalize(vz)  # NewZAxis
        vx = Vector.perpendicular(vz)[0]  # NewXAxis
        try:
            vx = Vector.normalize(vx)  # NewXAxisnormalized
        except:
            vx = Vector(1, 0, 0) #In case of vertical element the length is zero
        vy = Vector.perpendicular(vz)[1]  # NewYAxis
        try:
            vy = Vector.normalize(vy)  # NewYAxisnormalized
        except:
            vy = Vector(0, 1, 0)  #In case of vertical element the length is zero
        CSNew = CoordinateSystem(NewOriginCoordinateSystem, vx, vy, vz)
        return CSNew

    def __str__(self):
        return f"{__class__.__name__}(" + f"{self.Origin}, {self.Xaxis}, {self.Y_axis}, {self.Z_axis})"

CSGlobal = CoordinateSystem(Point(0, 0, 0), X_axis, Y_Axis, Z_Axis)


def transform_point(PointLocal: Point, CoordinateSystemOld: CoordinateSystem, NewOriginCoordinateSystem: Point,
                   DirectionVector):
    from abstract.vector import Vector
    vz = DirectionVector  # LineVector and new Z-axis
    vz = Vector.normalize(vz)  # NewZAxis
    vx = Vector.perpendicular(vz)[0]  # NewXAxis
    try:
        vx = Vector.normalize(vx)  # NewXAxisnormalized
    except:
        vx = Vector(1, 0, 0)  # In case of vertical element the length is zero
    vy = Vector.perpendicular(vz)[1]  # NewYAxis
    try:
        vy = Vector.normalize(vy)  # NewYAxisnormalized
    except:
        vy = Vector(0, 1, 0)  # In case of vertical element the length is zero
    P1 = PointLocal  # point to transform
    CSNew = CoordinateSystem(NewOriginCoordinateSystem, vx, vy, vz)
    v1 = Point.difference(CoordinateSystemOld.Origin, CSNew.Origin)
    v2 = Vector.product(P1.x, CSNew.Xaxis)  # local transformation van X
    v3 = Vector.product(P1.y, CSNew.Y_axis)  # local transformation van Y
    v4 = Vector.product(P1.z, CSNew.Z_axis)  # local transformation van Z
    vtot = Vector(v1.x + v2.x + v3.x + v4.x, v1.y + v2.y + v3.y + v4.y, v1.z + v2.z + v3.z + v4.z)
    pointNew = Point.translate(Point(0, 0, 0), vtot)  # Point 0,0,0 have to be checked
    return pointNew


def transform_point_2(PointLocal: Point, CoordinateSystemNew: CoordinateSystem):
    # Transfrom point from Global Coordinatesystem to a new Coordinatesystem
    # CSold = CSGlobal
    from abstract.vector import Vector
    pn = Point.translate(CoordinateSystemNew.Origin, Vector.scale(CoordinateSystemNew.Xaxis, PointLocal.x))
    pn2 = Point.translate(pn, Vector.scale(CoordinateSystemNew.Y_axis, PointLocal.y))
    pn3 = Point.translate(pn2, Vector.scale(CoordinateSystemNew.Z_axis, PointLocal.z))
    return pn3

class Vector2:
    def __init__(self, x, y) -> None:
        self.x: float = 0.0
        self.y: float = 0.0
        self.x = x
        self.y = y

    @staticmethod
    def by_two_points(p1, p2):
        return Vector2(
            p2.x - p1.x,
            p2.y - p1.y
        )

    @staticmethod
    def length(v1):
        return math.sqrt(v1.x * v1.x + v1.y * v1.y)

    @staticmethod
    def scale(v1, scalefactor):
        return Vector2(
            v1.x * scalefactor,
            v1.y * scalefactor
        )

    @staticmethod
    def normalize(v1):
        scale = 1 / Vector2.length(v1)
        return Vector2(
            v1.x * scale,
            v1.y * scale
        )

    @staticmethod  # inwendig product, if zero, then vectors are perpendicular
    def dot_product(v1, v2):
        return v1.x * v2.x + v1.y * v2.y

    @staticmethod
    def angle_between(v1, v2):
        return math.degrees(math.acos((Vector2.dot_product(v1, v2) / (Vector2.length(v1) * Vector2.length(v2)))))

    @staticmethod
    def angle_radian_between(v1, v2):
        return math.acos((Vector2.dot_product(v1, v2) / (Vector2.length(v1) * Vector2.length(v2))))

    def __id__(self):
        return f"id:{self.id}"

    def __str__(self) -> str:
        return f"{__class__.__name__}({self.X},{self.Y})"


class Point2D:
    def __init__(self, x, y) -> None:
        self.x: float = 0.0
        self.y: float = 0.0
        self.x = x
        self.y = y

    def __id__(self):
        return f"id:{self.id}"

    def translate(self, vector: Vector2):
        x = self.x + vector.x
        y = self.y + vector.y
        p1 = Point2D(x, y)
        return p1

    def rotate(self, rotation):
        x = self.x
        y = self.y
        r = math.sqrt(x * x + y * y)
        rotationstart = math.degrees(math.atan2(y, x))
        rotationtot = rotationstart + rotation
        xn = round(math.cos(math.radians(rotationtot)) * r, 3)
        yn = round(math.sin(math.radians(rotationtot)) * r, 3)
        p1 = Point2D(xn, yn)
        return p1

    def __str__(self) -> str:
        return f"{__class__.__name__}({self.x},{self.y})"

    @staticmethod
    def distance(point1, point2):
        return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

    @staticmethod
    def midpoint(point1, point2):
        return Point2D((point2.x - point1.x) / 2, (point2.y - point1.y) / 2)

    @staticmethod
    def to_pixel(point1, Xmin, Ymin, TotalWidth, TotalHeight, ImgWidthPix: int, ImgHeightPix: int):
        # Convert Point to pixel on a image given a deltaX, deltaY, Width of the image etc.
        x = point1.x
        y = point1.y
        xpix = math.floor(((x - Xmin) / TotalWidth) * ImgWidthPix)
        ypix = ImgHeightPix - math.floor(
            ((y - Ymin) / TotalHeight) * ImgHeightPix)  # min vanwege coord stelsel Image.Draw
        return xpix, ypix


def transform_point_2D(PointLocal1: Point2D, CoordinateSystemNew: CoordinateSystem):
    # Transform point from Global Coordinatesystem to a new Coordinatesystem
    # CSold = CSGlobal
    from abstract.vector import Vector
    from geometry.point import Point
    PointLocal = Point(PointLocal1.x, PointLocal1.y, 0)
    pn = Point.translate(CoordinateSystemNew.Origin, Vector.scale(CoordinateSystemNew.Xaxis, PointLocal.x))
    pn2 = Point.translate(pn, Vector.scale(CoordinateSystemNew.Y_axis, PointLocal.y))
    pn3 = Point2D(pn.x, pn.y)
    return pn3


class Line2D:
    def __init__(self, pntxy1, pntxy2) -> None:
        self.start: Point2D = pntxy1
        self.end: Point2D = pntxy2
        self.x = [self.start.x, self.end.x]
        self.y = [self.start.y, self.end.y]
        self.dx = self.start.x - self.end.x
        self.dy = self.start.y - self.end.y
        self.length = 0

    def length(self):
        self.length = math.sqrt(self.dx * self.dx + self.dy * self.dy)
        return self.length

    def f_line(self):
        # returns line for Folium(GIS)
        return [[self.start.y, self.start.x], [self.end.y, self.end.x]]

    def __str__(self) -> str:
        return f"{__class__.__name__}({self.start},{self.end})"


class Arc2D:
    def __init__(self, pntxy1, pntxy2, pntxy3) -> None:
        self.start: Point2D = pntxy1
        self.mid: Point2D = pntxy2
        self.end: Point2D = pntxy3
        self.origin = self.origin_arc()
        self.angle_radian = self.angle_radian()
        self.radius = self.radius_arc()
        self.coordinatesystem = self.coordinatesystem_arc()
        # self.length

    def points(self):
        # returns point on the curve
        return (self.start, self.mid, self.end)

    def coordinatesystem_arc(self):
        vx2d = Vector2.by_two_points(self.origin, self.start)  # Local X-axe
        vx = Vector(vx2d.x, vx2d.y, 0)
        vy = Vector(vx.y, vx.x * -1, 0)
        vz = Vector(0, 0, 1)
        self.coordinatesystem = CoordinateSystem(self.origin, Vector.normalize(vx), Vector.normalize(vy),
                                                 Vector.normalize(vz))
        return self.coordinatesystem

    def angle_radian(self):
        v1 = Vector2.by_two_points(self.origin, self.end)
        v2 = Vector2.by_two_points(self.origin, self.start)
        angle = Vector2.angle_radian_between(v1, v2)
        return angle

    def origin_arc(self):
        # calculation of origin of arc #Todo can be simplified for sure
        Vstartend = Vector2.by_two_points(self.start, self.end)
        halfVstartend = Vector2.scale(Vstartend, 0.5)
        b = 0.5 * Vector2.length(Vstartend)  # half distance between start and end
        x = math.sqrt(Arc2D.radius_arc(self) * Arc2D.radius_arc(self) - b * b)  # distance from start-end line to origin
        mid = Point2D.translate(self.start, halfVstartend)
        v2 = Vector2.by_two_points(self.mid, mid)
        v3 = Vector2.normalize(v2)
        tocenter = Vector2.scale(v3, x)
        center = Point2D.translate(mid, tocenter)
        # self.origin = center
        return center

    def radius_arc(self):
        a = Vector2.length(Vector2.by_two_points(self.start, self.mid))
        b = Vector2.length(Vector2.by_two_points(self.mid, self.end))
        c = Vector2.length(Vector2.by_two_points(self.end, self.start))
        s = (a + b + c) / 2
        A = math.sqrt(s * (s - a) * (s - b) * (s - c))
        R = (a * b * c) / (4 * A)
        return R

    @staticmethod
    def points_at_parameter(arc, count: int):
        # Create points at parameter on an arc based on an interval
        d_alpha = arc.angle_radian / (count - 1)
        alpha = 0
        pnts = []
        for i in range(count):
            pnts.append(Point2D(arc.radius * math.cos(alpha), arc.radius * math.sin(alpha), 0))
            alpha = alpha + d_alpha
        CSNew = arc.coordinatesystem
        pnts2 = []  # transformed points
        for i in pnts:
            pnts2.append(transform_point_2D(i, CSNew))
        return pnts2

    @staticmethod
    def segmented_arc(arc, count):
        pnts = Arc2D.points_at_parameter(arc, count)
        i = 0
        lines = []
        for j in range(len(pnts) - 1):
            lines.append(Line2D(pnts[i], pnts[i + 1]))
            i = i + 1
        return lines

    def __str__(self):
        return f"{__class__.__name__}({self.start},{self.mid},{self.end})"


class PolyCurve2D:
    def __init__(self) -> None:
        self.curves = []  # collect in list
        self.points2D = []

    @classmethod
    def by_joined_curves(cls, curves):
        pc = PolyCurve2D()
        for i in curves:
            pc.curves.append(i)
            pc.points2D.append(i.start)
            pc.points2D.append(i.end)
        return pc

    def points(self):
        for i in self.curves:
            self.points2D.append(i.start)
            self.points2D.append(i.end)
        return self.points2D

    @classmethod
    def by_points(self, points: list):
        plycrv = PolyCurve2D()
        for index, point2D in enumerate(points):
            plycrv.points2D.append(point2D)
            try:
                nextpoint = points[index + 1]
                plycrv.curves.append(Line2D(point2D, nextpoint))
            except:
                firstpoint = points[0]
                plycrv.curves.append(Line2D(point2D, firstpoint))
        return plycrv

    def translate(self, vector2d: Vector2):
        crvs = []
        v1 = vector2d
        for i in self.curves:
            if i.__class__.__name__ == "Arc2D":
                crvs.append(Arc2D(i.start.translate(v1), i.mid.translate(v1), i.end.translate(v1)))
            elif i.__class__.__name__ == "Line2D":
                crvs.append(Line2D(i.start.translate(v1), i.end.translate(v1)))
            else:
                print("Curvetype not found")
        crv = PolyCurve2D.by_joined_curves(crvs)
        return crv

    def rotate(self, rotation):
        crvs = []
        for i in self.curves:
            if i.__class__.__name__ == "Arc2D":
                crvs.append(Arc2D(i.start.rotate(rotation), i.mid.rotate(rotation), i.end.rotate(rotation)))
            elif i.__class__.__name__ == "Line2D":
                crvs.append(Line2D(i.start.rotate(rotation), i.end.rotate(rotation)))
            else:
                print("Curvetype not found")
        crv = PolyCurve2D.by_joined_curves(crvs)
        return crv

    @staticmethod
    def boundingbox_global_CS(PC):
        x = []
        y = []
        for i in PC.curves():
            x.append(i.start.x)
            y.append(i.start.y)
        xmin = min(x)
        xmax = max(x)
        ymin = min(y)
        ymax = max(y)
        bbox = PolyCurve2D.by_points(
            [Point2D(xmin, ymin), Point2D(xmax, ymin), Point2D(xmax, ymax), Point2D(xmin, ymax), Point2D(xmin, ymin)])
        return bbox

    @staticmethod
    def bounds(PC):
        # returns xmin,xmax,ymin,ymax,width,height of polycurve 2D
        x = []
        y = []
        for i in PC.curves:
            x.append(i.start.x)
            y.append(i.start.y)
        xmin = min(x)
        xmax = max(x)
        ymin = min(y)
        ymax = max(y)
        width = xmax - xmin
        height = ymax - ymin
        return xmin, xmax, ymin, ymax, width, height

    @staticmethod
    def polygon(self):
        points = []
        for i in self.curves:
            if i == Arc2D:
                points.append(i.start, i.mid)  #
            else:
                points.append(i.start)
        points.append(points[0])
        return points


#   def __str__(self) -> str:
#        return f"{__class__.__name__}({self})"


class Surface2D:
    def __init__(self) -> None:
        pass  # PolyCurve2D

    pass  # opening(PolyCurve2D)

    def __id__(self):
        return f"id:{self.id}"

    def __str__(self) -> str:
        return f"{__class__.__name__}({self})"


class Profile2D:
    def __init__(self) -> None:
        pass  # Surface2D, collect curves and add parameters

    # voorzien van parameters
    # gebruiken voor objecten(kanaalplaatvloer, HEA200, iets)
    pass

    def __id__(self):
        return f"id:{self.id}"

    def __str__(self) -> str:
        return f"{__class__.__name__}({self})"


class ParametricProfile2D:
    def __init__(self) -> None:
        pass  # iets van profile hier inladen

    # Aluminium
    # Generic
    # Precast Concrete
    # ParametricProfile2D
    pass

    def __id__(self):
        return f"id:{self.id}"

    def __str__(self) -> str:
        return f"{__class__.__name__}({self})"


class CChannelParallelFlange:
    def __init__(self, name, h, b, tw, tf, r, ex):
        self.Description = "C-channel with parallel flange"
        self.ID = "C_PF"

        #parameters
        self.name = name
        self.curve = []
        self.h = h          #height
        self.b = b          #width
        self.tw = tw        #web thickness
        self.tf = tf        #flange thickness
        self.r1 = r        #web fillet
        self.ex = ex        #centroid horizontal


        #describe points
        p1 = Point2D(-ex, -h / 2)  # left bottom
        p2 = Point2D(b - ex, -h / 2)  # right bottom
        p3 = Point2D(b - ex, -h / 2 + tf)
        p4 = Point2D(-ex + tw + r, -h / 2 + tf)  # start arc
        p5 = Point2D(-ex + tw + r, -h / 2 + tf + r)  # second point arc
        p6 = Point2D(-ex + tw, -h / 2 + tf + r)  # end arc
        p7 = Point2D(-ex + tw, h / 2 - tf - r)  # start arc
        p8 = Point2D(-ex + tw + r, h / 2 - tf - r)  # second point arc
        p9 = Point2D(-ex + tw + r, h / 2 - tf)  # end arc
        p10 = Point2D(b - ex, h / 2 - tf)
        p11 = Point2D(b - ex, h / 2)  # right top
        p12 = Point2D(-ex, h / 2)  # left top

        #describe curves
        l1 = Line2D(p1, p2)
        l2 = Line2D(p2, p3)
        l3 = Line2D(p3, p4)
        l4 = Arc2D(p4, p5, p6)
        l5 = Line2D(p6, p7)
        l6 = Arc2D(p7, p8, p9)
        l7 = Line2D(p9, p10)
        l8 = Line2D(p10, p11)
        l9 = Line2D(p11, p12)
        l10 = Line2D(p12, p1)

        self.curve = PolyCurve2D().by_joined_curves([l1, l2, l3, l4, l5, l6, l7, l8, l9, l10])

    def __str__(self):
        return "Profile(" + f"{self.name})"


class CChannelSlopedFlange:
    def __init__(self, name, h, b, tw, tf, r1, r2, tl, sa, ex):
        self.Description = "C-channel with sloped flange"
        self.ID = "C_SF"

        # parameters
        self.name = name
        self.curve = []
        self.b = b  # width
        self.h = h  # height
        self.tf = tf  # flange thickness
        self.tw = tw  # web thickness
        self.r1 = r1  # web fillet
        self.r11 = r1 / sqrt2
        self.r2 = r2  # flange fillet
        self.r21 = r2 / sqrt2
        self.tl = tl  # flange thickness location from right
        self.sa = math.radians(sa)  # the angle of sloped flange in degrees
        self.ex = ex  # centroid horizontal

        # describe points
        p1 = Point2D(-ex, -h / 2)  # left bottom
        p2 = Point2D(b - ex, -h / 2)  # right bottom
        p3 = Point2D(b - ex, -h / 2 + tf - math.tan(self.sa) * tl - r2)  # start arc
        p4 = Point2D(b - ex - r2 + self.r21, -h / 2 + tf - math.tan(self.sa) * tl - r2 + self.r21)  # second point arc
        p5 = Point2D(b - ex - r2 + math.sin(self.sa) * r2, -h / 2 + tf - math.tan(self.sa) * (tl - r2))  # end arc
        p6 = Point2D(-ex + tw + r1 - math.sin(self.sa) * r1, -h / 2 + tf + math.tan(self.sa) * (b - tl - tw - r1))  # start arc
        p7 = Point2D(-ex + tw + r1 - self.r11, -h / 2 + tf + math.tan(self.sa) * (b - tl - tw - r1) + r1 - self.r11)  # second point arc
        p8 = Point2D(-ex + tw, -h / 2 + tf + math.tan(self.sa) * (b - tl - tw) + r1)  # end arc
        p9 = Point2D(p8.x, -p8.y)  # start arc
        p10 = Point2D(p7.x, -p7.y)  # second point arc
        p11 = Point2D(p6.x, -p6.y)  # end arc
        p12 = Point2D(p5.x, -p5.y)  # start arc
        p13 = Point2D(p4.x, -p4.y)  # second point arc
        p14 = Point2D(p3.x, -p3.y)  # end arc
        p15 = Point2D(p2.x, -p2.y)  # right top
        p16 = Point2D(p1.x, -p1.y)  # left top

        # describe curves
        l1 = Line2D(p1, p2)
        l2 = Line2D(p2, p3)
        l3 = Arc2D(p3, p4, p5)
        l4 = Line2D(p5, p6)
        l5 = Arc2D(p6, p7, p8)
        l6 = Line2D(p8, p9)
        l7 = Arc2D(p9, p10, p11)
        l8 = Line2D(p11, p12)
        l9 = Arc2D(p12, p13, p14)
        l10 = Line2D(p14, p15)
        l11 = Line2D(p15, p16)
        l12 = Line2D(p16, p1)

        self.curve = PolyCurve2D().by_joined_curves([l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12])

    def __str__(self):
        return "Profile(" + f"{self.name})"


class IShapeParallelFlange:
    def __init__(self, name, h, b, tw, tf, r):
        self.Description = "I Shape profile with parallel flange"
        self.ID = "I_PF"
        # HEA, IPE, HEB, HEM etc.

        # parameters
        self.name = name
        self.h = h  # height
        self.b = b # width
        self.tw = tw  # web thickness
        self.tf = tf  # flange thickness
        self.r = r  # web fillet
        self.r1 = r1 = r / sqrt2

        # describe points
        p1 = Point2D(b / 2, -h / 2)  # right bottom
        p2 = Point2D(b / 2, -h / 2 + tf)
        p3 = Point2D(tw / 2 + r, -h / 2 + tf)  # start arc
        p4 = Point2D(tw / 2 + r - r1, (-h / 2 + tf + r - r1))  # second point arc
        p5 = Point2D(tw / 2, -h / 2 + tf + r)  # end arc
        p6 = Point2D(tw / 2, h / 2 - tf - r)  # start arc
        p7 = Point2D(tw / 2 + r - r1, h / 2 - tf - r + r1)  # second point arc
        p8 = Point2D(tw / 2 + r, h / 2 - tf)  # end arc
        p9 = Point2D(b / 2, h / 2 - tf)
        p10 = Point2D((b / 2), (h / 2))  # right top
        p11 = Point2D(-p10.x, p10.y)  # left top
        p12 = Point2D(-p9.x, p9.y)
        p13 = Point2D(-p8.x, p8.y)  # start arc
        p14 = Point2D(-p7.x, p7.y)  # second point arc
        p15 = Point2D(-p6.x, p6.y)  # end arc
        p16 = Point2D(-p5.x, p5.y)  # start arc
        p17 = Point2D(-p4.x, p4.y)  # second point arc
        p18 = Point2D(-p3.x, p3.y)  # end arc
        p19 = Point2D(-p2.x, p2.y)
        p20 = Point2D(-p1.x, p1.y)

        # describe curves
        l1 = Line2D(p1, p2)
        l2 = Line2D(p2, p3)
        l3 = Arc2D(p3, p4, p5)
        l4 = Line2D(p5, p6)
        l5 = Arc2D(p6, p7, p8)
        l6 = Line2D(p8, p9)
        l7 = Line2D(p9, p10)
        l8 = Line2D(p10, p11)
        l9 = Line2D(p11, p12)
        l10 = Line2D(p12, p13)
        l11 = Arc2D(p13, p14, p15)
        l12 = Line2D(p15, p16)
        l13 = Arc2D(p16, p17, p18)
        l14 = Line2D(p18, p19)
        l15 = Line2D(p19, p20)
        l16 = Line2D(p20, p1)

        self.curve = PolyCurve2D().by_joined_curves([l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12, l13, l14, l15, l16])

        def __str__(self):
            return "Profile(" + f"{self.name})"


class Rectangle:
    def __init__(self, name, b, h):
        self.Description = "Rectangle"
        self.ID = "Rec"

        # parameters
        self.name = name
        self.curve = []
        self.h = h  # height
        self.b = b  # width

        # describe points
        p1 = Point2D(b / 2, -h / 2)  # right bottom
        p2 = Point2D(b / 2, h / 2)  # right top
        p3 = Point2D(-b / 2, h / 2) # left top
        p4 = Point2D(-b / 2, -h / 2) # left bottom

        # describe curves
        l1 = Line2D(p1, p2)
        l2 = Line2D(p2, p3)
        l3 = Line2D(p3, p4)
        l4 = Line2D(p4, p1)

        self.curve = PolyCurve2D().by_joined_curves([l1, l2, l3, l4])

        def __str__(self):
            return "Profile(" + f"{self.name})"


class Round:
    def __init__(self, name, r):
        self.Description = "Round"
        self.ID = "Rnd"

        # parameters
        self.name = name
        self.curve = []
        self.r = r  # radius
        self.data = (name, r, "Round")
        dr = r / sqrt2 #grootste deel

        # describe points
        p1 = Point2D(r, 0)  # right middle
        p2 = Point2D(dr, dr)
        p3 = Point2D(0, r)  # middle top
        p4 = Point2D(-dr, dr)
        p5 = Point2D(-r, 0) # left middle
        p6 = Point2D(-dr, -dr)
        p7 = Point2D(0, -r) # middle bottom
        p8 = Point2D(dr, -dr)

        # describe curves
        l1 = Arc2D(p1, p2, p3)
        l2 = Arc2D(p3, p4, p5)
        l3 = Arc2D(p5, p6, p7)
        l4 = Arc2D(p7, p8, p1)

        self.curve = PolyCurve2D().by_joined_curves([l1, l2, l3, l4])

        def __str__(self):
            return "Profile(" + f"{self.name})"

class Roundtube:
    #ToDo: add inner circle
    def __init__(self, name, d, t):
        self.Description = "Round Tube Profile"
        self.ID = "Tube"

        # parameters
        self.name = name
        self.curve = []
        self.d = d
        self.r = d/2  # radius
        self.t = t  # wall thickness
        self.data = (name, d, t, "Round Tube Profile")
        dr = self.r / sqrt2 #grootste deel
        r = self.r

        # describe points
        p1 = Point2D(r, 0)  # right middle
        p2 = Point2D(dr, dr)
        p3 = Point2D(0, r)  # middle top
        p4 = Point2D(-dr, dr)
        p5 = Point2D(-r, 0) # left middle
        p6 = Point2D(-dr, -dr)
        p7 = Point2D(0, -r) # middle bottom
        p8 = Point2D(dr, -dr)

        # describe curves
        l1 = Arc2D(p1, p2, p3)
        l2 = Arc2D(p3, p4, p5)
        l3 = Arc2D(p5, p6, p7)
        l4 = Arc2D(p7, p8, p1)

        self.curve = PolyCurve2D().by_joined_curves([l1, l2, l3, l4])

        def __str__(self):
            return "Profile(" + f"{self.name})"


class LAngle:
    def __init__(self, name, h, b, tw, tf, r1, r2, ex, ey):
        self.Description = "LAngle"
        self.ID = "L"

        # parameters
        self.name = name
        self.curve = []
        self.b = b  # width
        self.h = h  # height
        self.tw = tw  # wall nominal thickness
        self.tf = tw
        self.r1 = r1  # inner fillet
        self.r11 = r1 / sqrt2
        self.r2 = r2  # outer fillet
        self.r21 = r2 / sqrt2
        self.ex = ex  # from left
        self.ey = ey  # from bottom

        # describe points
        p1 = Point2D(-ex, -ey)  # left bottom
        p2 = Point2D(b - ex, -ey)  # right bottom
        p3 = Point2D(b - ex, -ey + tf - r2)  # start arc
        p4 = Point2D(b - ex - r2 + self.r21, -ey + tf - r2 + self.r21)  # second point arc
        p5 = Point2D(b - ex - r2, -ey + tf)  # end arc
        p6 = Point2D(-ex + tf + r1, -ey + tf)  # start arc
        p7 = Point2D(-ex + tf + r1 - self.r11, -ey + tf + r1 - self.r11)  # second point arc
        p8 = Point2D(-ex + tf, -ey + tf + r1)  # end arc
        p9 = Point2D(-ex + tf, h - ey - r2)  # start arc
        p10 = Point2D(-ex + tf - r2 + self.r21, h - ey - r2 + self.r21)  # second point arc
        p11 = Point2D(-ex + tf - r2, h - ey)  # end arc
        p12 = Point2D(-ex, h - ey)  # left top

        # describe curves
        l1 = Line2D(p1, p2)
        l2 = Line2D(p2, p3)
        l3 = Arc2D(p3, p4, p5)
        l4 = Line2D(p5, p6)
        l5 = Arc2D(p6, p7, p8)
        l6 = Line2D(p8, p9)
        l7 = Arc2D(p9, p10, p11)
        l8 = Line2D(p11, p12)
        l9 = Line2D(p12, p1)

        self.curve = PolyCurve2D().by_joined_curves([l1, l2, l3, l4, l5, l6, l7, l8, l9])

        def __str__(self):
            return "Profile(" + f"{self.name})"

class TProfile:
    #ToDo: inner outer fillets in polycurve
    def __init__(self, name, h, b, tw, tf, r, r1, r2, ex, ey):
        self.Description = "TProfile"
        self.ID = "T"

        # parameters
        self.name = name
        self.curve = []
        self.b = b  # width
        self.h = h  # height
        self.tw = tw  # wall nominal thickness
        self.tf = tw
        self.r = r  # inner fillet
        self.r01 = r/sqrt2
        self.r1 = r1  # outer fillet flange
        self.r11 = r1 / sqrt2
        self.r2 = r2  # outer fillet top web
        self.r21 = r2 / sqrt2
        self.ex = ex  # from left
        self.ey = ey  # from bottom

        # describe points
        p1 = Point2D(-ex, -ey)  # left bottom
        p2 = Point2D(b - ex, -ey)  # right bottom
        p3 = Point2D(b - ex, -ey + tf - r1)  # start arc
        p4 = Point2D(b - ex - r1 + self.r11, -ey + tf - r1 + self.r11)  # second point arc
        p5 = Point2D(b - ex - r1, -ey + tf)  # end arc
        p6 = Point2D(0.5 * tw + r, -ey + tf)  # start arc
        p7 = Point2D(0.5 * tw + r - self.r01, -ey + tf + r - self.r01)  # second point arc
        p8 = Point2D(0.5 * tw, -ey + tf + r)  # end arc
        p9 = Point2D(0.5 * tw, -ey + h - r2)  # start arc
        p10 = Point2D(0.5 * tw - self.r21, -ey + h - r2 + self.r21) # second point arc
        p11 = Point2D(0.5 * tw - r2, -ey + h)  # end arc

        p12 = Point2D(-p11.x,p11.y)
        p13 = Point2D(-p10.x, p10.y)
        p14 = Point2D(-p9.x, p9.y)
        p15 = Point2D(-p8.x, p8.y)
        p16 = Point2D(-p7.x, p7.y)
        p17 = Point2D(-p6.x, p6.y)
        p18 = Point2D(-p5.x, p5.y)
        p19 = Point2D(-p4.x, p4.y)
        p20 = Point2D(-p3.x, p3.y)

        # describe curves
        l1 = Line2D(p1, p2)

        l2 = Line2D(p2, p3)
        l3 = Arc2D(p3, p4, p5)
        l4 = Line2D(p5, p6)
        l5 = Arc2D(p6, p7, p8)
        l6 = Line2D(p8, p9)
        l7 = Arc2D(p9, p10, p11)
        l8 = Line2D(p11, p12)

        l9 = Arc2D(p12, p13, p14)
        l10 = Line2D(p14, p15)
        l11 = Arc2D(p15, p16, p17)
        l12 = Line2D(p17, p18)
        l13 = Arc2D(p18, p19, p20)
        l14 = Line2D(p20, p1)

        self.curve = PolyCurve2D().by_joined_curves([l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12, l13, l14])

        def __str__(self):
            return "Profile(" + f"{self.name})"


class RectangleHollowSection:  #NOT COMPLETE YET
    def __init__(self, name, h, b, t, r1, r2):
        self.Description = "Rectangle Hollow Section"
        self.ID = "RHS"

        # parameters
        self.name = name
        self.curve = []
        self.h = h  # height
        self.b = b  # width
        self.t = t # thickness
        self.r1 = r1 # outer radius
        self.r2 = r2 # inner radius
        dr = r1 - r1 / sqrt2

        # describe points
        p1 = Point2D(-b / 2 + r1, - h / 2)  #left bottom end arc
        p2 = Point2D(b / 2 - r1, - h / 2)  #right bottom start arc
        p3 = Point2D(b / 2 - dr, - h / 2 + dr) #right bottom mid arc
        p4 = Point2D(b / 2, - h / 2 + r1) #right bottom end arc
        p5 = Point2D(p4.x, -p4.y) #right start arc
        p6 = Point2D(p3.x, -p3.y) #right mid arc
        p7 = Point2D(p2.x, -p2.y) #right end arc
        p8 = Point2D(-p7.x, p7.y) #left start arc
        p9 = Point2D(-p6.x, p6.y)  #left mid arc
        p10 = Point2D(-p5.x, p5.y)  #left end arc
        p11 = Point2D(p10.x, -p10.y) #right bottom start arc
        p12 = Point2D(p9.x, -p9.y) #right bottom mid arc

        # describe curves
        l1 = Line2D(p1, p2)
        l2 = Arc2D(p2,p3,p4)
        l3 = Line2D(p4,p5)
        l4 = Arc2D(p5,p6,p7)
        l5 = Line2D(p7,p8)
        l6 = Arc2D(p8, p9, p10)
        l7 = Line2D(p10, p11)
        l8 = Arc2D(p11, p12, p1)

        self.curve = PolyCurve2D().by_joined_curves([l1, l2, l3, l4, l5, l6, l7, l8])

        def __str__(self):
            return "Profile(" + f"{self.name})"


jsonFile = "https://raw.githubusercontent.com/3BMLabs/building.py/main/library/profile_database/steelprofile.json"
url = urllib.request.urlopen(jsonFile)
data = json.loads(url.read())


class searchProfile:
    def __init__(self, name):
        self.name = name
        self.shape_coords = None
        self.shape_name = None
        self.synonyms = None
        for item in data:
            for i in item.values():
                synonymList = i[0]["synonyms"]
                #if self.name in synonymList:
                #bools = [self.name.lower() in e for e in [synonym.lower() for synonym in synonymList]]
                #if True in bools:
                if self.name.lower() in [synonym.lower() for synonym in synonymList]:
                    self.shape_coords = i[0]["shape_coords"]
                    self.shape_name = i[0]["shape_name"]
                    self.synonyms = i[0]["synonyms"]


class profiledataToShape:
    def __init__(self, name1):
        from geometry.curve import PolyCurve
        profile_data = searchProfile(name1)
        shape_name = profile_data.shape_name
        self.shape_name = shape_name
        name = profile_data.name
        self.d1 = profile_data.shape_coords
        #self.d1.insert(0,name)
        d1 = self.d1
        if shape_name == "C-channel parallel flange":
            prof = CChannelParallelFlange(name,d1[0],d1[1],d1[2],d1[3],d1[4],d1[5])
        elif shape_name == "C-channel sloped flange":
            prof = CChannelSlopedFlange(name,d1[0],d1[1],d1[2],d1[3],d1[4],d1[5],d1[6],d1[7],d1[8])
        elif shape_name == "I-shape parallel flange":
            prof = IShapeParallelFlange(name,d1[0],d1[1],d1[2],d1[3],d1[4])
        elif shape_name == "I-shape sloped flange":
            prof = IShapeParallelFlange(name, d1[0], d1[1], d1[2], d1[3], d1[4])
            #Todo: add sloped flange shape
        elif shape_name == "Rectangle":
            prof = Rectangle(name,d1[0], d1[1])
        elif shape_name == "Round":
            prof = Round(name, d1[1])
        elif shape_name == "Round tube profile":
            prof = Roundtube(name, d1[0], d1[1])
        elif shape_name == "LAngle":
            prof = LAngle(name,d1[0],d1[1],d1[2],d1[3],d1[4],d1[5],d1[6],d1[7])
        elif shape_name == "TProfile":
            prof = TProfile(name, d1[0], d1[1], d1[2], d1[3], d1[4], d1[5], d1[6], d1[7], d1[8])
        elif shape_name == "Rectangle Hollow Section":
            prof = RectangleHollowSection(name,d1[0],d1[1],d1[2],d1[3],d1[4])
        else:
            prof = "error, profile not created"
        self.prof = prof
        self.data = d1
        pc2d = self.prof.curve  # 2D polycurve
        pc3d = PolyCurve.by_polycurve_2D(pc2d)
        pcsegment = PolyCurve.segment(pc3d, 10)
        pc2d2 = pcsegment.to_polycurve_2D()
        self.polycurve2d = pc2d2

def justifictionToVector(plycrv2D: PolyCurve2D, XJustifiction, Yjustification):
    xval = []
    yval = []
    for i in plycrv2D.curves:
        xval.append(i.start.x)
        yval.append(i.start.y)

    #Boundingbox2D
    xmin = min(xval)
    xmax = max(xval)
    ymin = min(yval)
    ymax = max(yval)
    b = xmax-xmin
    h = ymax-ymin

    dxleft = -xmax
    dxright = -xmin
    dxcenter = dxleft - 0.5 * b #CHECK
    dxorigin = 0

    dytop = -ymax
    dybottom = -ymin
    dycenter = dytop - 0.5 * h #CHECK
    dyorigin = 0

    if XJustifiction == "center":
        dx = 0 #TODO
    elif XJustifiction == "left":
        dx = dxleft
    elif XJustifiction == "right":
        dx = dxright
    elif XJustifiction == "origin":
        dx = 0 #TODO
    else:
        dx = 0

    if Yjustification == "center":
        dy = 0   #TODO
    elif Yjustification == "top":
        dy = dytop
    elif Yjustification == "bottom":
        dy = dybottom
    elif Yjustification == "origin":
        dy = 0 #TODO
    else:
        dy = 0

    v1 = Vector2(dx, dy)

    return v1

test2 = searchProfile("HEA200")
print("test")
print(test2)