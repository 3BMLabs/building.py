import sys, os
from pathlib import Path
import numpy as np
import ifcopenshell.geom
import ifcopenshell.api
import ifcopenshell.util.element as util
import ifcopenshell.util.shape as shape
from ifcopenshell.api import run

sys.path.append(str(Path(__file__).resolve().parents[2]))

from geometry.curve import *
from geometry.solid import *
from project.fileformat import BuildingPy
from objects.level import Level
from objects.wall import Wall
from objects.door import Door
from objects.room import Room
from geometry.surface import Surface
from abstract.matrix import *


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
        settings = ifcopenshell.geom.settings()
        settings.set(settings.SEW_SHELLS, True)

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

        return objs


class CreateIFC:
    def __init__(self):
        self.model = ifcopenshell.file()

    def add_project(self, name):
        self.project = self.model.createIfcProject(
            GlobalId=ifcopenshell.guid.new(), 
            OwnerHistory=None, 
            Name=name, 
            Description=None, 
            ObjectType=None, 
            LongName=None, 
            Phase=None, 
            RepresentationContexts=[], 
            UnitsInContext=None
        )

        run("unit.assign_unit", self.model)
        self.context = run("context.add_context", self.model, context_type="Model")
        self.body = run("context.add_context", self.model, context_type="Model",
            context_identifier="Body", target_view="MODEL_VIEW", parent=self.context)
        

    def add_site(self, name):
        self.site = self.model.createIfcSite(
            GlobalId=ifcopenshell.guid.new(), 
            OwnerHistory=None, 
            Name=name, 
            Description=None, 
            ObjectType=None, 
            ObjectPlacement=None, 
            Representation=None, 
            LongName=None, 
            CompositionType=None, 
            RefLatitude=None, 
            RefLongitude=None, 
            RefElevation=None, 
            LandTitleNumber=None, 
            SiteAddress=None
        )
        self.model.createIfcRelAggregates(
            GlobalId=ifcopenshell.guid.new(), 
            OwnerHistory=None, 
            Name=None, 
            Description=None, 
            RelatingObject=self.project, 
            RelatedObjects=[self.site]
        )

    def add_building(self, name):
        self.building = self.model.createIfcBuilding(
            GlobalId=ifcopenshell.guid.new(), 
            OwnerHistory=None, 
            Name=name, 
            Description=None, 
            ObjectType=None, 
            ObjectPlacement=None, 
            Representation=None, 
            LongName=None, 
            CompositionType=None, 
            ElevationOfRefHeight=None, 
            ElevationOfTerrain=None, 
            BuildingAddress=None
        )
        self.model.createIfcRelAggregates(
            GlobalId=ifcopenshell.guid.new(), 
            OwnerHistory=None, 
            Name=None, 
            Description=None, 
            RelatingObject=self.site, 
            RelatedObjects=[self.building]
        )

    def add_storey(self, name):
        self.storey = self.model.createIfcBuildingStorey(
            GlobalId=ifcopenshell.guid.new(), 
            OwnerHistory=None, 
            Name=name, 
            Description=None, 
            ObjectType=None, 
            ObjectPlacement=None, 
            Representation=None, 
            LongName=None, 
            CompositionType=None, 
            Elevation=None
        )
        self.model.createIfcRelAggregates(
            GlobalId=ifcopenshell.guid.new(), 
            OwnerHistory=None, 
            Name=None, 
            Description=None, 
            RelatingObject=self.building, 
            RelatedObjects=[self.storey]
        )


    def export(self, filename):
        # Export the IFC model to a file with the specified name
        self.model.write(filename)
        print(f"IFC created: {filename}")



def translateObjectsToIFC(objects, ifc_creator):
    IFCObj = []


    def create_ifc_polyline(points, ifc_creator):
        ifc_points = [ifc_creator.model.create_entity('IfcCartesianPoint', Coordinates=(p.x, p.y, 0)) for p in points]
        polyline = ifc_creator.model.create_entity('IfcPolyline', Points=ifc_points)
        return polyline

    # Elements
    # Andere category meegeven.
    # boundingbox van element bepalen.
    if not isinstance(objects, list):
        objects = [objects]

    for object_type in flatten(objects):
        nm = object_type.__class__.__name__
        if nm == 'Panel':
            test = "test"

        elif nm == 'Surface' or nm == 'Face':

            surface_type = run("root.create_entity", ifc_creator.model, ifc_class="IfcColumnType", name="")

            matrix = np.eye(4)

            material_set = run("material.add_material_set", ifc_creator.model, name="", set_type="IfcMaterialProfileSet")

            material = run("material.add_material", ifc_creator.model, name="", category="")


            interne_punten = []
            if object_type.inner_Polygon != None:
                for polycurve in object_type.inner_Polygon:
                    interne = []
                    for pt in polycurve.points:
                        interne.append((pt.x, pt.y))
                    interne_punten.append(interne)


            externe_punten = []
            for pt in object_type.outer_Polygon.points:
                externe_punten.append((pt.x, pt.y))


            externe_ifc_punten = [ifc_creator.model.create_entity('IfcCartesianPoint', Coordinates=p) for p in externe_punten]
            externe_polyline = ifc_creator.model.create_entity('IfcPolyline', Points=externe_ifc_punten)

            interne_polyline_lists = []
            for interne in interne_punten:
                interne_ifc_punten = [ifc_creator.model.create_entity('IfcCartesianPoint', Coordinates=p) for p in interne]
                interne_polyline = ifc_creator.model.create_entity('IfcPolyline', Points=interne_ifc_punten)
                interne_polyline_lists.append(interne_polyline)


            custom_profile_with_void = ifc_creator.model.create_entity(
                'IfcArbitraryProfileDefWithVoids',
                ProfileType='AREA',
                ProfileName= object_type.name,
                OuterCurve=externe_polyline,
                InnerCurves=interne_polyline_lists
            )

            run("material.add_profile", ifc_creator.model, profile_set=material_set, material=material, profile=custom_profile_with_void)

            run("material.assign_material", ifc_creator.model, product=surface_type, material=material_set)

            object = run("root.create_entity", ifc_creator.model, ifc_class="IfcBuildingElementProxy")

            run("geometry.edit_object_placement", ifc_creator.model, product=object, matrix=matrix, is_si=True)

            run("type.assign_type", ifc_creator.model, related_object=object, relating_type=surface_type)

            representation = run("geometry.add_profile_representation", ifc_creator.model, context=ifc_creator.body, profile=custom_profile_with_void, depth=0)

            run("geometry.assign_representation", ifc_creator.model, product=object, representation=representation)

            run("spatial.assign_container", ifc_creator.model, relating_structure=ifc_creator.storey, product=object)
            
        elif nm == 'Frame':

            start = Point.to_matrix(object_type.start)
            end = Point.to_matrix(object_type.end)
            distance = Point.distance(Point.from_matrix(start), Point.from_matrix(end))

            ifc_class_type = "IfcBeamType"
            ifc_class = "IfcBeam"
            column_type = run("root.create_entity", ifc_creator.model, ifc_class=ifc_class_type, name=object_type.name)
            material_set = run("material.add_material_set", ifc_creator.model, name=object_type.name, set_type="IfcMaterialProfileSet")
            material_name = run("material.add_material", ifc_creator.model, name="", category="steel")
            matrix = Matrix.from_points(object_type.start, object_type.end).matrix
            externe_punten = []
            for pt in object_type.curve.points2D:
                externe_punten.append((pt.x*1000, pt.y*1000))

            externe_ifc_punten = [ifc_creator.model.create_entity('IfcCartesianPoint', Coordinates=p) for p in externe_punten]
            polyline = ifc_creator.model.create_entity('IfcPolyline', Points=externe_ifc_punten)

            shape_profile = ifc_creator.model.create_entity("IfcArbitraryClosedProfileDef", 
                                                            ProfileType="AREA", 
                                                            OuterCurve=polyline)

            run("material.add_profile", ifc_creator.model, profile_set=material_set, material=material_name, profile=shape_profile)
            run("material.assign_material", ifc_creator.model, product=column_type, material=material_set)
            column = run("root.create_entity", ifc_creator.model, ifc_class=ifc_class)
            run("geometry.edit_object_placement", ifc_creator.model, product=column, matrix=matrix, is_si=True)
            run("type.assign_type", ifc_creator.model, related_object=column, relating_type=column_type)
            representation = run("geometry.add_profile_representation", ifc_creator.model, context=ifc_creator.body, profile=shape_profile, depth=distance)
            run("geometry.assign_representation", ifc_creator.model, product=column, representation=representation)
            run("spatial.assign_container", ifc_creator.model, relating_structure=ifc_creator.storey, product=column)


        elif nm == "Extrusion":
            test = "test"

        elif nm == 'PolyCurve' or nm == 'Polygon':
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

        elif nm == 'Grid': #zijn nog niet zichtbaar, maar zijn wel aanwezig
            point_a = (object_type.start.x, object_type.start.y, object_type.start.z)
            point_b = (object_type.end.x, object_type.end.y, object_type.end.z)
            grid_name = object_type.name

            ifc_point_a = ifc_creator.model.createIfcCartesianPoint(point_a)
            ifc_point_b = ifc_creator.model.createIfcCartesianPoint(point_b)
            grid_line = ifc_creator.model.createIfcPolyline([ifc_point_a, ifc_point_b])
            grid_axis = ifc_creator.model.createIfcGridAxis(grid_name, grid_line, True)

            grid_axes_u = [grid_axis]
            grid_axes_v = []
            grid_axes_w = []

            grid = ifc_creator.model.createIfcGrid(
                GlobalId=ifcopenshell.guid.new(),
                OwnerHistory=None,
                UAxes=grid_axes_u,
                VAxes=grid_axes_v,
                WAxes=grid_axes_w,
                ObjectPlacement=None,
                Representation=None
            )

            ifc_creator.model.createIfcRelContainedInSpatialStructure(
                GlobalId=ifcopenshell.guid.new(),
                OwnerHistory=None,
                Name=f"{grid_name} Placement",
                Description=None,
                RelatedElements=[grid],
                RelatingStructure=ifc_creator.storey
            )

        elif nm == 'GridSystem':
            test = "test"

        else:
            print(f"{nm} Object not yet added to translateObjectsToIFC")

    return IFCObj