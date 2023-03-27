# building.py
Python Library for creating building, building systems, object and export to any program like Blender, Revit and Speckle.

# Why?
Almost everything in a building is a frame or a panel. Windows, Curtainwalls, Floorsystems. The aim of the building.py project is automate the creation of these systems.

The goals of the building.py project are:
* Create a Pythonlibrary for geometry without dependencies.
* Exportoptions to:
  * Speckle
  * FreeCAD
  * Revit
  * XFEM4U

# Implemented

Group | Part | Implemented | ToSpeckle | ToFreeCAD 
--- | --- | --- | --- | --- 
Abstract | Vector3 | :heavy_check_mark: |  |  
-- | Vector2 | :heavy_check_mark: |  |  
-- | Plane | :heavy_check_mark: |  |  
-- | CoordinateSystem | :heavy_check_mark: |  |  
-- | Color | :heavy_check_mark: | :heavy_check_mark: |  
-- | Material | :heavy_check_mark: | |  
Geometry | Point3D | :heavy_check_mark: | :heavy_check_mark:  |  
-- | Line | :heavy_check_mark: | :heavy_check_mark:  |  
-- | Arc | :heavy_check_mark: | :heavy_check_mark:  |  
-- | PolyCurve | :heavy_check_mark: | :heavy_check_mark:  |  
-- | Point2D | :heavy_check_mark: | :heavy_check_mark:  |  
-- | Line2D | :heavy_check_mark: | :heavy_check_mark:  |  
-- | Arc2D | :heavy_check_mark: | :heavy_check_mark:  |  
-- | PolyCurve2D | :heavy_check_mark: | :heavy_check_mark:  |  
-- | LineStyle | :heavy_check_mark: | :heavy_check_mark:  |  
-- | Text | :heavy_check_mark: | :heavy_check_mark:  |  
-- | Mesh | :heavy_check_mark: | :heavy_check_mark:  |  
-- | BREP | | |  
-- | Extrusion | :heavy_check_mark: | :heavy_check_mark:  |  
-- | Sweep | | |  
Objects | Frame | :heavy_check_mark: | :heavy_check_mark:  |  
-- | FrameConnections | |  |  
--| Panel | :heavy_check_mark: | :heavy_check_mark:  |  
Library | Steelprofiles | |  |  
-- | Materials | |  |  
Exchange | Speckle | 50% |  |  
-- | IFC | |  |  
-- | PAT | |  |  
-- | OBJ | |  |  
-- | Struct4U | |  |  
Import | Image | 50% |  |  
-- | GIS | |  |  
-- | CityJSON | 50% |  |  


# Versions
Notice that this version is very much a beta version, although it is in our opinion usable. If you use it, feedback is very much appreciated!

We are currently working on version 0.1. Releasedate: april 14 2023
Versions 0.x will be subject to significant changes of the API until the release of version 1 which is planned on january 7 2024.

