from abstract.vector import Point, Vector
from construction.beam import Beam
from construction.panel import Panel
from construction.profile import RectangleProfile
from exchange.struct4U import createXFEM4UXML
from geometry.curve import PolyCurve
from library.material import BaseConcrete, BaseSteel
from project.fileformat import BuildingPy




project = BuildingPy("Steelstructure","0")

#BEAMS
project.objects.append(Beam.by_startpoint_endpoint(Point(0,0,0),Point(2000,0,0),RectangleProfile("400x600",400,600),"400x600",0,BaseConcrete))  #Concrete Beam
project.objects.append(Beam.by_startpoint_endpoint_profile_shapevector(Point(0,1000,0),Point(2000,1000,0),"HEA400","HEA400",Vector(0,0),0,BaseSteel,"Frame")) #Steel Beam

#PANELS/ PLATES IN XFEM4U
project.objects.append(Panel.by_polycurve_thickness(
    PolyCurve.by_points(
        [Point(4000,0,0),
         Point(6000,0,0),
         Point(6000,2000,0),
         Point(4000,2000,0),
         Point(4000,0,0)]),
    200,
    0,
    "Plate"
    ,BaseConcrete))

#project.toSpeckle("31d9948b31")

pathxml = "project/testXML.xml"
createXFEM4UXML(project, pathxml)
