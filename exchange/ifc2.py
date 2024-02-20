# CODE PIECES USED OF DION MOULT
# CODE PIECES USED OF COEN  CLAUS
# 2023-08-16: Modified by Maarten Vroegindeweij
# documentation:
#  https://blenderbim.org/docs-python/autoapi/ifcopenshell/api/material/add_material_set/index.html
#  https://wiki.osarch.org/index.php?title=IFC_-_Industry_Foundation_Classes/IFC_materials
#  https://academy.ifcopenshell.org/

import ifcopenshell
import ifcopenshell.api
import sys
import pandas as pd
import numpy
import uuid
import time

O = 0., 0., 0.
X = 1., 0., 0.
Y = 0., 1., 0.
Z = 0., 0., 1.
create_guid = lambda: ifcopenshell.guid.compress(uuid.uuid1().hex)


class IfcBp:
    #Combination of
    def __init__(self,):
        self.name = "name"
        self.file = None
        self.project = None
        self.library = None
        self.app = None
        self.person = None

    def create(self, projectname, projectlibrary):
        ifcopenshell.api.pre_listeners = {}
        ifcopenshell.api.post_listeners = {}
        self.file = ifcopenshell.api.run("project.create_file")
        self.project = ifcopenshell.api.run("root.create_entity", self.file, ifc_class="IfcProject", name=projectname)
        self.library = ifcopenshell.api.run("root.create_entity", self.file, ifc_class="IfcProjectLibrary", name=projectlibrary)
        library = ifcopenshell.api.run("project.assign_declaration", self.file, definition=self.library, relating_context=self.project)
        units = ifcopenshell.api.run("unit.assign_unit", self.file,length={"is_metric": True, "raw": "MILLIMETERS"})  # METERS OR MILLIMETERS
        self.file.createIfcDirection(X)
        self.file.createIfcDirection(Y)
        self.file.createIfcDirection(Z)
        self.file.createIfcCartesianPoint(O)
        return self

    def organisation_application(self, organisation_name):
        organisation = self.file.createIfcOrganization()
        organisation.Name = organisation_name
        app = self.file.createIfcApplication()
        app.ApplicationDeveloper = organisation
        app.Version = "0.7"
        app.ApplicationFullName = "IfcOpenShell v0.7.0-1b1fd1e6"
        self.app = app
        person = self.file.createIfcPerson()
        person.FamilyName = "M.D. Vroegindeweij"
        return self

    def ownerhistory(self, person: str):
        self.owner_history = self.file.createIfcOwnerHistory()
        self.owner_history.OwningUser = self.person
        self.owner_history.OwningApplication = self.app
        self.owner_history.ChangeAction = "NOCHANGE"
        self.owner_history.CreationDate = int(time.time())
        return self

    def site_building(self, sitename, building_name):
        site_placement = self.create_ifclocalplacement()
        building_placement = self.create_ifclocalplacement(O, Z, X, site_placement)
        site = ifcopenshell.api.run("root.create_entity", self.file, ifc_class="IfcSite", name=sitename)
        building = ifcopenshell.api.run("root.create_entity", self.file, ifc_class="IfcBuilding", name=building_name)
        ifcopenshell.api.run("aggregate.assign_object", self.file, relating_object=self.file.project, product=site)
        ifcopenshell.api.run("aggregate.assign_object", self.file, relating_object=site, product=building)

    def create_ifcaxis2placement(self, point=O, dir1=Z, dir2=X):
        point = self.file.createIfcCartesianPoint(point)
        dir1 = self.file.createIfcDirection(dir1)
        dir2 = self.file.createIfcDirection(dir2)
        axis2placement = self.file.createIfcAxis2Placement3D(point, dir1, dir2)
        return axis2placement

    def create_ifclocalplacement(self, point=O, dir1=Z, dir2=X, relative_to=None):
        axis2placement = self.create_ifcaxis2placement(point, dir1, dir2)
        ifclocalplacement = self.file.createIfcLocalPlacement(relative_to, axis2placement)
        return ifclocalplacement


ifc = IfcBp().create("testproject","testlibrary")
ifc.organisation_application("3BM")
ifc.ownerhistory("Maarten")


print(ifc.app)

