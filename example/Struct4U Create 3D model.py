from objects.frame import *
from exchange.struct4U import *
from objects.analytical import *

project = BuildingPy("Steelstructure","0")

#BEAMS
project.objects.append(Frame.by_startpoint_endpoint(Point(0,0,0),Point(2000,0,0),Rectangle("400x600",400,600).curve,"400x600",0,BaseConcrete))  #Concrete Beam
project.objects.append(Frame.by_startpoint_endpoint_profile_name_shapevector(Point(0,1000,0),Point(2000,1000,0),"HEA400","HEA400",Vector2(0,0),0,BaseSteel,"Frame")) #Steel Beam

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
    ,BaseConcrete.colorint))

#project.toSpeckle("31d9948b31")

pathxml = "C:/TEMP/test.xml"
createXFEM4UXML(project, pathxml)