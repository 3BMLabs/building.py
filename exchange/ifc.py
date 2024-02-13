import sys, os
from pathlib import Path

# import ifcopenshell
from ifcopenshell import *
import ifcopenshell.geom
import ifcopenshell.api
import ifcopenshell.util.element as util
import ifcopenshell.util.shape as shape

import time

sys.path.append(str(Path(__file__).resolve().parents[2]))

from exchange.speckle import *
from geometry.curve import *
from geometry.solid import *
from project.fileformat import BuildingPy


# CREATE PROJECT FILE & LIBRARY
# class CreateIfcProject:
#     def __init__(self, project_name, library_name,organisation_name,person_name):
#         ifcopenshell.api.pre_listeners = {}
#         ifcopenshell.api.post_listeners = {}

#         self.file = ifcopenshell.api.run("project.create_file")
#         self.project = ifcopenshell.api.run("root.create_entity", self.file, ifc_class="IfcProject", name= project_name)
#         self.library = ifcopenshell.api.run("root.create_entity", self.file, ifc_class="IfcProjectLibrary",name=library_name)
#         library = ifcopenshell.api.run("project.assign_declaration", self.file, definition=self.library,relating_context=self.project)
#         units = ifcopenshell.api.run("unit.assign_unit", self.file,length={"is_metric": True, "raw": "MILLIMETERS"})

#         # ORGANISATION DETAILS
#         organisation = self.file.createIfcOrganization()
#         organisation.Name = organisation_name
#         person = self.file.createIfcPerson()
#         person.FamilyName = person_name

#         # APPLICATION
#         app = self.file.createIfcApplication()
#         app.ApplicationDeveloper = organisation
#         app.Version = "0.7"
#         app.ApplicationFullName = "IfcOpenShell v0.7.0-1b1fd1e6"

#         # OWNER HISTORY
#         self.owner_history = self.file.createIfcOwnerHistory()
#         self.owner_history.OwningUser = person
#         self.owner_history.OwningApplication = app
#         self.owner_history.ChangeAction = "NOCHANGE"
#         self.owner_history.CreationDate = int(time.time())

#         # CREATE THE SITE
#         site_placement = self.create_ifclocalplacement()

#         # CREATE THE BUILDING
#         building_placement = self.create_ifclocalplacement(O, Z, X, site_placement)
#         # building = self.file.createIfcBuilding(create_guid(), self.owner_history, 'Bouwwerk', None, None,building_placement, None, None, "ELEMENT", None, None, None)

#         self.site = ifcopenshell.api.run("root.create_entity", self.file, ifc_class="IfcSite", name="Site")
#         self.building = ifcopenshell.api.run("root.create_entity", self.file, ifc_class="IfcBuilding", name=project_name)

#         # Since the site is our top level location, assign it to the project
#         # Then place our building on the site, and our storey in the building
#         ifcopenshell.api.run("aggregate.assign_object", self.file, relating_object=self.project, product=self.site)
#         ifcopenshell.api.run("aggregate.assign_object", self.file, relating_object=self.site, product=self.building)

#         # CREATE BUILDING STOREYS
#         self.storey_placement = self.create_ifclocalplacement(O, Z, X, relative_to=building_placement)
#         storeys_obj = self.create_building_storeys(building_storeys_lst)
#         storey = storeys_obj[2]
#         # storey = ifcopenshell.api.run("root.create_entity", self.file, ifc_class="IfcBuildingStorey", name="peil=0")
#         ifcopenshell.api.run("aggregate.assign_object", self.file, relating_object=self.building, product=storey)

#     def create_ifcaxis2placement(self, point=O, dir1=Z, dir2=X):
#         point = self.file.createIfcCartesianPoint(point)
#         dir1 = self.file.createIfcDirection(dir1)
#         dir2 = self.file.createIfcDirection(dir2)
#         axis2placement = self.file.createIfcAxis2Placement3D(point, dir1, dir2)
#         return axis2placement

#     def create_ifclocalplacement(self, point=O, dir1=Z, dir2=X, relative_to=None):
#         axis2placement = self.create_ifcaxis2placement(point, dir1, dir2)
#         ifclocalplacement = self.file.createIfcLocalPlacement(relative_to, axis2placement)
#         return ifclocalplacement

#     def create_building_storeys(self, building_storeys):
#         building_storeys_obj = []
#         for i in building_storeys:
#             name = i[0]
#             elevation = i[1]
#             building_storey_obj = self.file.createIfcBuildingStorey(create_guid(),
#                                                                     self.owner_history,                                                     float(elevation))
#             container_storey = self.file.createIfcRelAggregates(create_guid(), self.owner_history,
#                                                                 "Building Container", None, self.building,
#                                                                 [building_storey_obj])
#             building_storeys_obj.append(building_storey_obj)
#         return building_storeys_obj

# IfcProject = CreateIfcProject().file



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

    def convertobject(self):
        objs = []
        settings = ifcopenshell.geom.settings()
        for index, eachlist in enumerate(self.IFCObjects):
            if index < 20:
                for object in eachlist:
                    try:
                        points_list = []
                        z_values = []

                        min_z_points = []
                        max_z_points = []

                        min_z = float("inf")
                        max_z = float("inf")

                        elementName = util.get_psets(object)["Pset_ProductRequirements"]["Name"]
                        shape = ifcopenshell.geom.create_shape(settings, object)
                        mesh = shape.geometry
                        vertices = mesh.verts

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

                        ex = Extrusion.byPolyCurveHeight(PolyCurve.byPoints(min_z_points), top, 0)
                        ex.name = elementName
                        objs.append(ex)
                    except:
                        pass
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