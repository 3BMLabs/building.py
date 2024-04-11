#TODO
	REQUIREMENTS.txt
	FORMAT.py

#package
	helpers
	sciPy

#abstract
	#boundingbox
	#plane
	#coordinateSystem
	#vector
		Vector


#geometry
	#common
		geometry.intersect
		geometry.rotate
		geometry.translate
		geometry.transform
		geometry.split

	#curve
		#common
			curve.intersect
			curve.trim
		Polygon(Lines)
		Line(Curve)
		PolyCurve(Curves)
        Arc(Curve)
		Circle(Curve)
		Ellipse(Curve)
        Spline(Curve)
			ControlPoint
		
	#2d
		Point2D
		Vector2D
		Line2D
		Arc2D
		PolyCurve2D(Curves)
		Surface2D(PolyCurve2D)
			Opening(PolyCurve2D)
		Profile2D(Surface2D)
			#voorzien van parameters
			#gebruiken voor objecten(kanaalplaatvloer, HEA200, iets)
		ParametricProfile2D()
			Aluminium
			Generic
			Precast Concrete
			ParametricProfile2D

	#mesh
		Mesh
		
	#surface
		NurbsSurface
		PolySurface
		Surface
			Opening

	#point
		Point

	#pointcloud
		PointCloud

	#solid
        Extrusion
			Box
        Sweep
        SweptBlend


#AlgoritmnsObjects
	Pattern
    FramingAlgoritmns
		SimpleFace
	PanelAlgoritmns
	FramingSystem


#buildingsystem
	Face
		Face
		Openings
			Motherface
				Children(dependent/independent)
					Pattern
						Panel
							Stud
							Filling

    
#exchange
    #program
        FreeCAD
			import -> #import.py
        Revit
			import -> #import.py
        Blender
			import -> #import.py
        Sketchup
			import -> #import.py
		Struct4U

			import -> #import.py
        Speckle
			import -> #import.py
			utils
				Authenticator
    #file
        CSV -> #CSV.py
		PAT -> #PAT.py
        SVG -> #SVG.py
            DrawSection




#library
	#material
		Pattern
		
	#profile_database #Database of steelsections, concretesections and wood dimensions
		customprofiles #customprofiles.json
		steelprofile #steelprofile.json
		timber_europe #timber_europe.json


#objects, building objects 
    Shape(Profile2D)
	Section(Shape)
	Beam
    Floor
	Grids
	Panel
	Stud

#buildingstandardscodes
	StructuralAnalysis
		TGB1990
		Eurocodes
			EN1990
			EN1991
			NationalAnnex
	Coding #data of all sort of building codes
		Classificationsystem code
			-Source
			-StartYear
			-EndYear
			-Country
		NL
			NL-SFB
			STABU
			Revit SFB-1
			Revit SFB-2
			Revit-SFB-3
			Revit-SFB-4
		International
		Omniclass

#This pythonfile aims to contain buildingdata and algoritmns not directly linked to a certain software package. They can be used in Revit, FreeCAD, Jupyther etc.


PyBData.Materials
BaseMaterial
Color

FinishMaterial

	DrawingStandards
	Patterns
	Standard
		NL_NEN5104
		NL_Robertsen1990
		NL_3BM
		NL_OpenTopo
		NL_RevitGG
		NL_NEN2580

	FramingConnection
		Type
			Beam-Column
			Beam-Beam
			Beam-Beam-Beam
			Beam-Beam-Beam-Beam
			Column-Beam-Beam
			
		Materials
			Generic
			Steel-Steel
			Steel-Wood
				
			Wood-Wood
				
			Steel-Concrete
			Steel
		Parts
			Void
			Plate
			ConnectorSet
				Connector
					Solid
					Void
					
			
Parts:

//the framing  to the hard. T

FramingConnectionType
ConnectingMembers

SteelConnection


PyBData.Helper
	Primitives

