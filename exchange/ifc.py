import ifcopenshell
import ifcopenshell.api
import time


# CREATE PROJECT FILE & LIBRARY
class CreateIfcProject:
    def __init__(self, project_name, library_name,organisation_name,person_name):
        ifcopenshell.api.pre_listeners = {}
        ifcopenshell.api.post_listeners = {}

        self.file = ifcopenshell.api.run("project.create_file")
        self.project = ifcopenshell.api.run("root.create_entity", self.file, ifc_class="IfcProject", name= project_name)
        self.library = ifcopenshell.api.run("root.create_entity", self.file, ifc_class="IfcProjectLibrary",name=library_name)
        library = ifcopenshell.api.run("project.assign_declaration", self.file, definition=self.library,relating_context=self.project)
        units = ifcopenshell.api.run("unit.assign_unit", self.file,length={"is_metric": True, "raw": "MILLIMETERS"})

        # ORGANISATION DETAILS
        organisation = self.file.createIfcOrganization()
        organisation.Name = organisation_name
        person = self.file.createIfcPerson()
        person.FamilyName = person_name

        # APPLICATION
        app = self.file.createIfcApplication()
        app.ApplicationDeveloper = organisation
        app.Version = "0.7"
        app.ApplicationFullName = "IfcOpenShell v0.7.0-1b1fd1e6"

        # OWNER HISTORY
        self.owner_history = self.file.createIfcOwnerHistory()
        self.owner_history.OwningUser = person
        self.owner_history.OwningApplication = app
        self.owner_history.ChangeAction = "NOCHANGE"
        self.owner_history.CreationDate = int(time.time())

        # CREATE THE SITE
        site_placement = self.create_ifclocalplacement()

        # CREATE THE BUILDING
        building_placement = self.create_ifclocalplacement(O, Z, X, site_placement)
        # building = self.file.createIfcBuilding(create_guid(), self.owner_history, 'Bouwwerk', None, None,building_placement, None, None, "ELEMENT", None, None, None)

        self.site = ifcopenshell.api.run("root.create_entity", self.file, ifc_class="IfcSite", name="Site")
        self.building = ifcopenshell.api.run("root.create_entity", self.file, ifc_class="IfcBuilding", name=project_name)

        # Since the site is our top level location, assign it to the project
        # Then place our building on the site, and our storey in the building
        ifcopenshell.api.run("aggregate.assign_object", self.file, relating_object=self.project, product=self.site)
        ifcopenshell.api.run("aggregate.assign_object", self.file, relating_object=self.site, product=self.building)

        # CREATE BUILDING STOREYS
        self.storey_placement = self.create_ifclocalplacement(O, Z, X, relative_to=building_placement)
        storeys_obj = self.create_building_storeys(building_storeys_lst)
        storey = storeys_obj[2]
        # storey = ifcopenshell.api.run("root.create_entity", self.file, ifc_class="IfcBuildingStorey", name="peil=0")
        ifcopenshell.api.run("aggregate.assign_object", self.file, relating_object=self.building, product=storey)

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

    def create_building_storeys(self, building_storeys):
        building_storeys_obj = []
        for i in building_storeys:
            name = i[0]
            elevation = i[1]
            building_storey_obj = self.file.createIfcBuildingStorey(create_guid(),
                                                                    self.owner_history,
                                                                    name,
                                                                    None,
                                                                    None,
                                                                    self.storey_placement,
                                                                    None,
                                                                    None,
                                                                    "ELEMENT",
                                                                    float(elevation))

            container_storey = self.file.createIfcRelAggregates(create_guid(), self.owner_history,
                                                                "Building Container", None, self.building,
                                                                [building_storey_obj])
            building_storeys_obj.append(building_storey_obj)
        return building_storeys_obj

IfcProject = CreateIfcProject().file
