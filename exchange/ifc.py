import sys, os
from pathlib import Path

import ifcopenshell.geom
import ifcopenshell.api
import ifcopenshell.util.element as util
import ifcopenshell.util.shape as shape

sys.path.append(str(Path(__file__).resolve().parents[2]))

from exchange.speckle import *
from geometry.curve import *
from geometry.solid import *
from project.fileformat import BuildingPy
from objects.level import Level
from objects.wall import Wall
from objects.door import Door
from objects.room import Room
from geometry.surface import Surface


class LoadIFC:
    def __init__(self, filename=str, project=project, filter=None):
        self.filename = filename
        self.project = project
        self.root = self.load()
        self.IFCObjects = self.getobject(filter)
        self.convertedObjects = self.convertobject()
        self.sendToSpeckle()

    def load(self):
        model = ifcopenshell.open(self.filename)
        return model
    
    def getobject(self, data):
        if data != None:
            if type(data) != list:
                data = [data]
        else:
            return None
        
        fetched_objects = []
        for each in data:
            objs = self.root.by_type(each)
            fetched_objects.append(objs)
        return fetched_objects


    def get_storey_height_by_name(ifc_file_path, storey_name):
        ifc_file = ifcopenshell.open(ifc_file_path)
        building_storeys = ifc_file.by_type('IfcBuildingStorey')
        storey_height = None

        for storey in building_storeys:
            if storey.Name == storey_name:
                for definition in storey.IsDefinedBy:
                    if definition.is_a('IfcRelDefinesByProperties'):
                        property_set = definition.RelatingPropertyDefinition
                        if property_set.is_a('IfcPropertySet'):
                            for property in property_set.HasProperties:
                                if property.Name in ["StoreyHeight", "Height"]:
                                    if property.is_a('IfcPropertySingleValue'):
                                        storey_height = property.NominalValue.wrappedValue
                                        break
                if storey_height is not None:
                    break
        
        return storey_height



    def convertobject(self):
        objs = []
        # settings = ifcopenshell.geom.settings()
        settings = ifcopenshell.geom.settings()
        settings.set(settings.SEW_SHELLS, True)  # Attempt to sew shells into solids

        for index, eachlist in enumerate(self.IFCObjects):
            for object in eachlist:
                if object.is_a('IfcBuildingStorey'):
                    object
                    storey_height = None
                    for relDefines in object.IsDefinedBy:
                        if relDefines.is_a('IfcRelDefinesByProperties'):
                            property_set = relDefines.RelatingPropertyDefinition
                            if property_set.is_a('IfcPropertySet'):
                                for prop in property_set.HasProperties:
                                    if prop.Name in ["Height", "StoreyHeight", "Elevation"]:
                                        if prop.is_a('IfcPropertySingleValue'):
                                            storey_height = prop.NominalValue.wrappedValue
                                            break
                                if storey_height is not None:
                                    break
                    j = Level.by_point(Point(0,0,storey_height), "temp")
                    objs.append(j)


                elif object.is_a('IfcSpace'):
                    points_list = []
                    z_values = []

                    min_z_points = []
                    max_z_points = []

                    min_z = float("inf")
                    max_z = float("inf")

                    data = elementName = util.get_psets(object)
                    elementName = util.get_psets(object)["Pset_ProductRequirements"]["Name"]

                    bottom_elevation = None
                    a = object.get_info()
                    print(a["Name"])
                    print(a["ObjectPlacement"])
                    b = object.id
                    c = object.is_a()

                    shape = ifcopenshell.geom.create_shape(settings, object)
                    print(shape)
                    mesh = shape.geometry
                    print(mesh)
                    vertices = mesh.verts
                    print(vertices)
                    for i in range(0, len(vertices), 3):
                        point = Point(vertices[i] * project.scale, vertices[i+1] * project.scale, vertices[i+2] * project.scale)
                        points_list.append(point)

                        if point.z < min_z:
                            min_z = point.z
                            min_z_points = [point]
                        elif point.z == min_z:
                            min_z_points.append(point)

                        if point.z > max_z:
                            max_z = point.z
                            max_z_points = [point]
                        elif point.z == max_z:
                            max_z_points.append(point)

                    for pt in points_list:
                        z_values.append(pt.z)
                    top = max(z_values)
                    bottom = min(z_values)

                    print(top, bottom)

                    ex = Extrusion.by_polycurve_height(PolyCurve.by_points(min_z_points), top, bottom)
                    ex.name = elementName
                    objs.append(ex)
                    objs.append(ex.polycurve_3d_translated)


                elif object.is_a('IfcWall') or object.is_a('IfcDoor'):
                    shape = ifcopenshell.geom.create_shape(settings, object)
                    verts = shape.geometry.verts
                    edges = shape.geometry.edges
                    faces = shape.geometry.faces

                    # 2_door.ifc -> object.Representation.Representations[1].ContextOfItems.RepresentationsInContext[0]
                    

                    # grouped_verts = ifcopenshell.util.shape.get_vertices(shape.geometry)
                    # # A nested numpy array e.g. [[e1v1, e1v2], [e2v1, e2v2], ...]
                    # grouped_edges = ifcopenshell.util.shape.get_edges(shape.geometry)
                    # # A nested numpy array e.g. [[f1v1, f1v2, f1v3], [f2v1, f2v2, f2v3], ...]
                    # grouped_faces = ifcopenshell.util.shape.get_faces(shape.geometry)

                    # print(shape)

                    # print(grouped_faces[0])
                    # print(grouped_faces[1])

                    # print(shape)
                    # x = object.get_geometry()
                    # print(x)
                    # object
                    # a = object.Representation.Representations[1].Items[0].MappingSource.MappedRepresentation.Items[0].Elements
                    # c = object.Representation.Representations[1]
                    # print(a)
                    # print(c)
                    # for obj in a:
                    #     if obj.is_a("IfcPolyline"):
                    #         pts = []
                    #         for pt in obj.Points:
                    #             pts.append(Point2D(pt.Coordinates[0], pt.Coordinates[1]))
                    #             # print(pt.Coordinates)
                    #         pc = PolyCurve2D.by_points(pts)
                    #         objs.append(pc)

                    # b = 
                    # for obj in b:


                        # print()
                        # print(obj)
                    # print(a)


                    # def process_geometric_representation_item(item):
                    #     vertices = []
                    #     if item.is_a('IfcExtrudedAreaSolid'):
                    #         # Extract the 2D profile points
                    #         profile = item.SweptArea
                    #         if profile.is_a('IfcArbitraryClosedProfileDef'):
                    #             outer_curve = profile.OuterCurve
                    #             if outer_curve.is_a('IfcPolyline'):
                    #                 for point in outer_curve.Points:
                    #                     vertices.append(point.Coordinates)

                    #         direction = item.ExtrudedDirection.DirectionRatios
                    #         depth = item.Depth

                    #         extruded_vertices = []
                    #         for vert in vertices:
                    #             extruded_vert = [vert[0] + direction[0] * depth, vert[1] + direction[1] * depth, direction[2] * depth]
                    #             extruded_vertices.append(extruded_vert)

                    #         vertices += extruded_vertices


                    #     elif item.is_a('IfcFacetedBrep'):
                    #         for face in item.Outer.CfsFaces:
                    #             for loop in face.Bounds:
                    #                 for point in loop.PolyLoop.Polygon:
                    #                     coordinates = point.Coordinates
                    #                     vertices.append(coordinates)
                    #     return vertices


                    # def extract_wall_geometry(ifc_wall):
                    #     vertices = []
                    #     materials = []

                    #     representation = ifc_wall.Representation

                    #     for rep in representation.Representations:
                    #         if rep.RepresentationType == 'SolidModel' or rep.RepresentationType == 'SurfaceModel' or rep.RepresentationType == 'SweptSolid':
                    #             for item in rep.Items:
                    #                 print(item)
                    #                 vertices.extend(process_geometric_representation_item(item))
                                    
                    #     return vertices

                #temp
                            
                    # vertices = extract_wall_geometry(object)
                    # print(vertices)

                    # settings = ifcopenshell.geom.settings()
                    # shape = ifcopenshell.geom.create_shape(settings, object)
                    # faces = shape.geometry.faces
                    # verts = shape.geometry.verts
                    # materials = shape.geometry.materials
                    # material_ids = shape.geometry.material_ids

                    grouped_verts = [[verts[i], verts[i + 1], verts[i + 2]] for i in range(0, len(verts), 3)]
                    grouped_verts_scaled = [Point(verts[i]*project.scale, verts[i + 1]*project.scale, verts[i + 2]*project.scale) for i in range(0, len(verts), 3)]

                    grouped_faces = [[faces[i], faces[i + 1], faces[i + 2]] for i in range(0, len(faces), 3)]

                    for g_faces in grouped_faces:
                        pts = []
                        for index in g_faces:
                            pts.append(grouped_verts_scaled[index])
                        pc = PolyCurve.by_points(pts)
                        objs.append(pc)
                        objs.append(Extrusion.by_polycurve_height(pc, 0, 0))

                    # sys.exit()
                    # points = []
                    # pcurves = []
                    # for pt in grouped_verts:
                    #     p1 = Point(pt[0]*project.scale, pt[1]*project.scale, pt[2]*project.scale)
                    #     points.append(p1)
                    # return points
                

                #temp
                    # points_list = []
                    # z_values = []

                    # min_z_points = []
                    # max_z_points = []

                    # min_z = float("inf")
                    # max_z = float("inf")

                    # shape = ifcopenshell.geom.create_shape(settings, object)
                    # mesh = shape.geometry
                    # edges = shape.geometry.edges
                    # verticesX = shape.geometry.verts
                    # faces = shape.geometry.faces
                    # vertices = mesh.verts

                    # for i in range(0, len(vertices), 3):
                    #     point = Point(vertices[i] * project.scale, vertices[i+1] * project.scale, vertices[i+2] * project.scale)
                    #     points_list.append(point)
                    #     print(point)
                    #     if point.z < min_z:
                    #         min_z = point.z
                    #         min_z_points = [point]
                    #     elif point.z == min_z:
                    #         min_z_points.append(point)

                    #     if point.z > max_z:
                    #         max_z = point.z
                    #         max_z_points = [point]
                    #     elif point.z == max_z:
                    #         max_z_points.append(point)

                    # for pt in points_list:
                    #     z_values.append(pt.z)
                    # top = max(z_values)
                    # bottom = min(z_values)

                    # wall = Wall.by_mesh(verticesX, faces)
                    # # ex = Extrusion.by_polycurve_height(PolyCurve.by_points(min_z_points), top, 0)
                    # # objs.append(ex)
                    # objs.append(wall)



                    # points_list = []
                    # for i in range(0, len(vertices), 3):
                    #     point = Point(vertices[i] * project.scale, vertices[i+1] * project.scale, vertices[i+2] * project.scale)
                    #     points_list.append(point)

                        # if point.z < min_z:
                        #     min_z = point.z
                        #     min_z_points = [point]
                        # elif point.z == min_z:
                        #     min_z_points.append(point)

                        # if point.z > max_z:
                        #     max_z = point.z
                        #     max_z_points = [point]
                        # elif point.z == max_z:
                        #     max_z_points.append(point)

                    # print(points_list)
                    # for point_list in points_list:
                    # pc = PolyCurve.by_points(points_list)
                    # objs.append(pc)
                    # representation = object.Representation
                    # for rep in representation.Representations:
                    #     if rep.RepresentationType == 'SweptSolid':
                    #         solid = rep.Items[0]
                    #         print(solid)
                            # if hasattr(solid, 'SweptArea') and solid.SweptArea.ProfileType == 'AREA':
                            #     for profile in solid.SweptArea.Profiles:
                            #         if hasattr(profile, 'Width'):
                            #             details['thickness'] = profile.Width
                            # extrusion = solid.ExtrudedDirection
                            # if extrusion.DirectionRatios:
                            #     details['height'] = solid.Depth
                    
                    # for representation in object.Representation.Representations:
                    #     if representation.RepresentationIdentifier == "Axis":
                    #         if hasattr(representation.Items[0], 'Points'):
                    #             points = representation.Items[0].Points
                    #             if len(points) >= 2:
                    #                 # Start and end coordinates (simplified, actual extraction may vary)
                    #                 details['start_coordinate'] = (points[0].Coordinates[0], points[0].Coordinates[1], points[0].Coordinates[2])
                    #                 details['end_coordinate'] = (points[-1].Coordinates[0], points[-1].Coordinates[1], points[-1].Coordinates[2])
                    # print(details)
                    # objs.append(details)
                    # except:
                    #     pass

        return objs

                # shape = ifcopenshell.geom.create_shape(settings, object)
                # pass
                # parm = util.get_type(object)
                # parm = util.get_pset(object)
                # parm = util.get_layers(self.root, object)
                # parm = util.get_layer
                # parm = shape.id
                # parm = shape.geometry.id
                # print(parm)

                # verts = shape.geometry.verts
                # print(verts)
                
                # python split list in 3 parts

                # edges = shape.geometry.edges
                # print(edges)

                # faces = shape.geometry.faces
                # print(faces)
    
    def sendToSpeckle(self):
        for obj in flatten(self.convertedObjects):
            self.project.objects.append(obj)


def translateObjectsToIFC(Obj):
    FreeCADObj = []
    for i in Obj:
        nm = i.__class__.__name__
        if nm == 'Panel':
            test = "test"

        elif nm == 'Surface' or nm == 'Face':
            test = "test"

        elif nm == 'Frame':
            #convert this to a .ifc object
            # FreeCADObj.append(FrameToFreeCAD(i))
            pass

        elif nm == "Extrusion":
            test = "test"

        elif nm == 'PolyCurve':
            test = "test"

        elif nm == 'BoundingBox2d':
            test = "test"

        elif nm == 'ImagePyB':
            test = "test"

        elif nm == 'Interval':
            test = "test"

        elif nm == 'Line':
            test = "test"

        elif nm == 'Plane':
            test = "test"

        elif nm == 'Arc':
            test = "test"

        elif nm == 'Line2D':
            test = "test"

        elif nm == 'Point':
            test = "test"

        elif nm == 'Point2D':
            test = "test"

        elif nm == 'Grid':
            test = "test"

        elif nm == 'GridSystem':
            test = "test"

        else:
            print(f"{nm} Object not yet added to translateFreeCADObj")

    return FreeCADObj